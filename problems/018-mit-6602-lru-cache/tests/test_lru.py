"""LRU Cache 测试：命中提升、淘汰顺序、O(1) 正确性。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from lru import LRUCache


def main():
    c = LRUCache(2)
    c.put(1, "a"); c.put(2, "b")
    print(f"[lru] after put 1,2: {c.keys_mru_to_lru()}")
    assert c.get(1) == "a"           # 命中，1 提升为 MRU
    print(f"[lru] after get(1): {c.keys_mru_to_lru()}")
    assert c.keys_mru_to_lru() == [1, 2]
    c.put(3, "c")                    # 容量满，淘汰 LRU=2
    print(f"[lru] after put(3): {c.keys_mru_to_lru()} evictions={c.evictions}")
    assert c.get(2) is None and c.get(3) == "c"
    assert c.evictions == 1

    c.put(3, "C")                    # 更新已存在
    assert c.get(3) == "C" and c.evictions == 1

    # 经典序列验证
    c2 = LRUCache(2)
    ops = [("put",1,1),("put",2,2),("get",1,None),("put",3,3),("get",2,None),("put",4,4),
           ("get",1,None),("get",3,None),("get",4,None)]
    hits = 0
    for op, k, v in ops:
        if op == "put": c2.put(k, v)
        else:
            r = c2.get(k); hits += (r is not None)
    # 经典序列推演：put1 [1] → put2 [2,1] → get1 命中 [1,2]
    # → put3 淘汰 2，[3,1]，evictions=1 → get2 未命中
    # → put4 淘汰 1，[4,3]，evictions=2 → get1 未命中，get3/get4 命中
    # 共命中 3 次、淘汰 2 次
    print(f"[lru] classic sequence hits={hits} (expected 3), evictions={c2.evictions}")
    assert hits == 3 and c2.evictions == 2

    print("--- PASS: test_lru")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
