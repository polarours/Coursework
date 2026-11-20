"""Stanford CS248 光线追踪教学版（纯 Python，输出 PPM；独立编写）。"""

from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass
class Vec:
    x: float; y: float; z: float
    def __add__(self, o): return Vec(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o): return Vec(self.x-o.x, self.y-o.y, self.z-o.z)
    def __mul__(self, t): return Vec(self.x*t, self.y*t, self.z*t)
    def dot(self, o): return self.x*o.x + self.y*o.y + self.z*o.z
    def length(self): return math.sqrt(self.dot(self))
    def norm(self):
        l = self.length()
        return Vec(self.x/l, self.y/l, self.z/l) if l else self


@dataclass
class Sphere:
    center: Vec
    radius: float
    color: Vec


def ray_sphere(origin: Vec, direction: Vec, s: Sphere) -> float | None:
    """求射线与球的最近正交点 t；无交点返回 None。"""
    oc = origin - s.center
    b = oc.dot(direction)
    c = oc.dot(oc) - s.radius * s.radius
    disc = b * b - c
    if disc < 0:
        return None
    sq = math.sqrt(disc)
    t1, t2 = -b - sq, -b + sq
    return t1 if t1 > 1e-4 else (t2 if t2 > 1e-4 else None)


def trace(origin: Vec, direction: Vec, spheres: list[Sphere], light: Vec) -> Vec:
    best_t, hit_color, normal = float("inf"), None, None
    for s in spheres:
        t = ray_sphere(origin, direction, s)
        if t is not None and t < best_t:
            best_t = t
            hit_color = s.color
            normal = ((origin + direction * t) - s.center).norm()
    if hit_color is None:
        return Vec(0.05, 0.05, 0.12)  # 背景色 / background
    ldir = (light - (origin + direction * best_t)).norm()
    diffuse = max(0.0, normal.dot(ldir)) if normal is not None else 0.0
    ambient = 0.15
    shade = ambient + 0.85 * diffuse
    return hit_color * shade


def render(width: int, height: int, spheres: list[Sphere], light: Vec) -> list[list[Vec]]:
    """渲染：透视相机，返回逐像素颜色。"""
    image = []
    for y in range(height):
        row = []
        for x in range(width):
            # 屏幕坐标映射到 [-1,1]，y 翻转
            sx = (x / width) * 2 - 1
            sy = 1 - (y / height) * 2
            direction = Vec(sx, sy, 1).norm()
            row.append(trace(Vec(0, 0, 0), direction, spheres, light))
        image.append(row)
    return image


def to_ppm(image: list[list[Vec]]) -> str:
    h, w = len(image), len(image[0])
    lines = [f"P3", f"{w} {h}", "255"]
    for row in image:
        for p in row:
            r = min(255, int(max(0, p.x) * 255))
            g = min(255, int(max(0, p.y) * 255))
            b = min(255, int(max(0, p.z) * 255))
            lines.append(f"{r} {g} {b}")
    return "\n".join(lines) + "\n"
