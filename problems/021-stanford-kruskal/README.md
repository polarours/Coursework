# 021 · Stanford 算法 — Kruskal 最小生成树
- 来源高校 / University profile: [Stanford University](https://polarours.github.io/Coursework/universities/stanford.html)

- 课程 / Course: Stanford CS161 Design and Analysis of Algorithms
- 官方 / Official: https://web.stanford.edu/class/cs161/
- 方向 / Area: 图算法 / Graph algorithms
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 3–6 天
- 前置 / Prerequisites: Python、图基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Kruskal 是贪心算法的典范：并查集让「选边不成环」高效实现，是理解贪心正确性与数据结构配合的绝佳题目。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 经典图 MST 权重 37 与教科书答案一致；不连通图只得到 2 条边（少于 n-1），正确处理了非连通情况。
- 详见 [05-调试与测试.md](05-调试与测试.md)
