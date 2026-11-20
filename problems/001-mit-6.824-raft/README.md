# 001 · MIT 6.824 / 6.5840 — Raft

- 课程 / Course: MIT 6.824 / 6.5840 Distributed Systems
- 官方 / Official: https://pdos.csail.mit.edu/6.824/
- 社区参考 / Community reference: https://github.com/WenbinZhu/mit-6.824-labs
- 方向 / Area: 分布式系统 / Distributed systems
- 难度 / Difficulty: 硬核 / Advanced
- 预计耗时 / Estimated effort: 5–10 天 / 5–10 days
- 前置 / Prerequisites: Go、并发基础 / Go, concurrency basics
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Raft 要求实现共识算法：leader 选举、日志复制、持久化与安全性。难点不在代码量，而在对并发与故障的推理——这正是最能锻炼思考能力的那类题目。
Raft requires implementing consensus: leader election, log replication, persistence, and safety. The difficulty lies in reasoning about concurrency and failures — exactly the kind of problem that builds deep thinking.

> **English:** Raft is a capstone in reasoning, not just coding: correctness under network partitions and crashes forces students to reason about invariants rather than APIs.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/` 目录为独立编写的 Go 教学实现（module `coursework/raft001`），含内存网络模拟器，可注入宕机与分区。运行 / Run:

```bash
cd solution && go test ./... -v -count=1
```

## 实测结果 / Verified results

- 4 项测试全部通过（选举、日志复制、leader 故障转移、分区安全）/ 4 tests pass
- `go test -race` 无数据竞争 / no data races
- 详见 [05-调试与测试.md](05-调试与测试.md) 中的真实输出 / real output in chapter 05
