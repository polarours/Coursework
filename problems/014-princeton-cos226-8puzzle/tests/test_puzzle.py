"""8-Puzzle 测试：可解性、最优解、不可解检测。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from puzzle import solve, solvable, manhattan, display, GOAL


def main():
    assert manhattan(GOAL) == 0
    assert solvable(GOAL)
    print(f"[puzzle] goal:\n{display(GOAL)}")

    # 距离目标 1 步的局面（空格右移即可复原）
    s1 = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    r1 = solve(s1)
    print(f"[puzzle] start 1-move: {r1}")
    assert r1 is not None and len(r1[0]) == 1

    # 中等难度局面：从目标状态确定性地走若干步（保证可解）
    import random
    rng = random.Random(7)
    s2 = GOAL
    for _ in range(30):
        nxts = list(__import__("puzzle").neighbors(s2))
        s2 = rng.choice(nxts)
    r2 = solve(s2)
    print(f"[puzzle] scrambled start h={manhattan(s2)}: moves={len(r2[0])}, expanded={r2[1]}")
    assert r2 is not None

    # 不可解局面（逆序数奇数）
    s3 = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    print(f"[puzzle] {s3} solvable={solvable(s3)} solve -> {solve(s3)}")
    assert not solvable(s3) and solve(s3) is None

    # A* 最优性：从目标走 4 步得到的局面，解长度 <= 4
    s4 = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    r4 = solve(s4)
    print(f"[puzzle] 4-step scramble -> solution length {len(r4[0])}")
    assert len(r4[0]) <= 4

    print("--- PASS: test_puzzle")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
