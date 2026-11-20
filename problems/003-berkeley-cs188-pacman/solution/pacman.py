"""CS188 Pacman 核心 AI 算法的教学版实现（独立于官方框架编写）。

包含：网格世界、A* 搜索、Minimax + alpha-beta 对抗搜索、MDP 值迭代、Q-learning。
"""

from __future__ import annotations
import heapq
import random
from dataclasses import dataclass
from typing import Callable


# ---------------------------------------------------------------- 网格世界

@dataclass(frozen=True)
class State:
    pacman: tuple[int, int]
    ghost: tuple[int, int]
    food: tuple[tuple[int, int], ...]
    steps: int = 0

    def key(self):  # 用于搜索去重（不含 steps）
        return (self.pacman, self.ghost, self.food)


class GridWorld:
    """小型网格世界：Pacman 吃豆子，Ghost 追捕。"""

    def __init__(self, width: int, height: int, walls: set[tuple[int, int]]):
        self.width = width
        self.height = height
        self.walls = walls

    def neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = pos
        out = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            np = (x + dx, y + dy)
            if 0 <= np[0] < self.width and 0 <= np[1] < self.height and np not in self.walls:
                out.append(np)
        return out

    def display(self, state: State) -> str:
        rows = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                p = (x, y)
                if p in self.walls:
                    row += "#"
                elif p == state.pacman:
                    row += "P"
                elif p == state.ghost:
                    row += "G"
                elif p in state.food:
                    row += "."
                else:
                    row += " "
            rows.append(row)
        return "\n".join(rows)


# ---------------------------------------------------------------- 1. A* 搜索

def astar(grid: GridWorld, start: tuple[int, int], goals: set[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """A* 搜索最近的食物，返回路径（含起点，不含终点可选）。"""
    def heuristic(p):
        return min((abs(p[0]-g[0]) + abs(p[1]-g[1]) for g in goals), default=0)

    frontier = [(heuristic(start), 0, start)]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    cost = {start: 0}
    while frontier:
        _, g, cur = heapq.heappop(frontier)
        if cur in goals:
            path = []
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            return path[::-1]
        for nb in grid.neighbors(cur):
            ng = g + 1
            if ng < cost.get(nb, float('inf')):
                cost[nb] = ng
                came_from[nb] = cur
                heapq.heappush(frontier, (ng + heuristic(nb), ng, nb))
    return None


# ---------------------------------------------------------------- 2. Minimax + alpha-beta

def minimax(state: State, grid: GridWorld, depth: int, agent: int,
            alpha: float, beta: float) -> float:
    """对抗搜索：Pacman(agent=0) 最大化，Ghost(agent=1) 最小化。"""
    if depth == 0 or not state.food or state.pacman == state.ghost:
        return evaluate(state)
    if agent == 0:
        value = float('-inf')
        for nb in grid.neighbors(state.pacman):
            ns = State(nb, state.ghost, tuple(f for f in state.food if f != nb), state.steps + 1)
            value = max(value, minimax(ns, grid, depth - 1, 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta 剪枝
        return value
    else:
        value = float('inf')
        for nb in grid.neighbors(state.ghost):
            ns = State(state.pacman, nb, state.food, state.steps + 1)
            value = min(value, minimax(ns, grid, depth - 1, 0, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break  # alpha 剪枝
        return value


def evaluate(state: State) -> float:
    """评估函数：离食物越近越好，离 ghost 越远越好。"""
    if state.pacman == state.ghost:
        return -1000.0
    if not state.food:
        return 1000.0
    d_food = min(abs(state.pacman[0]-f[0]) + abs(state.pacman[1]-f[1]) for f in state.food)
    d_ghost = abs(state.pacman[0]-state.ghost[0]) + abs(state.pacman[1]-state.ghost[1])
    return -d_food + 0.5 * d_ghost


# ---------------------------------------------------------------- 3. MDP 值迭代

def value_iteration(grid: GridWorld, terminals: set[tuple[int, int]],
                    gamma: float = 0.9, theta: float = 1e-6) -> dict[tuple[int, int], float]:
    """在网格上求值迭代：每个格子到终点的折扣奖励。"""
    positions = [(x, y) for x in range(grid.width) for y in range(grid.height)
                 if (x, y) not in grid.walls]
    V = {p: (10.0 if p in terminals else 0.0) for p in positions}
    while True:
        delta = 0.0
        for p in positions:
            if p in terminals:
                continue
            best = float('-inf')
            for nb in grid.neighbors(p):
                reward = 10.0 if nb in terminals else 0.0
                best = max(best, reward + gamma * V[nb])
            if best > float('-inf'):
                delta = max(delta, abs(best - V[p]))
                V[p] = best
        if delta < theta:
            break
    return V


# ---------------------------------------------------------------- 4. Q-learning

def q_learning(grid: GridWorld, goal: tuple[int, int], episodes: int = 300,
               alpha: float = 0.2, gamma: float = 0.9, epsilon: float = 0.1):
    """表格型 Q-learning：在网格中学习到目标的策略。"""
    Q: dict[tuple, float] = {}
    start = (0, 0)

    def q(s, a):
        return Q.get((s, a), 0.0)

    rng = random.Random(42)
    total_steps = []
    for ep in range(episodes):
        s = start
        steps = 0
        while s != goal and steps < 200:
            actions = grid.neighbors(s)
            if not actions:
                break
            if rng.random() < epsilon:
                a = rng.choice(actions)
            else:
                a = max(actions, key=lambda x: q(s, x))
            ns = a
            reward = 10.0 if ns == goal else -0.1
            future = max((q(ns, x) for x in grid.neighbors(ns)), default=0.0)
            Q[(s, a)] = q(s, a) + alpha * (reward + gamma * future - q(s, a))
            s = ns
            steps += 1
        total_steps.append(steps)
    return Q, total_steps
