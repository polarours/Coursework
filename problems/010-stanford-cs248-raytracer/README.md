# 010 · Stanford CS248 — 光线追踪器
- 来源高校 / University profile: [Stanford University](https://polarours.github.io/Coursework/universities/stanford.html)

- 课程 / Course: Stanford CS248 Computer Graphics
- 官方 / Official: https://graphics.stanford.edu/courses/cs248-2/
- 参考仓库 / Repo: https://github.com/stanford-cs248/Cardinal3D
- 方向 / Area: 计算机图形学 / Graphics
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python、线性代数基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

几十行向量数学生成真实图像；射线与球求交、Lambert 着色、PPM 输出。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/raytracer.py（Vec + 求交 + 着色 + PPM）`。运行 / Run:

```bash
python3 tests/test_raytracer.py
```

## 实测结果 / Verified results

- 求交 t=2.0 精确；32×24 PPM 格式正确；球心像素比背景亮。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
