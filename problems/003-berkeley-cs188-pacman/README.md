# 003 · UC Berkeley CS188 — Pacman 项目
- 来源高校 / University profile: [UC Berkeley](https://polarours.github.io/Coursework/universities/berkeley.html)

- 课程 / Course: UC Berkeley CS188 Artificial Intelligence
- 参考 / Reference: https://github.com/BigEggStudy/UC-Berkeley-CS-188-Artificial-Intelligence
- 方向 / Area: 人工智能 / Artificial intelligence
- 难度 / Difficulty: 进阶 / Intermediate–advanced
- 预计耗时 / Estimated effort: 4–8 天 / 4–8 days
- 前置 / Prerequisites: Python、基础概率 / Python, basic probability
- 状态 / Status: ✅ 已完成 / Completed

## 为什么收录 / Why included

Pacman 用同一个游戏场景串起搜索、对抗搜索、MDP、强化学习和贝叶斯推断：题目有趣，但背后是 AI 的核心算法体系。
Pacman uses one game to carry search, adversarial search, MDPs, reinforcement learning, and Bayesian inference — an engaging wrapper around core AI algorithms.

> **English:** The project is pedagogically excellent because each project builds on the previous one while keeping the same concrete, visual domain.

## 解析章节 / Walkthrough chapters

- [01 题目解读](01-题目解读.md) · [02 设计思路](02-设计思路.md) · [03 逐步实现](03-逐步实现.md)
- [04 正确性与复杂度](04-正确性与复杂度.md) · [05 调试与测试](05-调试与测试.md)
- [06 踩坑清单](06-踩坑清单.md) · [07 延伸练习](07-延伸练习.md)

## 参考实现 / Reference implementation

`solution/pacman.py`：独立编写的 Python 实现，含共享网格世界与四种算法（A*、Minimax+α-β、值迭代、Q-learning）。运行 / Run:

```bash
python3 tests/test_pacman.py
```

## 实测结果 / Verified results

- 5 项测试全部通过 / 5 tests pass
- Q-learning：平均步数从 25.6（前 10 轮）降到 9.6（后 10 轮）/ measurable learning curve
- A* 绕墙找到 10 步最短路径；Pacman 13 步吃光 3 颗豆子（终局地图见 05）
- 详见 [05-调试与测试.md](05-调试与测试.md) 的真实轨迹与输出
