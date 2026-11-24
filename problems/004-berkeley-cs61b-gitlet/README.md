# 004 · UC Berkeley CS61B — Gitlet
- 来源高校 / University profile: [UC Berkeley](https://polarours.github.io/Coursework/universities/berkeley.html)

- 课程 / Course: UC Berkeley CS61B Data Structures
- 课程组织 / Course org: https://github.com/Berkeley-CS61B
- 方向 / Area: 数据结构 / Data structures
- 难度 / Difficulty: 进阶 / Intermediate–advanced
- 预计耗时 / Estimated effort: 5–10 天 / 5–10 days
- 前置 / Prerequisites: Java/Python、哈希基础 / Java/Python, hashing basics
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Gitlet 让学生从零实现一个简化版 Git：内容寻址存储、提交图、暂存区。概念简单但工程细节多，是锻炼"把抽象概念落地成持久数据结构"的极佳题目。
Gitlet asks students to build a simplified Git from scratch: content-addressable storage, commit graphs, and a staging area. Simple concepts, but rich engineering detail.

> **English:** Gitlet teaches that version control is just a handful of data structures — snapshots, hashes, and parent pointers — assembled carefully.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/gitlet.py`：独立编写的 Python 教学版，实现 init/add/commit/log/status/checkout。运行 / Run:

```bash
python3 tests/test_gitlet.py
```

## 实测结果 / Verified results

- 3 次提交（initial + 2），log 按 newest-first 显示 / 3 commits, log newest-first
- checkout 把改坏的文件恢复为 HEAD 版本（`'hello gitlet\n'`）/ restore verified
- 记录并修复了一个真实的"uid 哈希不一致"bug / a real hash-consistency bug found and fixed
- 详见 [05-调试与测试.md](05-调试与测试.md)
