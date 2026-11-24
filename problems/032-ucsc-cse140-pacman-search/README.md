# 032 · UCSC CSE140 p1 — Pacman 搜索大作业（真实高校作业，Python）
- 来源高校 / University profile: [UC Santa Cruz](https://polarours.github.io/Coursework/universities/ucsc.html)

- 学校 / University: UC Santa Cruz
- 课程 / Course: CSE 140 Artificial Intelligence（题面在 031 upstream 的 `p1/README.md`）
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/edulinq/pacai（pin 到 **v2.1.0**，题面指定的框架版本）
- 方向 / Area: Python / DFS、BFS、UCS、A*、Corners、Food、贪心与近似搜索
- 状态 / Status: ✅ 8 个待实现函数全部完成，9 用例全过（board↔problem 正确配对）

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

CSE140 p1（改编自 Berkeley CS188）要求实现 `pacai/student/singlesearch.py` 的 8 个函数：DFS/BFS/UCS/A* 四个搜索器、CornersProblem（状态设计 + 启发式）、FoodSearchProblem 启发式、ClosestDot 贪心 agent、AnyMarker 目标判定。框架 pacai v2.1.0 完全开源（MIT），starter 的 8 处 `NotImplementedError` 就是题面。

The full search assignment of CS188-style p1: eight solvers over the open-source pacai framework, with the starter's eight NotImplementedError stubs as the problem statement.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 运行 / Run

```bash
bash tests/run.sh   # 首次自建 venv（Pillow + edq-utils），构建副本树后跑 9 用例
```

## 实测结果 / Verified results

| 用例 | 结果 |
|---|---|
| maze-tiny × DFS/BFS/UCS/A* | 全 Win；**BFS/UCS/A* cost=8 一致最优，DFS=10** |
| corners-tiny + A* + corners_h | Win 28 步，展开 1050 节点（null 启发式 1449——启发式收益实测） |
| corners-medium + A* + corners_h | Win 106 步，845707 节点 5.24s |
| search-tiny + A* + food_h | Win 27 步 |
| search-medium ClosestDot / Approximate | Win 165 步（贪心策略） |

## 官方测试说明 / Note on official tests

官方评测在课程 autograder（`python -m autograder.run.submit`，不公开）；本地按题面语义自建用例矩阵，README 如实注明。upstream 框架原样保留，student 文件以**构建副本树**方式替换（不改 upstream 一个字节）。
