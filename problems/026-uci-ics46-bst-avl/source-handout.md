# 原始作业说明 / Original Assignment Handout

> 提取自 upstream 原仓库 `README.md`（保持原文）；中文导读见 `01-题目解读.md`。
> Extracted verbatim from the upstream repo; Chinese walkthrough in `01-题目解读.md`.

> 注：完整题面（评分细则）在课程 Google Sites 链接，仓库 README 只有入口；见 01 章。

---

# ICS 46: Homework 6

Welcome to ICS 46 Homework 6! You will be implementing a Binary Search Tre and an AVL Tree.

**Links**
- [Instructions](https://sites.google.com/view/ics-46-data-structures/homework-6)
- [HW0 Environment Setup](https://github.com/klefstad-teaching/ICS-46-HW0)

## Local GTests
To install GTests on your hub instances and enable local test development, run:
```sudo apt-get install -y libgtest-dev libgmock-dev```

## Submit to GradeScope

Each homework submission will follow the same general pattern and should always have the
following folder structure:

```bash
.
├── CMakeLists.txt
├── gtest
│   └── <CLASSNAME>_gtests.cpp
└── src
    ├── main.cpp
    ├── <CLASSNAME>.cpp
    └── <CLASSNAME>.h
```

All submissions are done on [Gradescope](https://www.gradescope.com/).

On GradeScope, go into your Account Settings, and link your GitHub account to Gradescope.

Then on the course Gradescope, go to the **Homework 6** assignment, press the Submit button, choose the GitHub option, and select your project and branch.
