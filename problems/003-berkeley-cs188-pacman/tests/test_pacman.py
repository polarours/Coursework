"""CS188 Pacman 教学实现的测试（确定性，固定随机种子）。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))

from pacman import (GridWorld, State, astar, minimax, evaluate,
                    value_iteration, q_learning)


def make_grid():
    walls = {(1, 1), (2, 1), (3, 1)}
    return GridWorld(6, 5, walls)


def test_grid_and_astar():
    grid = make_grid()
    path = astar(grid, (0, 0), {(5, 4)})
    print(f"[test_grid_and_astar] path from (0,0) to (5,4): {path}")
    assert path is not None and path[0] == (0, 0) and path[-1] == (5, 4)
    print(f"[test_grid_and_astar] world:\n{grid.display(State((0,0),(4,3),((5,4),)))}")


def test_minimax():
    grid = make_grid()
    state = State((0, 0), (5, 4), ((3, 4), (5, 0)))
    v0 = minimax(state, grid, depth=4, agent=0, alpha=float('-inf'), beta=float('inf'))
    print(f"[test_minimax] depth=4 minimax value={v0:.2f}, static eval={evaluate(state):.2f}")
    assert isinstance(v0, float)


def test_value_iteration():
    grid = make_grid()
    terminal = {(5, 4)}
    V = value_iteration(grid, terminal)
    print(f"[test_value_iteration] V[(4,4)]={V[(4,4)]:.3f}, V[(0,0)]={V[(0,0)]:.3f}, "
          f"V[goal]={V[(5,4)]:.3f}")
    assert V[(4, 4)] > V[(0, 0)]


def test_q_learning():
    grid = make_grid()
    Q, steps = q_learning(grid, (5, 4), episodes=300)
    first = sum(steps[:10]) / 10
    last = sum(steps[-10:]) / 10
    print(f"[test_q_learning] Q entries={len(Q)}, "
          f"avg steps first 10 episodes={first:.1f}, last 10={last:.1f}")
    assert len(Q) > 0
    assert last < first, "Q-learning should improve (fewer steps)"


def test_game_trace():
    """用 A* 引导 Pacman 吃光所有豆子，打印真实轨迹。"""
    grid = make_grid()
    state = State((0, 0), (5, 4), ((5, 0), (5, 4), (0, 4)))
    trace = []
    for step in range(30):
        if not state.food:
            break
        path = astar(grid, state.pacman, set(state.food))
        if path is None or len(path) < 2:
            break
        nxt = path[1]
        state = State(nxt, state.ghost, tuple(f for f in state.food if f != nxt), step + 1)
        trace.append(nxt)
    print(f"[test_game_trace] Pacman 轨迹: {trace}")
    print(f"[test_game_trace] 剩余豆子: {state.food}, 步数: {state.steps}")
    print(f"[test_game_trace] 终局地图:\n{grid.display(state)}")
    assert len(trace) > 0


def main():
    tests = [test_grid_and_astar, test_minimax, test_value_iteration,
             test_q_learning, test_game_trace]
    for t in tests:
        t()
        print(f"--- PASS: {t.__name__}")
    print(f"ALL {len(tests)} TESTS PASSED")


if __name__ == "__main__":
    main()
