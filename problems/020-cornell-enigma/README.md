# 020 · Cornell CS3110 — Enigma 密码机

- 课程 / Course: Cornell CS 3110 Functional Programming
- 官方 / Official: https://www.cs.cornell.edu/courses/cs3110/2020fa/a1/
- 方向 / Area: 密码学 / Cryptography
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天
- 前置 / Prerequisites: Python、函数式思维
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Enigma 是 CS3110 的经典作业：用纯函数式思维实现转子密码机，理解状态、映射与对称性。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 加解密对称（HELLO→WSDUQ→HELLO）验证了反射器的数学性质；连续两个 A 得到 Q 和 X，证明转子每次加密后推进。
- 详见 [05-调试与测试.md](05-调试与测试.md)
