# 014 · Princeton COS226 — 8-Puzzle

- 课程 / Course: Princeton COS 226 Algorithms and Data Structures
- 官方 / Official: https://algs4.cs.princeton.edu/
- 方向 / Area: 算法 / Algorithms
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 3–6 天 / 3–6 days
- 前置 / Prerequisites: Python、搜索算法基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

A* 搜索 + 曼哈顿距离可采纳启发式；逆序数判定可解性——启发式搜索的经典教学题。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/puzzle.py（曼哈顿距离 + A* + 可解性判定）`。运行 / Run:

```bash
python3 tests/test_puzzle.py
```

## 实测结果 / Verified results

- 1 步局面解长度 1；不可解局面正确返回 None；A* 最优性验证。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
