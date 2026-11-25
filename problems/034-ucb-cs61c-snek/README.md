# 034 · UC Berkeley CS61C Proj1 — Snek（真实高校作业）
- 来源高校 / University profile: [UC Berkeley](https://polarours.github.io/Coursework/universities/berkeley.html)

- 学校 / University: UC Berkeley
- 课程 / Course: CS 61C Great Ideas in Computer Architecture
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/61c-teach/sp26-proj1-starter
- 方向 / Area: C / 结构体、指针、动态内存与游戏循环
- 状态 / Status: ✅ submodule 引用 + 21 集成测试 + 官方单元测试全过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 任务分解与规则摘录 / task breakdown and rules

## 为什么收录 / Why included

CS61C 的招牌项目：一个能跑的贪吃蛇引擎，全部用裸 C 写成，没有容器库、没有 GC。它把“结构体 + 指针 + `malloc`/`realloc` + 二维字符数组”这几件事压进一个具体目标里，而 21 组官方输入/参考输出让每一步都可判定。

The flagship CS61C project: a working snake engine in bare C — no containers, no GC. Structs, pointers, `malloc`/`realloc` and a ragged 2-D char board all serve one concrete goal, and 21 official input/reference pairs make every step checkable.

## 运行 / Run

```bash
bash tests/run.sh
```

## 实测结果 / Verified results

- 官方集成测试 **21/21 通过**（输入棋盘 → 一步之后的参考棋盘，逐字节比对）
- 官方 1708 行单元测试**全过**（Task 1–6 的每个函数）
- 10000 列的棋盘可正常加载与输出（`read_line` 的 `realloc` 路径）
- 默认棋盘 18 行 × 20 列，首步后 `d>D` 整体右移一格
- 实现过程中被官方单测纠正一处规格误读：`create_default_game` 必须**自带**那条蛇（`num_snakes = 1`），而不是留给 `initialize_snakes`

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
