#!/usr/bin/env python3
"""Build the browser-based exercise bank from the repository's own solutions.

Expected values are produced by executing the checked-in reference
implementations, not typed by hand. If a solution changes, re-running this
script re-derives every answer.

Output: book/exercises/problems.json
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "exercises", "problems.json")

SPECS = [
    {
        "id": "014",
        "title": "8-Puzzle 可解性 / Solvability",
        "course": "Princeton COS226",
        "page": "../problems/014-princeton-cos226-8puzzle.qmd",
        "module": "problems/014-princeton-cos226-8puzzle/solution/puzzle.py",
        "starter": '''"""返回 8-Puzzle 局面是否可解。忽略空格(0)后数逆序对，奇数行宽按列数从上往下数。"""

def solvable(state: tuple[int, ...]) -> bool:
    # TODO: 实现可解性判定
    pass
''',
        "tests": [
            ("已经解开", None, "solvable((1, 2, 3, 4, 5, 6, 7, 8, 0))"),
            ("空格在左上角", None, "solvable((0, 1, 2, 3, 4, 5, 6, 7, 8))"),
            ("交换 7 和 8", None, "solvable((1, 2, 3, 4, 5, 6, 0, 8, 7))"),
            ("交换 1 和 2", None, "solvable((2, 1, 3, 4, 5, 6, 7, 8, 0))"),
            ("多步可解局面", None, "solvable((1, 2, 3, 4, 0, 5, 6, 7, 8))"),
            ("逆序较多的局面", None, "solvable((8, 1, 2, 0, 4, 3, 7, 6, 5))"),
        ],
    },
    {
        "id": "018",
        "title": "LRU 缓存 / LRU Cache",
        "course": "MIT 6.6602",
        "page": "../problems/018-mit-6602-lru-cache.qmd",
        "module": "problems/018-mit-6602-lru-cache/solution/lru.py",
        "starter": '''"""用哈希表 + 双向链表实现 O(1) 的 LRU 缓存。keys_mru_to_lru() 返回从最近使用到最久未用的键。"""

class Node:
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        # TODO: 初始化哈希表与哨兵节点
        pass

    def get(self, key):
        # TODO: 命中后移到最前，未命中返回 None
        pass

    def put(self, key, value):
        # TODO: 更新或插入，超出容量时淘汰最后一个
        pass

    def keys_mru_to_lru(self):
        # TODO: 按顺序返回键列表
        pass
''',
        "tests": [
            ("新缓存为空", "c = LRUCache(2)", "c.keys_mru_to_lru()"),
            ("put 后立即读出", "c = LRUCache(2); c.put(1, 10)", "c.get(1)"),
            ("get 更新最近性", "c = LRUCache(2); c.put(1, 10); c.put(2, 20); c.get(1)", "c.keys_mru_to_lru()"),
            ("超出容量淘汰 LRU", "c = LRUCache(2); c.put(1, 10); c.put(2, 20); c.get(1); c.put(3, 30)", "c.keys_mru_to_lru()"),
            ("淘汰后旧键不可达", "c = LRUCache(2); c.put(1, 10); c.put(2, 20); c.put(3, 30)", "(c.get(1), c.keys_mru_to_lru())"),
            ("覆盖已有键不增容量", "c = LRUCache(2); c.put(1, 10); c.put(2, 20); c.put(1, 99)", "(c.get(1), c.keys_mru_to_lru())"),
        ],
    },
    {
        "id": "021",
        "title": "Kruskal 最小生成树 / MST",
        "course": "Stanford 算法",
        "page": "../problems/021-stanford-kruskal.qmd",
        "module": "problems/021-stanford-kruskal/solution/kruskal.py",
        "starter": '''"""edges 是 (u, v, w) 列表，返回 (MST 边列表, 总权重)。用并查集判环。"""

class UnionFind:
    def __init__(self, n):
        # TODO
        pass

    def find(self, x):
        # TODO: 路径压缩
        pass

    def union(self, a, b):
        # TODO: 按秩合并，成功返回 True
        pass


def kruskal(n, edges):
    # TODO: 按权重升序逐条尝试
    pass
''',
        "tests": [
            ("三角形", None, "kruskal(3, [(0,1,1),(1,2,2),(0,2,3)])"),
            ("带更贵的替代边", None, "kruskal(4, [(0,1,1),(1,2,2),(2,3,3),(0,3,10)])"),
            ("输入未排序", None, "kruskal(4, [(0,3,10),(2,3,3),(0,1,1),(1,2,2)])"),
            ("等高边", None, "kruskal(4, [(0,1,1),(1,2,1),(2,3,1),(0,3,1)])"),
            ("只有一条边", None, "kruskal(2, [(0,1,7)])"),
            ("不连通图", None, "kruskal(4, [(0,1,1),(2,3,2)])"),
        ],
    },
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    bank = []
    for spec in SPECS:
        mod = load("ref_" + spec["id"], spec["module"])
        tests = []
        for name, setup, expr in spec["tests"]:
            ns = {k: v for k, v in vars(mod).items() if not k.startswith("__")}
            if setup:
                exec(setup, ns)
            value = repr(eval(expr, ns))
            tests.append({"name": name, "setup": setup or "", "expr": expr, "expect": value})
            print(f"{spec['id']} · {name}: {value}")
        bank.append({
            "id": spec["id"],
            "title": spec["title"],
            "course": spec["course"],
            "page": spec["page"],
            "starter": spec["starter"],
            "tests": tests,
        })

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(bank, fh, ensure_ascii=False, indent=2)
    print(f"wrote {OUT} ({len(bank)} problems, {sum(len(p['tests']) for p in bank)} tests)")


if __name__ == "__main__":
    main()
