// Package raft 提供一个用于教学的 Raft 共识算法实现。
// 这是独立编写的教学版代码，不是 MIT 6.824 官方实验框架，也不复制任何现有 solution 仓库。
package raft

import (
	"math/rand"
	"sync"
	"time"
)

// State 是节点的三种角色。
type State int

const (
	Follower State = iota
	Candidate
	Leader
)

func (s State) String() string {
	switch s {
	case Follower:
		return "Follower"
	case Candidate:
		return "Candidate"
	case Leader:
		return "Leader"
	}
	return "Unknown"
}

// LogEntry 是复制日志中的一条记录；index 0 是哨兵条目。
type LogEntry struct {
	Term    int
	Command string
}

// ApplyMsg 是已提交日志向上层状态机投递的消息。
type ApplyMsg struct {
	Index   int
	Command string
}

// RequestVoteArgs / Reply 是选举 RPC 的参数与响应。
type RequestVoteArgs struct {
	Term         int
	CandidateId  int
	LastLogIndex int
	LastLogTerm  int
}

type RequestVoteReply struct {
	Term        int
	VoteGranted bool
}

// AppendEntriesArgs / Reply 是日志复制与心跳 RPC 的参数与响应。
type AppendEntriesArgs struct {
	Term         int
	LeaderId     int
	PrevLogIndex int
	PrevLogTerm  int
	Entries      []LogEntry
	LeaderCommit int
}

type AppendEntriesReply struct {
	Term    int
	Success bool
}

// Persister 模拟持久化存储：term、投票和日志在状态变更时写回。
type Persister struct {
	mu          sync.Mutex
	currentTerm int
	votedFor    int
	log         []LogEntry
}

func NewPersister() *Persister { return &Persister{votedFor: -1} }

func (p *Persister) save(term, vote int, log []LogEntry) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.currentTerm = term
	p.votedFor = vote
	p.log = append([]LogEntry(nil), log...)
}

func (p *Persister) load() (int, int, []LogEntry) {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.currentTerm, p.votedFor, append([]LogEntry(nil), p.log...)
}

// Raft 是一个共识节点。
type Raft struct {
	mu sync.Mutex

	id    int
	peers []int // 其他节点的 id
	net   *Network

	state       State
	currentTerm int
	votedFor    int // -1 表示未投票
	log         []LogEntry
	commitIndex int
	lastApplied int

	// 仅 leader 使用，按节点 id 索引
	nextIndex  []int
	matchIndex []int

	persister *Persister
	applyCh   chan ApplyMsg

	electionDeadline  time.Time
	heartbeatInterval time.Duration
	electionMin       time.Duration
	electionMax       time.Duration

	stopCh  chan struct{}
	stopped bool
}

// NewRaft 创建并启动一个节点。参数 peers 不含自己。
func NewRaft(id int, peers []int, net *Network, persister *Persister, applyCh chan ApplyMsg) *Raft {
	term, vote, log := persister.load()
	if len(log) == 0 {
		log = []LogEntry{{Term: 0, Command: ""}}
	}
	n := len(peers) + 1
	rf := &Raft{
		id: id, peers: peers, net: net,
		state: Follower, currentTerm: term, votedFor: vote, log: log,
		nextIndex: make([]int, n), matchIndex: make([]int, n),
		persister: persister, applyCh: applyCh,
		heartbeatInterval: 60 * time.Millisecond,
		electionMin:       180 * time.Millisecond,
		electionMax:       320 * time.Millisecond,
		stopCh:            make(chan struct{}),
	}
	rf.resetElectionDeadline()
	net.register(id, rf)
	go rf.run()
	go rf.applyLoop()
	return rf
}

// 以下辅助函数要求调用方已持有 rf.mu。
func (rf *Raft) save() {
	rf.persister.save(rf.currentTerm, rf.votedFor, rf.log)
}

func (rf *Raft) lastLogTerm() int {
	return rf.log[len(rf.log)-1].Term
}

func (rf *Raft) resetElectionDeadline() {
	d := rf.electionMin + time.Duration(rand.Int63n(int64(rf.electionMax-rf.electionMin)))
	rf.electionDeadline = time.Now().Add(d)
}

// ID 返回节点 id。
func (rf *Raft) ID() int { return rf.id }

