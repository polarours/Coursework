# 018 · MIT 6.006 — LRU 缓存

- 课程 / Course: MIT 6.006 Introduction to Algorithms
- 官方 / Official: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/
- 方向 / Area: 数据结构 / Data structures
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 3–6 天
- 前置 / Prerequisites: Python、哈希表
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

LRU 缓存是哈希表与双向链表结合的经典题：O(1) 完成读写与淘汰，是理解数据结构组合的绝佳案例。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- get(1) 后顺序从 [2,1] 变为 [1,2]，证明命中被提升为 MRU；put(3) 淘汰了 LRU 的键 2。
- 详见 [05-调试与测试.md](05-调试与测试.md)
