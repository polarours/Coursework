# 022 · Assignment: ScopedHandle（RAII 与移动语义）
- 来源高校 / University profile: [Stanford University](https://polarours.github.io/Coursework/universities/stanford.html)

> 原创题目，模仿 Stanford CS106L 作业的结构与教学意图（starter code + handout + 简答 + autograder）。
> 不是 CS106L 的原题或原代码，不复制其内容。

- 课程风格 / Course style: Stanford CS106L Standard C++ Programming
- 方向 / Area: 现代 C++ / RAII / Move semantics
- 难度 / Difficulty: 进阶 / Intermediate
- 前置 / Prerequisites: C++ 基础、指针与引用 / C++ basics, pointers and references
- 实现语言 / Language: C++20
- 状态 / Status: ✅ 含完整 starter + 参考实现 + autograder

## 背景 / Overview

标准库的 `std::unique_ptr` 用 RAII 管理动态资源：对象析构时自动释放资源，且只能有一个所有者。本题让你从零实现一个简化版 `ScopedHandle<T>`，理解 RAII、Rule of Five 与移动语义如何配合。

Implement a simplified `ScopedHandle<T>` — a teaching version of `std::unique_ptr` — to learn RAII, the Rule of Five, and move semantics.

## 文件 / Files

```text
starter/scoped_handle.h   # 你要完成的文件 / the file you implement
starter/main.cpp          # 演示程序 / demo program
tests/test_scoped_handle.cpp  # autograder（编译即可运行）
solution/scoped_handle.h  # 参考实现 / reference implementation
short_answer.md           # 概念题与参考答案 / conceptual questions + answers
```

## 你的任务 / Your tasks

### Part 0 — 读 starter code

打开 `starter/scoped_handle.h`，注意构造函数与析构函数的声明。`/ TODO /` 标记了你要填的地方。

### Part 1 — Rule of Five

实现：构造、析构、移动构造、移动赋值；**显式删除**拷贝构造与拷贝赋值。

```cpp
ScopedHandle(ScopedHandle&& other) noexcept;          // 移动构造
ScopedHandle& operator=(ScopedHandle&& other) noexcept; // 移动赋值
ScopedHandle(const ScopedHandle&) = delete;            // 禁止拷贝
```

### Part 2 — 访问接口

实现 `operator*`、`operator->`、`get()`、`reset()`、`release()`，语义对齐 `std::unique_ptr`。

### Part 3 — 简答题

回答 `short_answer.md` 中的三个概念题（先自己做，再看参考答案）。

## 编译与运行 / Build & run

```bash
# 用你的实现
g++ -std=c++20 -I starter tests/test_scoped_handle.cpp -o /tmp/test_handle && /tmp/test_handle

# 对照参考实现
g++ -std=c++20 -I solution tests/test_scoped_handle.cpp -o /tmp/test_handle_ref && /tmp/test_handle_ref
```

## 验收 / Acceptance

- [x] autograder 全部通过（构造/析构计数、移动后源为空、拷贝被禁用、reset/release 语义）
- [x] 参考实现同样通过 autograder