// GetState 返回当前 term 与角色，供测试与观测使用。
func (rf *Raft) GetState() (int, State) {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	return rf.currentTerm, rf.state
}

// LogSnapshot 返回日志副本。
func (rf *Raft) LogSnapshot() []LogEntry {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	return append([]LogEntry(nil), rf.log...)
}

// CommitIndex 返回当前提交位点。
func (rf *Raft) CommitIndex() int {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	return rf.commitIndex
}

// Stop 停止节点的主循环。
func (rf *Raft) Stop() {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	if rf.stopped {
		return
	}
	rf.stopped = true
	close(rf.stopCh)
}

// run 是事件循环：leader 定期发心跳，其他角色在选举超时后发起选举。
func (rf *Raft) run() {
	for {
		select {
		case <-rf.stopCh:
			return
		default:
		}
		rf.mu.Lock()
		state, deadline := rf.state, rf.electionDeadline
		rf.mu.Unlock()

		if state == Leader {
			rf.broadcastAppendEntries()
			time.Sleep(rf.heartbeatInterval)
			continue
		}
		if time.Now().After(deadline) {
			rf.startElection()
		} else {
			time.Sleep(10 * time.Millisecond)
		}
	}
}

func (rf *Raft) broadcastAppendEntries() {
	for _, p := range rf.peers {
		if p == rf.id {
			continue
		}
		go rf.sendAppendEntries(p)
	}
}

// startElection 自增 term、投给自己，并向所有 peer 请求投票。
func (rf *Raft) startElection() {
	rf.mu.Lock()
	rf.currentTerm++
	rf.state = Candidate
	rf.votedFor = rf.id
	term := rf.currentTerm
	args := &RequestVoteArgs{
		Term:         term,
		CandidateId:  rf.id,
		LastLogIndex: len(rf.log) - 1,
		LastLogTerm:  rf.lastLogTerm(),
	}
	rf.resetElectionDeadline()
	rf.save()
	rf.mu.Unlock()

	votes := 1 // 自己的一票
	majority := (len(rf.peers)+1)/2 + 1
	var wg sync.WaitGroup
	var voteMu sync.Mutex

	for _, p := range rf.peers {
		wg.Add(1)
		go func(peer int) {
			defer wg.Done()
			resp, ok := rf.net.send(rf.id, peer, args)
			if !ok {
				return
			}
			r := resp.(*RequestVoteReply)

			voteMu.Lock()
			defer voteMu.Unlock()

			if r.Term > term {
				rf.mu.Lock()
				if rf.currentTerm < r.Term {
					rf.currentTerm = r.Term
					rf.votedFor = -1
					rf.state = Follower
					rf.save()
				}
				rf.mu.Unlock()
				return
			}
			if r.VoteGranted {
				votes++
				if votes >= majority {
					rf.becomeLeader(term)
				}
			}
		}(p)
	}
	wg.Wait()
}

func (rf *Raft) becomeLeader(term int) {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	if rf.currentTerm != term || rf.state != Candidate {
		return
	}
	rf.state = Leader
	for i := range rf.nextIndex {
		rf.nextIndex[i] = len(rf.log)
	}
	for i := range rf.matchIndex {
		rf.matchIndex[i] = 0
	}
	rf.matchIndex[rf.id] = len(rf.log) - 1
}

// sendAppendEntries 向单个 peer 发送心跳或日志条目。
func (rf *Raft) sendAppendEntries(peer int) {
	rf.mu.Lock()
	if rf.state != Leader {
		rf.mu.Unlock()
		return
	}
	term := rf.currentTerm
	next := rf.nextIndex[peer]
	if next < 1 {
		next = 1
	}
	prevIndex := next - 1
	prevTerm := rf.log[prevIndex].Term
	var entries []LogEntry
	if next < len(rf.log) {
		entries = append(entries, rf.log[next:]...)
	}
	args := &AppendEntriesArgs{
		Term: term, LeaderId: rf.id, PrevLogIndex: prevIndex,
		PrevLogTerm: prevTerm, Entries: entries, LeaderCommit: rf.commitIndex,
	}
	rf.mu.Unlock()

	resp, ok := rf.net.send(rf.id, peer, args)
	if !ok {
		return
	}
	r := resp.(*AppendEntriesReply)

	rf.mu.Lock()
	defer rf.mu.Unlock()
	if r.Term > rf.currentTerm {
		rf.currentTerm = r.Term
		rf.votedFor = -1
		rf.state = Follower
		rf.save()
		return
	}
	if rf.state != Leader || rf.currentTerm != term {
		return
	}
	if r.Success {
		rf.nextIndex[peer] = prevIndex + len(entries) + 1
		rf.matchIndex[peer] = prevIndex + len(entries)
		rf.advanceCommit()
	} else if rf.nextIndex[peer] > 1 {
		rf.nextIndex[peer]--
	}
}

