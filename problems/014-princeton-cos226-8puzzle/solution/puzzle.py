"""Princeton COS 226 8-Puzzle 求解器教学版（A* + 曼哈顿距离；独立编写）。"""

from __future__ import annotations
import heapq


GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
POS = {v: divmod(i, 3) for i, v in enumerate(GOAL)}  # 值 -> (row, col) 目标位置


def manhattan(state: tuple[int, ...]) -> int:
    total = 0
    for i, v in enumerate(state):
        if v == 0:
            continue
        r, c = divmod(i, 3)
        gr, gc = POS[v]
        total += abs(r - gr) + abs(c - gc)
    return total


def solvable(state: tuple[int, ...]) -> bool:
    """逆序数奇偶性判定可解性。"""
    tiles = [x for x in state if x != 0]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles))
              if tiles[i] > tiles[j])
    return inv % 2 == 0


def neighbors(state: tuple[int, ...]):
    z = state.index(0)
    r, c = divmod(z, 3)
    for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nz = nr * 3 + nc
            lst = list(state)
            lst[z], lst[nz] = lst[nz], lst[z]
            yield tuple(lst)


class Node:
    def __init__(self, state, g, parent=None, move=""):
        self.state = state
        self.g = g
        self.f = g + manhattan(state)
        self.parent = parent
        self.move = move

    def __lt__(self, other):
        return self.f < other.f


def solve(start: tuple[int, ...]) -> tuple[list[str], int] | None:
    """A* 搜索；返回 (移动序列, 展开节点数)，无解返回 None。"""
    if not solvable(start):
        return None
    frontier = [Node(start, 0)]
    best_g = {start: 0}
    expanded = 0
    while frontier:
        node = heapq.heappop(frontier)
        expanded += 1
        if node.state == GOAL:
            moves = []
            while node.parent:
                moves.append(node.move)
                node = node.parent
            return moves[::-1], expanded
        for ns in neighbors(node.state):
            if ns in best_g and best_g[ns] <= node.g + 1:
                continue
            best_g[ns] = node.g + 1
            heapq.heappush(frontier, Node(ns, node.g + 1, node, "move"))
    return None


def display(state: tuple[int, ...]) -> str:
    return "\n".join(" ".join(str(x) if x else "_" for x in state[r*3:r*3+3])
                     for r in range(3))
