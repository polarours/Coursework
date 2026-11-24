# 026 · UCI ICS46 HW6 — BST 与 AVL 树（真实高校作业）
- 来源高校 / University profile: [UC Irvine](https://polarours.github.io/Coursework/universities/uci.html)

- 学校 / University: UC Irvine
- 课程 / Course: ICS 46 Data Structures
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/klefstad-teaching/ICS-46-HW6
- 方向 / Area: C++ / 二叉搜索树与自平衡树
- 状态 / Status: ✅ submodule 引用 + 参考实现 5/5 测试通过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

官方教学仓库：实现 BSTree 与 AVLTree（继承抽象基类 BST），starter 的三个 `.cpp` 全空、接口完整。官方本地 gtest 只有占位用例（真实评测在 Gradescope），因此本项目按 `bst.h` 接口语义自写测试，README 如实注明。

The official teaching repo: implement BSTree and AVLTree over an abstract BST base. The local gtest is a placeholder (real grading on Gradescope), so our tests are self-written against the bst.h interface.

## 运行 / Run

```bash
bash tests/run.sh   # 5 tests + 官方 main.cpp 的 measure demo
```

## 实测结果 / Verified results

- BST 顺序插入 1024 键退化成链（高度=1024）；同样数据 AVL 高度=11 —— 教科书级对比
- 官方 demo 真实输出：sorted.txt 下 **BSTree 高度 26 vs AVLTree 高度 5**
- 开发中修复两个真实错误：`Node` 是全局类型不能写成 `BSTree::Node`；static 成员函数不能访问非静态 `count`（计数移到公共接口维护）

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
