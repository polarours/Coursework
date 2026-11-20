"""Stanford CS106B Boggle 回溯求解器教学版（独立编写）。

在 4x4 字母网格中找所有可由相邻（含对角）格子拼出、且在词典中的单词。
用 Trie 做前缀剪枝，避免无效递归。
"""

from __future__ import annotations


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


def build_trie(words) -> TrieNode:
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True
    return root


class Boggle:
    def __init__(self, board, words):
        self.board = [list(row) for row in board]
        self.rows, self.cols = len(self.board), len(self.board[0])
        self.root = build_trie(w.lower() for w in words)
        self.found: set[str] = set()
        self.visited: set[tuple[int, int]] = set()

    def solve(self) -> set[str]:
        for r in range(self.rows):
            for c in range(self.cols):
                self._dfs(r, c, self.root, "")
        return self.found

    def _dfs(self, r, c, node, prefix):
        if (r, c) in self.visited:
            return
        ch = self.board[r][c].lower()
        if ch not in node.children:
            return  # 前缀剪枝：词典无此前缀
        node = node.children[ch]
        prefix += ch
        if node.is_word:
            self.found.add(prefix)
        self.visited.add((r, c))
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self._dfs(nr, nc, node, prefix)
        self.visited.remove((r, c))
