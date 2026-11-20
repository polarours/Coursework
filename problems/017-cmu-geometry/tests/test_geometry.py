"""计算几何测试：叉积、线段相交、凸包、点在多边形内。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from geometry import cross, segments_intersect, convex_hull, point_in_polygon


def main():
    assert cross((0,0),(1,0),(0,1)) == 1   # 逆时针为正
    assert cross((0,0),(0,1),(1,0)) == -1
    print("[geometry] cross products ok")

    assert segments_intersect((0,0),(2,2),(0,2),(2,0))   # 十字交叉
    assert not segments_intersect((0,0),(1,0),(2,0),(3,0))  # 共线不相交
    assert segments_intersect((0,0),(2,0),(1,0),(3,0))   # 共线重叠
    print("[geometry] segment intersection ok")

    pts = [(0,0),(1,0),(1,1),(0,1),(0.5,0.5),(2,0.5)]
    hull = convex_hull(pts)
    print(f"[geometry] hull of {len(pts)} points = {hull}")
    assert (0.5,0.5) not in hull, "内部点不应在凸包上"
    assert len(hull) == 4 or len(hull) == 5

    square = [(0,0),(2,0),(2,2),(0,2)]
    print(f"[geometry] (1,1) in square: {point_in_polygon((1,1), square)}")
    print(f"[geometry] (3,1) in square: {point_in_polygon((3,1), square)}")
    assert point_in_polygon((1,1), square)
    assert not point_in_polygon((3,1), square)

    print("--- PASS: test_geometry")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
