# 028 · Clemson CPSC2121 Lab 1 — 链表栈与队列（真实高校作业）
- 来源高校 / University profile: [Clemson University](https://polarours.github.io/Coursework/universities/clemson.html)

- 学校 / University: Clemson University
- 课程 / Course: CPSC 2121 Data Structures and Algorithms
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/russellocean/CPSC2121（学生作业仓库，含完整实现与 13 个官方样例用例）
- 方向 / Area: C++ / 模板链表、栈与队列
- 状态 / Status: ✅ submodule 引用 + 官方 13 样例 + 5 项边界测试全过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

带官方样例测试（T1–T22）的完整作业：模板链表 List + 基于它的 ListStack / ListQueue。upstream 是学生提交版，其实现存在**5 处真实缺陷**，我们的 solution 是修复版——学生可对比 upstream 原版找 bug，本身就是练习。

A complete lab with official sample tests. The upstream student submission contains 5 real defects; our solution is the fixed version — diffing the two is itself an exercise.

## solution 相对 upstream 修复的缺陷 / Fixed defects

1. `ListStack::size()` 缺少 `return`（未定义行为）
2. `pop()` 空栈解引用空指针（应返回 `T()`）
3. `dequeue()` 空队列同上
4. `getFirst/getLast/getAt` 空表/越界崩溃（接口注释要求返回 `T()`）
5. `removeStart/removeEnd` 空表崩溃

## 运行 / Run

```bash
bash tests/run.sh   # 13 官方样例 + 边界测试
```

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
