# 031 · UCSC CSE140 p0 — CS188 风格 Pacman warmup（真实高校作业，Python）
- 来源高校 / University profile: [UC Santa Cruz](https://polarours.github.io/Coursework/universities/ucsc.html)

- 学校 / University: UC Santa Cruz
- 课程 / Course: CSE 140 Artificial Intelligence（作业改编自 Berkeley CS188 Pacman 项目）
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/ucsc-cse-140/cse140-assignments-public（课程官方仓库）
- 方向 / Area: Python / 基础建模与最优化
- 状态 / Status: ✅ submodule 引用 + 7/7 测试通过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

课程官方公开作业仓库，p0 是 Berkeley CS188 classic search 项目的 warmup：`buyLotsOfFruit`（价格表查表计算）与 `shopSmart`（遍历商店选最优价）。starter 标准的 `*** Your Code Here ***` 风格，期望输出写在 docstring 里，可机器验证。仓库还有 p1/p2（DFS 搜索等更深入的 Pacman 项目）留作后续。

The official public assignment repo; p0 is the CS188-style warmup (buyLotsOfFruit + shopSmart) with a standard "Your Code Here" starter and docstring-verified expected output.

## 运行 / Run

```bash
bash tests/run.sh
```

## 实测结果 / Verified results

- 7/7 通过：12.25 总价、缺货水果返回 None、两商店择优、两个 main 的 docstring 期望输出
- 发现一处真实不一致：docstring 写 "best shop is shop1."，而 `shop.py` 的 main 实际打印 "the best shop is shop1."——测试断言以实际代码为准并注释说明

## p1（搜索大作业）/ About p1

p1 已作为独立题目完成：见 **[032 · UCSC CSE140 p1 Pacman 搜索](../032-ucsc-cse140-pacman-search/README.md)**（pacai v2.1.0 submodule + 8 个函数全部实现，9 用例全过）。
