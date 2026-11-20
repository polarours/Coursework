# 简答题 / Short answer questions

> 先自己写答案，再看下面的参考答案。/ Answer first, then read the reference answers.

## Q1. 什么是 RAII？为什么本题的析构函数如此重要？
（学生在此作答 / your answer here）

## Q2. 为什么拷贝构造和拷贝赋值要 `= delete`？如果允许拷贝会发生什么？
（学生在此作答 / your answer here）

## Q3. 移动赋值中 `if (this != &other)` 和 `delete ptr_` 分别解决什么问题？
（学生在此作答 / your answer here）

---

## 参考答案 / Reference answers

**A1.** RAII（Resource Acquisition Is Initialization）把资源的生命周期绑定到对象的生命周期：构造时获取，析构时释放。本题析构函数 `delete ptr_` 保证即使发生异常或提前返回，资源也会被释放——这是 C++ 区别于手动 `free` 的核心机制。
*RAII ties a resource's lifetime to an object's lifetime: acquire in constructor, release in destructor. The destructor guarantees cleanup even on exceptions or early returns.*

**A2.** 若允许拷贝，两个 `ScopedHandle` 会指向同一资源，析构时双重释放（double free）。独占所有权语义要求资源只有一个所有者，因此必须禁止拷贝，只允许移动。
*Copying would create two owners of one resource and cause a double free. Exclusive ownership requires deleting copy operations.*

**A3.** `this != &other` 防止自移动赋值时先 `delete` 掉自己的资源再读取；`delete ptr_` 释放当前持有的旧资源，避免移动赋值时内存泄漏。这两点分别处理正确性与资源管理。
*The self-check prevents deleting the resource before reading it during self-move; `delete ptr_` frees the old resource to avoid leaks.*
