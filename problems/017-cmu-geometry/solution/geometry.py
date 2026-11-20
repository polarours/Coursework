"""CMU 15-112 风格计算几何教学版（独立编写）。

实现：叉积、线段相交判定、Andrew 单调链凸包、点在多边形内。
"""

from __future__ import annotations


def cross(o, a, b):
    """向量 oa × ob 的二维叉积。"""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def on_segment(a, b, p):
    return (min(a[0],b[0]) <= p[0] <= max(a[0],b[0]) and
            min(a[1],b[1]) <= p[1] <= max(a[1],b[1]))


def segments_intersect(a, b, c, d):
    """标准相交判定：跨立 + 共线特殊情况。"""
    c1, c2 = cross(a,b,c), cross(a,b,d)
    c3, c4 = cross(c,d,a), cross(c,d,b)
    if ((c1 > 0 and c2 < 0) or (c1 < 0 and c2 > 0)) and \
       ((c3 > 0 and c4 < 0) or (c3 < 0 and c4 > 0)):
        return True
    if c1 == 0 and on_segment(a,b,c): return True
    if c2 == 0 and on_segment(a,b,d): return True
    if c3 == 0 and on_segment(c,d,a): return True
    if c4 == 0 and on_segment(c,d,b): return True
    return False


def convex_hull(points):
    """Andrew 单调链：返回逆时针凸包顶点。"""
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def point_in_polygon(p, poly):
    """射线法：奇进偶出。"""
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        if ((a[1] > p[1]) != (b[1] > p[1])):
            xint = a[0] + (p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if p[0] < xint:
                inside = not inside
    return inside
