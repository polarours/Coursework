# 007 · Stanford CS143 — 迷你编译器

- 课程 / Course: Stanford CS143 Compilers
- 官方 / Official: https://web.stanford.edu/class/cs143/
- 方向 / Area: 编译器 / Compilers
- 难度 / Difficulty: 硬核 / Advanced
- 预计耗时 / Estimated effort: 6–12 天 / 6–12 days
- 前置 / Prerequisites: Python、自动机与文法基础 / Python, automata and grammars
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

CS143 是把自动机、数据结构与系统串起来的综合大作业。本项目实现完整的前端→后端流水线（词法→语法→AST→代码生成→执行），让学生看清每一环如何衔接。
CS143 ties together automata theory, data structures, and systems. Our mini-compiler keeps the full front-end→back-end pipeline.

> **English:** A compiler is the ultimate "build something that builds something" project — exceptionally rewarding for students who want to understand how programs really work.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/compiler.py`：独立编写的迷你编译器，含词法、递归下降语法分析、AST、栈式虚拟机代码生成与执行。运行 / Run:

```bash
python3 tests/test_compiler.py
```

## 实测结果 / Verified results

- 词法 67 token，代码生成 34 指令（真实输出）
- 综合程序输出 [25, 0, 1, 2, 1]；阶乘 5! = 120
- 词法/语法错误正确抛出；开发中修复 3 个真实 bug（分号/token 类型/赋值符），详见 05
