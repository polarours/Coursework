"""光线追踪测试：球交点、渲染 PPM、明暗效果。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from raytracer import Vec, Sphere, ray_sphere, render, to_ppm


def main():
    s = Sphere(Vec(0, 0, 3), 1.0, Vec(1, 0, 0))
    t = ray_sphere(Vec(0, 0, 0), Vec(0, 0, 1), s)
    print(f"[raytracer] ray-sphere hit t={t}")
    assert t is not None and abs(t - 2.0) < 1e-6
    assert ray_sphere(Vec(0, 0, 0), Vec(0, 1, 0), s) is None

    spheres = [s, Sphere(Vec(-1.2, 0.5, 4), 0.7, Vec(0, 1, 0))]
    img = render(32, 24, spheres, Vec(-2, 2, 1))
    ppm = to_ppm(img)
    lines = ppm.splitlines()
    print(f"[raytracer] PPM header={lines[:3]}")
    print(f"[raytracer] total lines={len(lines)} (expect {3 + 32*24})")
    assert lines[0] == "P3" and lines[1] == "32 24" and lines[2] == "255"
    assert len(lines) == 3 + 32 * 24
    center = img[12][16]
    corner = img[0][0]
    print(f"[raytracer] center pixel={center}, corner(background)={corner}")
    assert center.x > corner.x, "球体中心应比背景更亮（红色通道）"

    out = Path(__file__).resolve().parent / "output.ppm"
    out.write_text(ppm)
    print(f"[raytracer] wrote {out.name} ({len(ppm)} bytes)")
    print("--- PASS: test_raytracer")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