// advanceCommit 尝试推进 commitIndex：某 index 被多数派复制且 term 等于当前 term。
func (rf *Raft) advanceCommit() {
	n := len(rf.log) - 1
	for n > rf.commitIndex {
		count := 1 // leader 自己
		for id, m := range rf.matchIndex {
			if id != rf.id && m >= n {
				count++
			}
		}
		if count >= len(rf.matchIndex)/2+1 && rf.log[n].Term == rf.currentTerm {
			rf.commitIndex = n
			break
		}
		n--
	}
}

// handleRequestVote 处理投票请求。
func (rf *Raft) handleRequestVote(args *RequestVoteArgs, reply *RequestVoteReply) bool {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	reply.Term = rf.currentTerm
	if args.Term < rf.currentTerm {
		return true
	}
	if args.Term > rf.currentTerm {
		rf.currentTerm = args.Term
		rf.votedFor = -1
		rf.state = Follower
		rf.save()
	}
	lastTerm := rf.lastLogTerm()
	lastIndex := len(rf.log) - 1
	upToDate := args.LastLogTerm > lastTerm ||
		(args.LastLogTerm == lastTerm && args.LastLogIndex >= lastIndex)
	if (rf.votedFor == -1 || rf.votedFor == args.CandidateId) && upToDate {
		rf.votedFor = args.CandidateId
		rf.state = Follower
		rf.resetElectionDeadline()
		rf.save()
		reply.VoteGranted = true
	}
	return true
}

// handleAppendEntries 处理日志复制/心跳：一致性检查、冲突截断、跟提交位点。
func (rf *Raft) handleAppendEntries(args *AppendEntriesArgs, reply *AppendEntriesReply) bool {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	reply.Term = rf.currentTerm
	if args.Term < rf.currentTerm {
		return true
	}
	if args.Term > rf.currentTerm {
		rf.currentTerm = args.Term
		rf.votedFor = -1
		rf.save()
	}
	rf.state = Follower
	rf.resetElectionDeadline()

	if args.PrevLogIndex >= len(rf.log) || rf.log[args.PrevLogIndex].Term != args.PrevLogTerm {
		return true // reply.Success 默认 false
	}
	for i, e := range args.Entries {
		idx := args.PrevLogIndex + 1 + i
		if idx < len(rf.log) {
			if rf.log[idx].Term != e.Term {
				rf.log = rf.log[:idx]
				rf.log = append(rf.log, e)
			}
		} else {
			rf.log = append(rf.log, e)
		}
	}
	if args.LeaderCommit > rf.commitIndex {
		rf.commitIndex = min(args.LeaderCommit, len(rf.log)-1)
	}
	reply.Success = true
	rf.save()
	return true
}

// Start 由上层状态机调用，把一条命令追加到 leader 日志。
func (rf *Raft) Start(command string) (int, bool) {
	rf.mu.Lock()
	defer rf.mu.Unlock()
	if rf.state != Leader {
		return -1, false
	}
	rf.log = append(rf.log, LogEntry{Term: rf.currentTerm, Command: command})
	rf.matchIndex[rf.id] = len(rf.log) - 1
	rf.save()
	return len(rf.log) - 1, true
}

// applyLoop 把已提交但尚未应用的日志投递给上层状态机。
func (rf *Raft) applyLoop() {
	for {
		select {
		case <-rf.stopCh:
			return
		default:
		}
		rf.mu.Lock()
		if rf.lastApplied < rf.commitIndex {
			rf.lastApplied++
			msg := ApplyMsg{Index: rf.lastApplied, Command: rf.log[rf.lastApplied].Command}
			rf.mu.Unlock()
			rf.applyCh <- msg
		} else {
			rf.mu.Unlock()
			time.Sleep(10 * time.Millisecond)
		}
	}
}
