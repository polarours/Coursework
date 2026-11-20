# 005 · MIT 6.1810 — xv6 核心机制模拟器

- 课程 / Course: MIT 6.1810 Operating Systems Engineering（原 6.828）
- 官方 / Official: https://pdos.csail.mit.edu/6.1810/
- 方向 / Area: 操作系统 / Operating systems
- 难度 / Difficulty: 硬核 / Advanced
- 预计耗时 / Estimated effort: 5–10 天 / 5–10 days
- 前置 / Prerequisites: C/Python、操作系统基础 / C/Python, OS basics
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

xv6 实验让学生修改教学用 Unix 内核，是理解操作系统最经典的路径。本项目聚焦调度与伙伴分配器两个算法核心，做成自包含的模拟器。
The xv6 labs are the classic path to understanding operating systems. We focus on two algorithmic cores — scheduling and buddy allocation — as a self-contained simulator.

> **English:** Keeping the algorithmic core while dropping QEMU/toolchain baggage makes these OS concepts accessible in a self-contained learning repo.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/xv6sim.py`：FCFS / Round Robin / MLFQ 三种调度 + 伙伴分配器。运行 / Run:

```bash
python3 tests/test_xv6sim.py
```

## 实测结果 / Verified results

- FCFS avg_wait=3.33；RR（q=2）=6.00；MLFQ=5.33（真实输出，见 05）
- 伙伴分配器：alloc(7)→0, alloc(8)→8, alloc(4)→16；free(8)+free(0) 后合并出 (0,16)
- 如实记录了 RR 平均等待高于 FCFS 的调度理论原因（非 bug）
