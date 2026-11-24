# 008 · CMU 15-445 — Buffer Pool Manager
- 来源高校 / University profile: [Carnegie Mellon University](https://polarours.github.io/Coursework/universities/cmu.html)

- 课程 / Course: CMU 15-445/645 Database Systems
- 官方 / Official: https://15445.courses.cs.cmu.edu/
- 参考仓库 / Repo: https://github.com/cmu-db/bustub
- 方向 / Area: 数据库 / Database systems
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python、操作系统基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

LRU 淘汰、pin/unpin、脏页写回——数据库存储引擎的核心；真实踩过动态属性补丁的坑。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/buffer_pool.py（DiskManager + BufferPoolManager）`。运行 / Run:

```bash
python3 tests/test_buffer_pool.py
```

## 实测结果 / Verified results

- 3 页框 LRU 淘汰正确；pin 住的页经历 6 次分配仍存活；flush 后磁盘数据一致。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
