# 030 · UMD CMSC132 Project1 — SubmitServer（真实高校作业，Java）

- 学校 / University: University of Maryland
- 课程 / Course: CMSC 132 Object-Oriented Programming II
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/a-blender/cmsc132（学生提交仓库，含 Larry Herman 官方 PublicTests）
- 方向 / Area: Java / 链表、类设计
- 状态 / Status: ✅ submodule 引用 + 官方 15 tests + 边界 4 tests 全过（JUnit 4）

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 原题面全文副本（资源图在 `resources/`）/ original assignment text

## 为什么收录 / Why included

UMD 官方以**测试即规格**著称：PublicTests.java 就是需求文档（统计提交数、best 分数、satisfactory 判定等 7 个方法语义全在测试里）。upstream 学生实现（Anna Blendermann）经我们实测通过全部官方测试，可直接作为参考对照。

UMD's official "tests as spec" style: PublicTests.java defines the required semantics. The upstream student implementation passes all 15 official tests (verified here).

## 运行 / Run

```bash
bash tests/run.sh   # 官方 PublicTests + 边界补充
```

## 实测结果 / Verified results

- 官方 PublicTests 15/15 通过；边界补充 4/4 通过
- 边界语义实测记录（官方测试未覆盖的分支）：`numSubmissions(null)` 返回 -1、非法分数（101/-1）静默忽略、`bestSubmissionNumber` 1-based
