# CS Course Project Workbook / 计算机课程大作业精解库

> 把名校计算机课程里真正锻炼人的大作业拆透：题目背景、设计思路、逐步实现、调试过程、踩坑清单和延伸练习，全部可运行、可复现。
>
> Deep, runnable walkthroughs of outstanding CS course projects from top universities: background, design reasoning, step-by-step implementation, debugging records, pitfalls, and follow-up exercises.

## 📖 正式成书 / The Book

本项目已按主题编排成一部 Quarto 书籍，可构建为 HTML 网站与 PDF（93 页）：

```bash
bash scripts/build-book.sh all
# HTML → book/_site/（18 页）; PDF → book/_book/计算机课程大作业精解.pdf
```

书分四卷（系统基础 / 算法与数据结构 / 网络与分布式 / 智能系统），22 道题作为核心案例编入各章。详见 [book/README.md](book/README.md)。
The repo is now also a rendered Quarto book (four volumes, 21 case studies, HTML + PDF). See [book/README.md](book/README.md).

## 为什么做 / Why this exists

很多公开课的大作业质量极高，但公开资料往往只有零散的代码，缺少「为什么这样设计」「哪里会出错」「怎么验证自己写对了」的解释。本项目的定位是**学习解构**，而不是答案搬运：

Many top-tier course projects are excellent, but public material is usually scattered code without the reasoning: *why* a design was chosen, *where* implementations break, and *how* to verify correctness. This repo is a **study workbook**, not an answer dump:

- 每题一份完整解析，按「先自己做，再看解析」的顺序组织 / Each problem has a full walkthrough, organized so readers try first and read later.
- 参考实现带注释、可运行、有真实测试输出 / Reference implementations are commented, runnable, and backed by real test output.
- 每道题附我们自己出的变体练习 / Every problem includes follow-up exercises we designed ourselves.
- 只引用官方题目链接，转载与实现都注明来源 / We link to official problem statements and attribute every source.

## 收录标准 / Selection criteria

详见 [docs/selection-criteria.md](docs/selection-criteria.md)。核心四条 / The core four:

1. 来自知名高校 CS 课程，来源可查 / Traceable origin from a reputable CS course.
2. 期末/大作业级别，而非简单习题 / Capstone-scale, not a toy exercise.
3. 强调独立思考与动手实现 / Requires genuine reasoning and implementation.
4. 有清晰可验证的验收标准 / Has verifiable acceptance criteria.

## 题目清单 / Problem catalog

22 道原创精解 + 10 道真实高校作业（git submodule 引用原仓库）= 32 道：

