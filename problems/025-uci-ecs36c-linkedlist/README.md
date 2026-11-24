# 025 · UC Irvine ECS36C HW1（真实高校作业）
- 来源高校 / University profile: [UC Irvine](https://polarours.github.io/Coursework/universities/uci.html)

- 学校 / University: University of California, Irvine
- 课程 / Course: ECS36C Fall 2023 — Templates, Linked Lists, Stacks, Queues
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/ecs36c-fq2023/hw1（pin `d490998`）
- 方向 / Area: 模板 + 链表/栈/队列 / Templates + LinkedList/Stack/Queue
- 状态 / Status: ✅ 原始作业以 submodule 引用 + 参考实现 9/9 测试通过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

真实的模板库作业：先实现 `LinkedList`，再用它实现 `Stack` 和 `Queue`（明确禁止用 `std::vector`）。上游评分用隐藏测试，仓库里公开了 4 个官方 LinkedList 用例；Stack/Queue 的官方测试是注释状态的 TODO。我们启用了官方示例并按接口语义补全了测试。

A genuine template-library assignment: implement `LinkedList` first, then build `Stack` and `Queue` on it (vectors explicitly disallowed). Grading uses hidden tests; we enabled the official examples and added semantic tests.

## 目录 / Layout

- `upstream/` — git submodule，指向原仓库 / submodule pointing at the original repo
- `solution/` — LinkedList/Stack/Queue 参考实现 / reference implementations
- `tests/` — 官方 4 用例（upstream 原样）+ Stack/Queue 激活测试 / tests

## 运行 / Run

```bash
bash tests/run.sh   # LinkedList 4 官方用例 + Stack/Queue 5 用例全部通过
```

## 实测结果 / Verified results

- upstream 官方 LinkedList 测试 4/4 通过（用原文件，未修改）
- Stack/Queue 测试 5/5 通过（官方注释示例启用 + 语义补全）
- 实现细节：Stack 的 vector 构造"末尾为栈顶"需要逆序建链；析构经 `clear()` 释放节点

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
