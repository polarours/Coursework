package raft

import (
	"sync"
	"time"
)

// Network 是内存中的 RPC 传输层，支持离线与网络分区，便于教学测试。
type Network struct {
	mu        sync.Mutex
	nodes     map[int]*Raft
	offline   map[int]bool
	partition map[int]int
	delay     time.Duration
	rpcCount  int
}

func NewNetwork() *Network {
	return &Network{
		nodes:     make(map[int]*Raft),
		offline:   make(map[int]bool),
		partition: make(map[int]int),
		delay:     2 * time.Millisecond,
	}
}

func (n *Network) register(id int, rf *Raft) {
	n.mu.Lock()
	defer n.mu.Unlock()
	n.nodes[id] = rf
	n.partition[id] = 0
}

// SetOffline 模拟节点宕机：它发出的和发给它的 RPC 都会被丢弃。
func (n *Network) SetOffline(id int, offline bool) {
	n.mu.Lock()
	defer n.mu.Unlock()
	n.offline[id] = offline
}

// Partition 把节点划分为多个互通组；不同组之间无法通信。
func (n *Network) Partition(groups ...[]int) {
	n.mu.Lock()
	defer n.mu.Unlock()
	for gi, g := range groups {
		for _, id := range g {
			n.partition[id] = gi
		}
	}
}

// Heal 清除所有分区与离线设置。
func (n *Network) Heal() {
	n.mu.Lock()
	defer n.mu.Unlock()
	for id := range n.nodes {
		n.partition[id] = 0
		n.offline[id] = false
	}
}

func (n *Network) send(from, to int, req interface{}) (interface{}, bool) {
	n.mu.Lock()
	target := n.nodes[to]
	reachable := target != nil && !n.offline[from] && !n.offline[to] &&
		n.partition[from] == n.partition[to]
	d := n.delay
	if reachable {
		n.rpcCount++
	}
	n.mu.Unlock()
	if !reachable {
		return nil, false
	}
	if d > 0 {
		time.Sleep(d)
	}
	switch a := req.(type) {
	case *RequestVoteArgs:
		reply := &RequestVoteReply{}
		target.handleRequestVote(a, reply)
		return reply, true
	case *AppendEntriesArgs:
		reply := &AppendEntriesReply{}
		target.handleAppendEntries(a, reply)
		return reply, true
	}
	return nil, false
}

// RPCCount 返回已投递的 RPC 总数，用于观测。
func (n *Network) RPCCount() int {
	n.mu.Lock()
	defer n.mu.Unlock()
	return n.rpcCount
}
