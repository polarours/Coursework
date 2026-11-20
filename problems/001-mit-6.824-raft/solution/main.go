// Command raft-demo 演示一个 3 节点 Raft 集群的选举与日志复制。
package main

import (
	"fmt"
	"time"

	"coursework/raft001/raft"
)

func main() {
	net := raft.NewNetwork()
	rafts := make([]*raft.Raft, 3)
	chans := make([]chan raft.ApplyMsg, 3)
	for i := 0; i < 3; i++ {
		chans[i] = make(chan raft.ApplyMsg, 100)
		others := []int{}
		for j := 0; j < 3; j++ {
			if j != i {
				others = append(others, j)
			}
		}
		rafts[i] = raft.NewRaft(i, others, net, raft.NewPersister(), chans[i])
	}
	defer func() {
		for _, r := range rafts {
			r.Stop()
		}
	}()

	time.Sleep(800 * time.Millisecond)
	leader := -1
	for _, r := range rafts {
		if term, st := r.GetState(); st == raft.Leader {
			leader = r.ID()
			fmt.Printf("leader = node %d, term = %d\n", leader, term)
		}
	}
	if leader < 0 {
		fmt.Println("未选出 leader")
		return
	}
	for _, cmd := range []string{"GET x", "SET x=42", "DEL x"} {
		idx, ok := rafts[leader].Start(cmd)
		fmt.Printf("提交命令 %q -> index=%d ok=%v\n", cmd, idx, ok)
	}
	time.Sleep(500 * time.Millisecond)
	for i, ch := range chans {
		got := []string{}
		for len(ch) > 0 {
			got = append(got, (<-ch).Command)
		}
		fmt.Printf("node %d 应用层收到: %v (commitIndex=%d)\n", i, got, rafts[i].CommitIndex())
	}
}
