# 017 · CMU 15-112 — 计算几何基础
- 来源高校 / University profile: [Carnegie Mellon University](https://polarours.github.io/Coursework/universities/cmu.html)

- 课程 / Course: CMU 15-112 Fundamentals of Programming
- 官方 / Official: https://www.cs.cmu.edu/~112/notes/project.html
- 方向 / Area: 计算几何 / Geometry
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天
- 前置 / Prerequisites: Python、向量基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

计算几何是算法与图形学的基础：叉积这一个原语就能派生出相交判定、凸包与点包含等算法。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 叉积符号区分顺逆时针；十字交叉的线段相交返回 True，共线不相交返回 False；凸包排除了内部点。
- 详见 [05-调试与测试.md](05-调试与测试.md)
