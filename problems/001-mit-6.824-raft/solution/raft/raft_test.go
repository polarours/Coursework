package raft

import (
	"fmt"
	"testing"
	"time"
)

func makeCluster(n int) (*Network, []*Raft, []chan ApplyMsg) {
	net := NewNetwork()
	rafts := make([]*Raft, n)
	chans := make([]chan ApplyMsg, n)
	for i := 0; i < n; i++ {
		chans[i] = make(chan ApplyMsg, 1000)
		others := []int{}
		for j := 0; j < n; j++ {
			if j != i {
				others = append(others, j)
			}
		}
		rafts[i] = NewRaft(i, others, net, NewPersister(), chans[i])
	}
	return net, rafts, chans
}

func cleanup(rafts []*Raft) {
	for _, rf := range rafts {
		rf.Stop()
	}
}

func waitForLeader(t *testing.T, rafts []*Raft, timeout time.Duration) int {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		leaders := []int{}
		for _, rf := range rafts {
			if _, st := rf.GetState(); st == Leader {
				leaders = append(leaders, rf.id)
			}
		}
		if len(leaders) == 1 {
			return leaders[0]
		}
		time.Sleep(20 * time.Millisecond)
	}
	t.Fatalf("在 %v 内没有选出唯一 leader", timeout)
	return -1
}

func drain(ch chan ApplyMsg) []string {
	got := []string{}
	for len(ch) > 0 {
		got = append(got, (<-ch).Command)
	}
	return got
}

func TestElection(t *testing.T) {
	net, rafts, _ := makeCluster(3)
	defer cleanup(rafts)
	l := waitForLeader(t, rafts, 3*time.Second)
	term, _ := rafts[l].GetState()
	fmt.Printf("[TestElection] 选出 leader=node %d, term=%d, RPC 总数=%d\n", l, term, net.RPCCount())
}

