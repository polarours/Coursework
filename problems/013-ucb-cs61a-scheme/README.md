# 013 · UC Berkeley CS61A — Scheme 解释器

- 课程 / Course: UC Berkeley CS61A Structure and Interpretation of Computer Programs
- 官方 / Official: https://cs61a.org/
- 方向 / Area: 编程语言 / Programming languages
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 5–10 天 / 5–10 days
- 前置 / Prerequisites: Python、函数式编程基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

写解释器是理解求值、环境、闭包的最佳方式；支持 quote/define/lambda/if 与列表原语。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/scheme.py（词法 + 递归下降 + 环境链 + 闭包）`。运行 / Run:

```bash
python3 tests/test_scheme.py
```

## 实测结果 / Verified results

- 递归阶乘 120；闭包 make-adder 记住 x（add5(3)=8）。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
