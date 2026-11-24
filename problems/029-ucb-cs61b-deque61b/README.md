# 029 · UC Berkeley CS61B proj1a+1b — Deque61B 完整大作业（真实高校作业，Java）
- 来源高校 / University profile: [UC Berkeley](https://polarours.github.io/Coursework/universities/berkeley.html)

- 学校 / University: UC Berkeley
- 课程 / Course: CS 61B Data Structures (sp25, Josh Hug)
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/Berkeley-CS61B/skeleton-sp25（官方教学组织）
- 方向 / Area: Java / 泛型链表与环形数组、Comparator、迭代器、Karplus-Strong 音频仿真
- 状态 / Status: ✅ 完整大作业：proj1a + proj1b 全部四件，15/15 测试通过 + 播放 demo 编译验证

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

官方课程组织公开的完整 skeleton 仓库（lab/hw/proj 全套）。本题覆盖 proj1a+1b 的**全部交付物**：

| 部分 | 交付物 | 状态 |
|---|---|---|
| proj1a | LinkedListDeque61B（环形哨兵链表 + 递归 get） | ✅ 6/6 |
| proj1b | ArrayDeque61B（环形数组 + 扩缩容 + iterator） | ✅ 6/6 |
| proj1b | Maximizer61B（自然序 + Comparator 双重载） | ✅ 同上 |
| proj1b | GuitarString（Karplus-Strong，缓冲=自己的 Deque） | ✅ 3/3 + demo 编译 |

The full deliverable set of proj1a+1b: linked deque, array deque, generic maximizer, and a Karplus-Strong guitar whose buffer is your own deque.

## 官方测试说明 / Note on official tests

upstream 的 `LinkedListDeque61BTest.java` 示例用例全部处于**注释状态**（CS61B 的 TDD 风格：鼓励学生自己写测试），且依赖课程私有测试库 jh61b/Google Truth（未随仓库公开）。本项目按 `Deque61B.java` 的接口 javadoc 自写测试并如实注明。

The upstream example tests are all commented out (CS61B's TDD style) and depend on the private jh61b library. Our tests are written against the interface javadoc.

## 官方测试说明 / Note on official tests

upstream 的官方测试用例全部处于**注释状态**（CS61B 的 TDD 风格），且依赖课程私有测试库 jh61b/Google Truth（未随仓库公开）。本项目按接口 javadoc 自写测试并如实注明。

## 运行 / Run

```bash
bash tests/run.sh   # 首次自动下载 JUnit5 console-standalone 与 algs4.jar
```

## 实测结果 / Verified results

- proj1a 6/6：哨兵环形结构 100 次增删、get/getRecursive 一致、越界 null
- proj1b 6/6：环形回绕、64 增 60 删触发缩容、Maximizer 双重载（含逆序 Comparator）
- GuitarString 3/3：构造容量 100、白噪声 [-0.5,0.5)、500 步能量衰减
- **作业暗设计实测**：官方 starter 两份文件互不编译（`Maximizer61BTest` 注释直接把 ArrayDeque61B 传入 `max(Iterable,...)` 而 `Deque61B` 不 extends Iterable）——学生须自己补 `iterator()`，见 03/06 章
