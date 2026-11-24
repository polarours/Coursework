# 012 · UC Berkeley CS61C — Cache 模拟器
- 来源高校 / University profile: [UC Berkeley](https://polarours.github.io/Coursework/universities/berkeley.html)

- 课程 / Course: UC Berkeley CS61C Machine Structures
- 官方 / Official: https://www.cs.berkeley.edu/~cs61c/
- 方向 / Area: 计算机组成 / Computer architecture
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 3–6 天 / 3–6 days
- 前置 / Prerequisites: Python、存储器层次基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

地址划分、直接映射与组相联、LRU 替换、写回策略——把存储器层次变成可观察的统计。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/cache_sim.py（可配置组相联 + LRU + 写回）`。运行 / Run:

```bash
python3 tests/test_cache.py
```

## 实测结果 / Verified results

- 直接映射冲突全 miss，2 路组相联命中 2 次；顺序访问命中率 0.5 > 跨步 0.0。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