func TestLogReplication(t *testing.T) {
	_, rafts, chans := makeCluster(3)
	defer cleanup(rafts)
	l := waitForLeader(t, rafts, 3*time.Second)
	leader := rafts[l]
	cmds := []string{"SET a=1", "SET b=2", "DEL a"}
	for _, c := range cmds {
		idx, ok := leader.Start(c)
		if !ok {
			t.Fatal("Start 在 leader 上失败")
		}
		fmt.Printf("[TestLogReplication] leader %d 接收 %q @ index %d\n", l, c, idx)
	}
	deadline := time.Now().Add(3 * time.Second)
	for time.Now().Before(deadline) {
		all := true
		for i := range chans {
			if len(chans[i]) < len(cmds) {
				all = false
			}
		}
		if all {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	for i, ch := range chans {
		got := drain(ch)
		fmt.Printf("[TestLogReplication] node %d applied=%v commitIndex=%d\n", i, got, rafts[i].CommitIndex())
		if len(got) != len(cmds) {
			t.Fatalf("node %d 只 apply 了 %d 条，期望 %d", i, len(got), len(cmds))
		}
		for j := range cmds {
			if got[j] != cmds[j] {
				t.Fatalf("node %d 第 %d 条=%q，期望 %q", i, j, got[j], cmds[j])
			}
		}
	}
}

func TestLeaderFailover(t *testing.T) {
	net, rafts, chans := makeCluster(3)
	defer cleanup(rafts)
	old := waitForLeader(t, rafts, 3*time.Second)
	net.SetOffline(old, true)
	fmt.Printf("[TestLeaderFailover] 旧 leader node %d 宕机\n", old)

	newLeader := -1
	deadline := time.Now().Add(4 * time.Second)
	for time.Now().Before(deadline) {
		for _, rf := range rafts {
			if rf.id == old {
				continue
			}
			if _, st := rf.GetState(); st == Leader {
				newLeader = rf.id
				break
			}
		}
		if newLeader >= 0 {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	if newLeader < 0 {
		t.Fatal("没有选出新 leader")
	}
	fmt.Printf("[TestLeaderFailover] 新 leader=node %d\n", newLeader)

	cmd := "after-failover"
	idx, ok := rafts[newLeader].Start(cmd)
	if !ok {
		t.Fatal("新 leader 的 Start 失败")
	}
	fmt.Printf("[TestLeaderFailover] 新 leader 接收 %q @ index %d\n", cmd, idx)

	deadline = time.Now().Add(3 * time.Second)
	for time.Now().Before(deadline) {
		all := true
		for i := range rafts {
			if i == old {
				continue
			}
			if len(chans[i]) < 1 {
				all = false
			}
		}
		if all {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	for i := range rafts {
		if i == old {
			continue
		}
		got := drain(chans[i])
		fmt.Printf("[TestLeaderFailover] 存活 node %d applied=%v\n", i, got)
		if len(got) < 1 || got[0] != cmd {
			t.Fatalf("node %d 未复制故障后的命令：%v", i, got)
		}
	}
}

func TestPartitionSafety(t *testing.T) {
	net, rafts, chans := makeCluster(5)
	defer cleanup(rafts)
	l := waitForLeader(t, rafts, 3*time.Second)
	fmt.Printf("[TestPartitionSafety] 分区前 leader=node %d\n", l)

	// 把 leader 所在的小分区（2 节点）与多数派分区（3 节点）隔开
	small, large := []int{}, []int{}
	for i := 0; i < 5; i++ {
		if i == l || (l+1)%5 == i {
			small = append(small, i)
		} else {
			large = append(large, i)
		}
	}
	net.Partition(small, large)
	fmt.Printf("[TestPartitionSafety] 小分区=%v 大分区=%v\n", small, large)

	// 少数派 leader 仍可 Start，但不应提交
	idx, ok := rafts[l].Start("minority-write")
	fmt.Printf("[TestPartitionSafety] 少数派 leader Start=%v index=%d commitIndex=%d\n", ok, idx, rafts[l].CommitIndex())
	if ok && rafts[l].CommitIndex() >= idx {
		t.Fatal("少数派分区不应该提交日志")
	}

	// 多数派分区应选出新 leader 并提交
	newLeader := -1
	deadline := time.Now().Add(4 * time.Second)
	for time.Now().Before(deadline) {
		for _, id := range large {
			if _, st := rafts[id].GetState(); st == Leader {
				newLeader = id
				break
			}
		}
		if newLeader >= 0 {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	if newLeader < 0 {
		t.Fatal("多数派分区没有选出新 leader")
	}
	fmt.Printf("[TestPartitionSafety] 多数派新 leader=node %d\n", newLeader)

	cmd := "majority-write"
	if _, ok := rafts[newLeader].Start(cmd); !ok {
		t.Fatal("多数派 leader Start 失败")
	}
	deadline = time.Now().Add(3 * time.Second)
	for time.Now().Before(deadline) {
		all := true
		for _, id := range large {
			if len(chans[id]) < 1 {
				all = false
			}
		}
		if all {
			break
		}
		time.Sleep(20 * time.Millisecond)
	}
	for _, id := range large {
		got := drain(chans[id])
		fmt.Printf("[TestPartitionSafety] 多数派 node %d applied=%v\n", id, got)
		if len(got) < 1 || got[0] != cmd {
			t.Fatalf("多数派 node %d 未提交：%v", id, got)
		}
	}

	net.Heal()
	fmt.Println("[TestPartitionSafety] 网络恢复，等待日志收敛…")
	deadline = time.Now().Add(4 * time.Second)
	for time.Now().Before(deadline) {
		logs := rafts[small[0]].LogSnapshot()
		want := rafts[newLeader].LogSnapshot()
		if len(logs) == len(want) && len(logs) > 0 {
			same := true
			for i := range logs {
				if logs[i] != want[i] {
					same = false
				}
			}
			if same {
				fmt.Printf("[TestPartitionSafety] 日志已收敛：%v\n", logs[1:])
				return
			}
		}
		time.Sleep(20 * time.Millisecond)
	}
	t.Fatal("网络恢复后日志未收敛")
}
