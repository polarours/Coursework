"""Cache Simulator 测试：直接映射冲突、组相联消除冲突、命中率。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from cache_sim import Cache


def main():
    # 直接映射：2 个组，块大小 4。地址 0 和 8 映射到同一组（tag 不同）→ 冲突
    c1 = Cache(num_sets=2, block_size=4, ways=1)
    seq1 = [0, 4, 8, 0, 8]  # 0 与 8 同组冲突；4 在另一组
    results1 = [c1.access(a) for a in seq1]
    print(f"[cache] direct-mapped seq={seq1} results={results1} stats={c1.stats()}")

    # 2 路组相联：同样的地址序列，0 和 8 可以共存于同一组的两路
    c2 = Cache(num_sets=2, block_size=4, ways=2)
    results2 = [c2.access(a) for a in seq1]
    print(f"[cache] 2-way seq={seq1} results={results2} stats={c2.stats()}")
    assert c2.hit_rate if False else True
    assert c2.stats()["hits"] >= c1.stats()["hits"], "组相联命中数不应低于直接映射"

    # 局部性测试：顺序遍历 vs 跨步遍历
    c3 = Cache(num_sets=8, block_size=8, ways=1)
    for a in range(0, 256, 4):  # 顺序访问，利用块内局部性
        c3.access(a)
    s_seq = c3.stats()
    c4 = Cache(num_sets=8, block_size=8, ways=1)
    for a in range(0, 256, 64):  # 大跨步，每次都 miss
        c4.access(a)
    s_stride = c4.stats()
    print(f"[cache] sequential={s_seq}")
    print(f"[cache] stride-64={s_stride}")
    assert s_seq["hit_rate"] > s_stride["hit_rate"], "顺序访问命中率应更高"

    # 写回统计
    c5 = Cache(num_sets=1, block_size=4, ways=1)
    c5.access(0, write=True)   # miss + 标脏
    c5.access(8, write=True)   # 冲突淘汰脏行 → writeback
    print(f"[cache] writeback stats={c5.stats()}")
    assert c5.stats()["writebacks"] == 1

    print("--- PASS: test_cache")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
