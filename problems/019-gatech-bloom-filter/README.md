# 019 · Georgia Tech — 布隆过滤器
- 来源高校 / University profile: [Georgia Institute of Technology](https://polarours.github.io/Coursework/universities/gatech.html)

- 课程 / Course: Georgia Tech CS 8803 Database Systems
- 官方 / Official: https://faculty.cc.gatech.edu/~jarulraj/courses/8803-s23/
- 方向 / Area: 概率数据结构 / Probabilistic DS
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 3–6 天
- 前置 / Prerequisites: Python、哈希基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

布隆过滤器用极小的空间换取「可能有」的查询——以可控假阳性换取常数空间，是数据库与网络中的实用结构。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 已插入的 3 个元素全部命中（无假阴性）；1000 个不存在项的假阳性为 0，增大过滤器到 8192 位后仍为 0。
- 详见 [05-调试与测试.md](05-调试与测试.md)
