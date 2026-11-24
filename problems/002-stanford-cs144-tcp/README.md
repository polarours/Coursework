# 002 · Stanford CS144 — 手写 TCP / Build a TCP
- 来源高校 / University profile: [Stanford University](https://polarours.github.io/Coursework/universities/stanford.html)

- 课程 / Course: Stanford CS144 Introduction to Computer Networking
- 官方 / Official: https://cs144.github.io/
- GitHub: https://github.com/CS144/
- 方向 / Area: 计算机网络 / Networking
- 难度 / Difficulty: 进阶 / Intermediate–advanced
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python 基础、网络基础 / Python basics, networking basics
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

从零构建可靠传输：分段、确认、重传、滑动窗口、拥塞控制。每一层都能用真实测试验证，是把网络课理论变成工程能力的经典项目。
Building reliable transport from scratch — segmentation, ACKs, retransmission, sliding window, congestion control. Every layer is testable, making it a classic bridge from networking theory to engineering skill.

> **English:** CS144's lab string is unusually well-scoped: each stage is independently testable, so students get fast feedback on subtle protocol logic.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/tcp.py`：独立编写的 Python 教学实现，含 ByteStream、Reassembler、TCPReceiver、TCPSender（虚拟时钟，测试确定性强）。运行 / Run:

```bash
python3 tests/test_tcp.py
```

## 实测结果 / Verified results

- 6 项测试全部通过（重组、回绕、接收端、重传退避、滑动窗口、端到端）/ 6 tests pass
- 端到端：4 个段完整送达 `the quick brown fox`（19 字节 + SYN/FIN）/ end-to-end delivery verified
- 详见 [05-调试与测试.md](05-调试与测试.md) 中的真实输出与开发中修正的 3 个测试错误
