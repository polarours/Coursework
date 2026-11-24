# 009 · Stanford CS155 — 密码学构件
- 来源高校 / University profile: [Stanford University](https://polarours.github.io/Coursework/universities/stanford.html)

- 课程 / Course: Stanford CS155 Cryptography and Security
- 官方 / Official: https://crypto.stanford.edu/cs155/
- 方向 / Area: 密码学与安全 / Cryptography
- 难度 / Difficulty: 进阶 / Intermediate
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python、数论基础
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Miller-Rabin、RSA、Merkle 树——HTTPS 与区块链背后的原语，亲手实现才能理解数学。

> **English:** A carefully chosen capstone that builds transferable reasoning skills through hands-on implementation.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/crypto.py（Miller-Rabin + RSA + Merkle）`。运行 / Run:

```bash
python3 tests/test_crypto.py
```

## 实测结果 / Verified results

- RSA 加解密往返成功；签名验证正确/篡改拒绝；Merkle 根检测篡改。
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实输出
