"""Kruskal 与并查集测试：MST 权重、连通性、路径压缩。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from kruskal import UnionFind, kruskal


def main():
    uf = UnionFind(5)
    assert uf.union(0,1) and uf.union(1,2)
    assert not uf.union(0,2)  # 已连通
    print(f"[unionfind] components after unions: {uf.components} (expect 3)")
    assert uf.components == 3
    assert uf.find(0) == uf.find(2)
    assert uf.union(3,4) and uf.components == 2

    edges = [(0,1,4),(0,7,8),(1,2,8),(1,7,11),(2,3,7),(2,8,2),
             (2,5,4),(3,4,9),(3,5,14),(4,5,10),(5,6,2),(6,7,1),(6,8,6),(7,8,7)]
    mst, w = kruskal(9, edges)
    print(f"[kruskal] MST edges={mst}")
    print(f"[kruskal] total weight={w} (classic answer: 37)")
    assert w == 37 and len(mst) == 8

    # 不连通图：MST 边数 < n-1
    mst2, w2 = kruskal(4, [(0,1,1),(2,3,2)])
    print(f"[kruskal] disconnected graph: edges={mst2} weight={w2}")
    assert len(mst2) == 2

    print("--- PASS: test_kruskal")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
