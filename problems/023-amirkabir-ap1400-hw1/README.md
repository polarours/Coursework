# 023 · Amirkabir AP1400-2 HW1（真实高校作业）

- 学校 / University: Amirkabir University of Technology（伊朗）
- 课程 / Course: AP1400-2 Advanced Programming, Spring 2022
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/polarours/Coursework（pin `8afe8fd`）
- 方向 / Area: C++ 线性代数库 / Linear algebra library
- 状态 / Status: ✅ 原始作业以 submodule 引用 + 参考实现 24/24 测试通过

## 为什么收录 / Why included

一份**真实的大学作业仓库**：原始 handout、starter 骨架、4 张资源图、CMake + Dockerfile、24 个 gtest 测试（原文件中被 `/* */` 注释，学生需激活）。以 git submodule 引用原仓库，不复制其内容。

A genuine university assignment referenced as a git submodule: original handout, skeleton, resources, build system, and 24 gtest cases (commented out in the source repo).

## 目录 / Layout

- `upstream/` — git submodule，指向原仓库 / submodule pointing at the original repo
- `source-handout.md` — 原始作业说明的提取副本（便于离线阅读；图片在 `resources/`）/ extracted handout copy
- `resources/` — handout 引用的 4 张图 / handout figures
- `solution/` — 参考实现 / reference implementation
- `tests/` — 激活版测试 + 运行脚本 / activated tests + runner

## 运行 / Run

```bash
bash tests/run.sh   # 24 个 gtest 全部通过（需先 git submodule update --init）
```

## 实测结果 / Verified results

- 原始 24 个测试全部通过（C++17 编译：本机 gtest 1.18 要求；原作业为 C++14）
- 实现中修复 4 处真实语义细节：空矩阵行列式=1、`ero_sum` 方向（r1×c 加到 r2）、奇异矩阵抛 `logic_error`、`upper_triangular` 主元为零不用换行

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
