# 011 · Stanford CS231n — 两层神经网络

- 课程 / Course: Stanford CS231n Convolutional Neural Networks
- 官方 / Official: https://cs231n.github.io/
- 参考仓库 / Repo: https://github.com/cs231n/cs231n.github.io
- 方向 / Area: 机器学习 / Machine learning
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python、线性代数、微积分基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

无 numpy、无 autograd——前向/反向传播全部手写，梯度检验证明实现正确。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/nn.py（手写矩阵运算 + 前向/反向 + SGD）`。运行 / Run:

```bash
python3 tests/test_nn.py
```

## 实测结果 / Verified results

- 600 轮训练 loss 1.0865→0.1248，准确率 0.339→0.967。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
