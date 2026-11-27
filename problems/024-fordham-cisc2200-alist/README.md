# 024 · Fordham CISC2200 Lab3（真实高校作业）
- 来源高校 / University profile: [Fordham University](https://polarours.github.io/Coursework/universities/fordham.html)

- 学校 / University: Fordham University
- 课程 / Course: CISC2200 Spring 2024
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/CISC2200-Fall-24-Fordham/Lab3（pin `173c9f6`）
- 方向 / Area: 动态数组 + 深拷贝 / Dynamic array + deep copy
- 状态 / Status: ✅ 原始作业以 submodule 引用 + 参考实现 9/9 断言通过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

真实的 C++ 数据结构实验：实现 AList 的 5 个成员函数（addFirst、getFirst、removeFirst、拷贝构造、赋值运算符），doctest 验证。starter 里有一个真实笔误（`itemType` 大小写错误）——学生必须先修它才能编译。

A genuine DS lab: implement 5 AList members verified by doctest. The starter contains a real typo (`itemType`) students must fix to compile.

## 目录 / Layout

- `upstream/` — git submodule，指向原仓库 / submodule pointing at the original repo
- `solution/AList.h` — 参考实现 / reference implementation
- `tests/` — doctest 测试（含上游 `doctest.h` 单头文件副本，因网络隔离保留本地）/ doctest tests + local copy of the single-header doctest

## 实测结果 / Verified results

- 官方 doctest 全部用例通过（`make` 后直接运行，零外部依赖）
- 修掉 starter 自带的 `resize` 参数错误：原文用 `count * RFACTOR`，`count < maxCnt` 时扩容反而可能缩小容量
- 编译器在编译第一秒就报出 `AList<itemType>` 的大小写错误——这道题的隐藏考点是读懂编译器在说什么

## 运行 / Run

```bash
bash tests/run.sh   # doctest: 1 test case, 9 assertions passed
```

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