| # | 题目 / Problem | 方向 / Area | 状态 |
|---|---|---|---|
| [001](problems/001-mit-6.824-raft/README.md) | MIT 6.824 Raft（共识算法） | 分布式系统 | ✅ |
| [002](problems/002-stanford-cs144-tcp/README.md) | Stanford CS144 TCP | 网络 | ✅ |
| [003](problems/003-berkeley-cs188-pacman/README.md) | UC Berkeley CS188 Pacman | 人工智能 | ✅ |
| [004](problems/004-berkeley-cs61b-gitlet/README.md) | UC Berkeley CS61B Gitlet | 数据结构 | ✅ |
| [005](problems/005-mit-6.1810-xv6/README.md) | MIT 6.1810 xv6 | 操作系统 | ✅ |
| [006](problems/006-cmu-csapp-malloc-lab/README.md) | CMU CSAPP Malloc Lab | 系统 | ✅ |
| [007](problems/007-stanford-cs143-compiler/README.md) | Stanford CS143 编译器 | 编译器 | ✅ |
| [008](problems/008-cmu-15445-buffer-pool/README.md) | CMU 15-445 Buffer Pool Manager | 数据库 | ✅ |
| [009](problems/009-stanford-cs155-crypto/README.md) | Stanford CS155 密码学构件 | 密码学与安全 | ✅ |
| [010](problems/010-stanford-cs248-raytracer/README.md) | Stanford CS248 光线追踪器 | 图形学 | ✅ |
| [011](problems/011-stanford-cs231n-neuralnet/README.md) | Stanford CS231n 两层神经网络 | 机器学习 | ✅ |
| [012](problems/012-ucb-cs61c-cache/README.md) | UC Berkeley CS61C Cache 模拟器 | 计算机组成 | ✅ |
| [013](problems/013-ucb-cs61a-scheme/README.md) | UC Berkeley CS61A Scheme 解释器 | 编程语言 | ✅ |
| [014](problems/014-princeton-cos226-8puzzle/README.md) | Princeton COS226 8-Puzzle | 算法 | ✅ |
| [015](problems/015-stanford-cs106b-boggle/README.md) | Stanford CS106B Boggle | 回溯搜索 | ✅ |
| [016](problems/016-mit-shell/README.md) | MIT 6.858 Shell 解析器 | 系统编程 | ✅ |
| [017](problems/017-cmu-geometry/README.md) | CMU 15-112 计算几何 | 几何 | ✅ |
| [018](problems/018-mit-6602-lru-cache/README.md) | MIT 6.006 LRU 缓存 | 数据结构 | ✅ |
| [019](problems/019-gatech-bloom-filter/README.md) | Georgia Tech 布隆过滤器 | 概率数据结构 | ✅ |
| [020](problems/020-cornell-enigma/README.md) | Cornell CS3110 Enigma | 密码学 | ✅ |
| [021](problems/021-stanford-kruskal/README.md) | Stanford 算法 Kruskal MST | 图算法 | ✅ |
| [022](problems/022-cs106l-scoped-handle/README.md) | CS106L 风格 ScopedHandle（作业包） | 现代 C++ / RAII | ✅ |
| [023](problems/023-amirkabir-ap1400-hw1/README.md) | Amirkabir AP1400-2 HW1（真实作业） | C++ / 线性代数 | ✅ |
| [024](problems/024-fordham-cisc2200-alist/README.md) | Fordham CISC2200 Lab3（真实作业） | C++ / 数据结构 | ✅ |
| [025](problems/025-uci-ecs36c-linkedlist/README.md) | UC Irvine ECS36C HW1（真实作业） | C++ / 链表栈队列 | ✅ |
| [026](problems/026-uci-ics46-bst-avl/README.md) | UCI ICS46 HW6（真实作业） | C++ / BST 与 AVL | ✅ |
| [027](problems/027-ccny-csc212-backtracking/README.md) | CCNY CSC212 Lab07（真实作业） | C++ / 回溯 | ✅ |
| [028](problems/028-clemson-cpsc2121-liststack-queue/README.md) | Clemson CPSC2121 Lab1（真实作业） | C++ / 链表栈队列 | ✅ |
| [029](problems/029-ucb-cs61b-deque61b/README.md) | UC Berkeley CS61B proj1a（真实作业） | Java / 泛型链表 | ✅ |
| [030](problems/030-umd-cmsc132-submitserver/README.md) | UMD CMSC132 Project1（真实作业） | Java / OOP | ✅ |
| [031](problems/031-ucsc-cse140-pacman-warmup/README.md) | UCSC CSE140 p0（真实作业） | Python / Pacman warmup | ✅ |
| [032](problems/032-ucsc-cse140-pacman-search/README.md) | UCSC CSE140 p1（真实作业） | Python / 搜索 | ✅ |

每题均含：题目卡片 + 7 章中英双语解析 + 可运行参考实现 + 真实测试输出 + 踩坑清单 + 自出延伸练习。
Each problem includes: a card + 7 bilingual chapters + runnable reference implementation + real test output + pitfalls + original exercises.

## 怎么读 / How to use

1. 打开题目的 `README.md`，确认前置知识与预计耗时 / Open the problem README; check prerequisites and estimated effort.
2. **先自己做一遍**，哪怕只完成设计 / **Attempt it yourself first**, even if only the design phase.
3. 按 `01 → 07` 顺序阅读解析，对照自己的实现 / Read `01 → 07` in order and compare with your own work.
4. 跑通 `solution/`，再挑战 `07-延伸练习.md` / Run `solution/`, then tackle the follow-up exercises.

## 目录结构 / Repository layout

```text
.
├── README.md                # 总览 / Overview
├── CONTRIBUTING.md          # 贡献指南 / Contribution guide
├── docs/                    # 规范、路线图、版权说明 / Standards, roadmap, licensing
├── templates/problem/       # 新题模板 / Template for new problems
└── problems/                # 逐题解析 / One directory per problem
    └── 001-xxx/
        ├── README.md        # 题目卡片 / Problem card
        ├── 01-题目解读.md ... 07-延伸练习.md
        ├── solution/        # 参考实现 / Reference implementation
        └── tests/           # 自测脚本 / Self-tests
```

## 边界与许可 / Scope and license

本项目内容为原创解析与实现，采用 [CC BY-NC-SA 4.0](LICENSE)。课程题目原文归各课程所有，我们只做引用与链接，**不转载题目全文、不提供可直接提交的作业答案**。详见 [docs/academic-integrity.md](docs/academic-integrity.md)。

All walkthroughs and implementations here are original and licensed under [CC BY-NC-SA 4.0](LICENSE). Problem statements belong to their respective courses; we reference and link them rather than reproducing them, and we do not provide copy-paste-ready homework submissions. See [docs/academic-integrity.md](docs/academic-integrity.md).

> 状态 / Status: ✅ 32 道全部完成：22 道原创精解 + 10 道真实高校作业（submodule 引用）/ All 32 complete: 22 original + 10 real university assignments via submodules.
