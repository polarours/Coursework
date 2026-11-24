# 006 · CMU 15-213 — CSAPP Malloc Lab
- 来源高校 / University profile: [Carnegie Mellon University](https://polarours.github.io/Coursework/universities/cmu.html)

- 课程 / Course: CMU 15-213 Introduction to Computer Systems (CSAPP)
- 社区参考 / Community reference: https://github.com/kcxain/CSAPP-Lab
- 方向 / Area: 系统 / Systems
- 难度 / Difficulty: 硬核 / Advanced
- 预计耗时 / Estimated effort: 5–12 天 / 5–12 days
- 前置 / Prerequisites: C 语言、指针与内存布局 / C, pointers and memory layout
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

malloc lab 让系统方向学生直面指针算术、对齐与内存布局——一个 off-by-four 就能让整个程序段错误。这是锻炼底层调试能力的极佳题目。
Malloc lab forces systems students to confront pointer arithmetic, alignment, and memory layout — a single off-by-four segfaults everything.

> **English:** It is also a debugging bootcamp: we hit and fixed three real bugs (out-of-bounds, boundary coalescing, alignment) while building the reference implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/malloc.c`：独立编写的 C 实现——隐式空闲链表 + 边界标签 + 首次适应 + 分割合并。运行 / Run:

```bash
bash tests/run.sh
```

## 实测结果 / Verified results

- gcc 16.2.1 编译通过（-Wall -Wextra 无警告）/ compiles clean
- 3 次 malloc 8 字节对齐、数据隔离；free 后空闲块 1→2→2→1（正确合并）
- 释放后首次适应复用最低地址块（d == a）
- 开发中用 gdb 定位并修复 3 个真实 bug，详见 [05-调试与测试.md](05-调试与测试.md)
