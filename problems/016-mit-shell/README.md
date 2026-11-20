# 016 · MIT 6.858 — Shell 解析器

- 课程 / Course: MIT 6.858 Computer Systems Security
- 官方 / Official: https://pdos.csail.mit.edu/6.858/
- 方向 / Area: 系统编程 / Systems
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天
- 前置 / Prerequisites: Python、操作系统基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Shell 是理解进程、文件描述符与解析的经典系统作业。本项目实现词法/解析层：管道、重定向、引号与变量展开。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

见 `solution/`，运行 / Run: `python3 tests/test_*.py`

## 实测结果 / Verified results

- 三级管道 `wc -l < a.txt | sort | uniq > result.txt` 正确解析为 3 个命令；引号内的空格保持为单个参数。
- 详见 [05-调试与测试.md](05-调试与测试.md)
