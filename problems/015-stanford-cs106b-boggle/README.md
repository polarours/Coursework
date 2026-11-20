# 015 · Stanford CS106B — Boggle 回溯求解

- 课程 / Course: Stanford CS106B Programming Abstractions
- 官方 / Official: https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1212/assignments/4-backtracking/boggle
- 方向 / Area: 回溯与搜索 / Backtracking
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天
- 前置 / Prerequisites: Python、递归
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Boggle 是经典的回溯法教学题：在字母网格中用 DFS 穷举所有可能路径，配合 Trie 前缀剪枝大幅减少无效搜索。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 2×2 网格含对角时完全连通，6 个词全部可达；3×3 中 `aei` 沿对角链可达，证明 8 邻域正确。
- 详见 [05-调试与测试.md](05-调试与测试.md)
