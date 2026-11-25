# 033 · Princeton COS 217 A1 — Decomment（真实高校作业）
- 来源高校 / University profile: [Princeton University](https://polarours.github.io/Coursework/universities/princeton.html)

- 学校 / University: Princeton University
- 课程 / Course: COS 217 Introduction to Programming Systems
- 上游仓库 / Upstream: `upstream/` git submodule → https://github.com/COS217/Decomment
- 方向 / Area: C / 有限状态机与词法边界
- 状态 / Status: ✅ submodule 引用 + 参考实现 38 金标准 + 74 官方输入全过

## 原始题面 / Original handout

- [source-handout.md](source-handout.md) — 题面要求摘录与原文链接 / assignment requirements and source link

## 为什么收录 / Why included

这道题只有 60 行有效代码，却是整门课最锋利的边界训练：注释不能出现在字符串里、转义的反斜杠会翻转引号的含义、多行注释必须保留行号、文件在注释中途结束要精确报出起始行。官方 starter 自带 74 个输入文件，把这套组合爆炸拆成可枚举的用例。

Sixty lines of code, but the sharpest boundary training in the course: comment markers inside literals, escapes that flip what a quote means, line numbers preserved across multi-line comments, and an exact line report when the file ends mid-comment. The starter ships 74 input files that enumerate the combinations.

## 运行 / Run

```bash
bash tests/run.sh
```

## 实测结果 / Verified results

- 规格表格中的例子全部逐字节复现：**38/38 金标准通过**
- 官方 74 个输入文件与独立 Python oracle 交叉验证：**74/74 一致**
- 实现过程中修掉一个真实缺陷：文件以孤立 `/` 结尾时该字符被吞掉（EOF 时状态仍停在“待定斜杠”）

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)
