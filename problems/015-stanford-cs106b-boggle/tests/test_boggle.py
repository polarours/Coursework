"""Boggle 测试：回溯穷举、Trie 剪枝、对角相邻。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from boggle import Boggle, build_trie


def main():
    # 2x2 网格：A B / C D，词表含 ab, cd, abd(不可达), abcd(不可达), ba(反向不可达)
    board = [["A", "B"], ["C", "D"]]
    words = ["ab", "cd", "ba", "abc", "bcd", "abcd", "x"]
    got = Boggle(board, words).solve()
    print(f"[boggle] 2x2 found={sorted(got)}")
    # 2x2 网格完全连通（含对角），任何长度<=4 的路径都可能：
    # ab 右邻、cd 下邻、abc(a->b->c 对角)、abcd、ba、bcd 全部可达
    assert "ab" in got and "cd" in got and "abcd" in got
    assert "x" not in got  # 词典里有 x 但网格无此字母 → Trie 剪枝
    assert "xx" not in got  # 不存在的词
    assert len(got) == 6, f"expected all 6 reachable words, got {sorted(got)}"

    # Trie 前缀剪枝验证
    trie = build_trie(["cat", "car", "dog"])
    assert "c" in trie.children and "d" in trie.children
    assert "z" not in trie.children
    print("[boggle] trie structure ok")

    # 3x3 经典：验证对角相邻
    b3 = [["A","B","C"],["D","E","F"],["G","H","I"]]
    got3 = Boggle(b3, ["aei", "aeg", "ieg", "abc", "adg"]).solve()
    print(f"[boggle] 3x3 found={sorted(got3)}")
    assert "aei" in got3   # 对角链 (0,0)->(1,1)->(2,2)

    print("--- PASS: test_boggle")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
