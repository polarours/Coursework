# 027 · CCNY CSC212 Lab 07 — 回溯三题（真实高校作业）

- 学校 / University: City College of New York (CUNY)
- 课程 / Course: CSC 212 Data Structures
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/uricsc/212-Deliverables（教师课程仓库，本题为其中 Lab 07）
- 方向 / Area: C++ / 递归回溯
- 状态 / Status: ✅ submodule 引用 + 参考实现全部测试通过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

教师仓库（uricsc）中的回溯实验：N-Queens、Sudoku、Sujiko 三个经典问题，scaffolding 给出类接口与数据文件，`solve` 留空由学生实现。三题覆盖回溯的三个难度梯度。

The instructor's course repo: three classic backtracking problems (N-Queens, Sudoku, Sujiko) with class scaffolding and data files; the solve functions are left empty.

## 运行 / Run

```bash
bash tests/run.sh
```

## 实测结果 / Verified results

- 8-Queens 求解成功；4-Queens 有解、2/3-Queens 正确判无解
- Sudoku easy/medium/hard 三档谜题全部解出
- Sujiko 谜题解出（含剪枝：填满的宫校验目标和）

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
