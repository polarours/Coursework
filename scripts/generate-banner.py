#!/usr/bin/env python3
"""Generate the project banner: a designed 'knowledge atlas' wordmark.

This is the visual front door of the README. It encodes the real structure
(32 problems, five volumes, 22 original + 10 real) but is drawn as artwork,
not as a diagram: layered glow, depth-of-field nodes, fine grid, and a
deliberate type hierarchy.

Light and dark variants are produced for GitHub's prefers-color-scheme.
No third-party dependencies.
"""

import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

# Palette
NAVY0 = "#0B1626"
NAVY1 = "#12233B"
NAVY2 = "#1B3352"
TEAL = "#3EE0C8"
TEAL_D = "#159F8C"
AMBER = "#F5BE5C"
AMBER_D = "#C98A22"
WHITE = "#F4F8FC"
MUTED = "#93A9C4"
GRID = "#294364"

DISPLAY = "'Avenir Next','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','JetBrains Mono',monospace"
CJK = "'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif"

W, H = 1200, 420


def t(x, y, s, size=16.0, fill=WHITE, family=DISPLAY, weight=400,
      anchor="start", spacing=0.0, opacity=1.0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{ls}{op}>'
            f'{s}</text>')


def defs():
    return f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{NAVY0}"/>
    <stop offset="0.55" stop-color="{NAVY1}"/>
    <stop offset="1" stop-color="#0E1E32"/>
  </linearGradient>
  <radialGradient id="tealGlow">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.30"/>
    <stop offset="0.5" stop-color="{TEAL}" stop-opacity="0.08"/>
    <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="amberGlow">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0.22"/>
    <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/>
    <stop offset="1" stop-color="{AMBER}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GRID}" stop-opacity="0.55"/>
    <stop offset="0.6" stop-color="{GRID}" stop-opacity="0.18"/>
    <stop offset="1" stop-color="{GRID}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="{GRID}" stroke-width="0.6" opacity="0.35"/>
    <circle cx="0" cy="0" r="1" fill="{GRID}" opacity="0.5"/>
  </pattern>
  <filter id="blur"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="softglow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>'''


def constellation():
    """The right-side atlas: five volume clusters, 32 problem nodes."""
    rng = random.Random(42)
    parts = []
    centers = [
        (735, 118, 0),   # I Systems
        (930, 96, 0),    # II Algorithms
        (1082, 150, 0),  # III Networks
        (790, 305, 0),   # IV Intelligence
        (1010, 312, 1),  # V Real assignments
    ]
    labels = ["SYSTEMS", "ALGORITHMS", "NETWORKS", "INTELLIGENCE", "REAL ASSIGNMENTS"]
    roman = ["I", "II", "III", "IV", "V"]

    # ambient glow behind the atlas
    parts.append(f'<ellipse cx="930" cy="205" rx="300" ry="200" fill="url(#tealGlow)"/>')
    parts.append(f'<ellipse cx="1010" cy="312" rx="105" ry="72" fill="url(#amberGlow)" opacity="0.7"/>')

    # constellation web: hub-to-hub connections
    hub_path = "M735 118 L930 96 L1082 150 L1010 312 L790 305 L735 118"
    parts.append(f'<path d="{hub_path}" fill="none" stroke="{TEAL}" stroke-width="1" opacity="0.26"/>')

    counts = [5, 5, 2, 10, 10]
    nodes = []
    idx = 1
    for ci, (cx, cy, is_real) in enumerate(centers):
        n = counts[ci]
        for i in range(n):
            a = 2 * math.pi * i / n + ci * 0.85
            rad = 30 + (i % 3) * 11 + rng.random() * 6
            x = cx + rad * math.cos(a) * 1.45
            y = cy + rad * math.sin(a) * 1.0
            nodes.append((idx, cx, cy, x, y, is_real))
            idx += 1

    # links from each hub to its satellites
    for num, cx, cy, x, y, is_real in nodes:
        color = AMBER if is_real else TEAL
        parts.append(f'<path d="M{cx} {cy} Q{(cx+x)/2:.1f} {(cy+y)/2-8:.1f} {x:.1f} {y:.1f}" '
                     f'fill="none" stroke="{color}" stroke-width="0.9" opacity="0.38"/>')

    # satellite nodes with depth variation
    for num, cx, cy, x, y, is_real in nodes:
        color = AMBER if is_real else TEAL
        depth = 0.55 + ((num * 37) % 10) / 20  # 0.55 - 1.0
        r = 3.2 + depth * 1.8
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+3:.1f}" fill="{color}" opacity="{0.06*depth:.2f}" filter="url(#blur)"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}" opacity="{0.45+depth*0.4:.2f}"/>')

    # hub nodes
    for i, (cx, cy, is_real) in enumerate(centers):
        color = AMBER if is_real else TEAL
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{color}" opacity="0.07" filter="url(#blur)"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="17" fill="{NAVY0}" stroke="{color}" stroke-width="1.5" opacity="0.95"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{color}" stroke-width="0.5" opacity="0.3"/>')
        parts.append(t(cx, cy + 4.5, roman[i], 13, color, MONO, 700, "middle"))
        # label plate below hub
        ly = cy + 42
        parts.append(t(cx, ly, labels[i], 12.5, WHITE, MONO, 600, "middle", 0.9, 0.92))

    return "\n".join(parts)


def banner(zh=False):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'role="img" aria-label="Coursework — university CS capstone walkthroughs">']
    p.append(defs())
    p.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    # subtle light sweep + bottom fade
    p.append(f'<path d="M0 0 L520 0 L200 {H} L0 {H} Z" fill="{NAVY2}" opacity="0.28"/>')
    p.append(f'<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" stroke="url(#fade)" stroke-width="2"/>')

    # thin top rule with accent segment
    p.append(f'<rect x="64" y="42" width="46" height="2" fill="url(#accent)"/>')

    # eyebrow
    p.append(t(64, 72, "A STUDY WORKBOOK · UNIVERSITY COMPUTER SCIENCE", 12,
               TEAL, MONO, 600, spacing=2.2))

    # display title — large, tight tracking
    if zh:
        p.append(t(60, 136, "计算机课程", 54, WHITE, CJK, 700, spacing=2))
        p.append(t(60, 196, "大作业精解库", 54, WHITE, CJK, 700, spacing=2))
    else:
        p.append(t(60, 138, "COURSEWORK", 62, WHITE, DISPLAY, 800, spacing=1))
        p.append(t(60, 198, "A CAPSTONE ATLAS", 30, MUTED, DISPLAY, 300, spacing=5))

    # accent hairline
    p.append(f'<rect x="64" y="224" width="228" height="2" fill="url(#accent)"/>')

    # tagline
    if zh:
        p.append(t(64, 262, "把名校 CS 大作业拆透：设计、实现、调试、踩坑，", 15, MUTED, CJK))
        p.append(t(64, 288, "全部可运行、可复现。", 15, MUTED, CJK))
    else:
        p.append(t(64, 262, "Deep, runnable walkthroughs of the projects that", 15, MUTED))
        p.append(t(64, 288, "actually teach computer science — from design to debug.", 15, MUTED))

    # bottom stat row with engraved feel
    p.append(f'<line x1="64" y1="330" x2="520" y2="330" stroke="{GRID}" stroke-width="1"/>')
    stats = [("32", "PROJECTS"), ("22", "ORIGINAL"), ("10", "REAL"), ("7", "CHAPTERS")]
    for i, (num, label) in enumerate(stats):
        x = 64 + i * 116
        p.append(t(x, 372, num, 30, TEAL if i < 3 else AMBER, DISPLAY, 700))
        p.append(t(x, 392, label, 11, MUTED, MONO, 500, spacing=1.1))

    # atlas on the right
    p.append(constellation())

    p.append('</svg>')
    return "\n".join(p)


def strip(zh=False):
    """Compact stat strip for smaller contexts."""
    w, h = 560, 40
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="project counts">']
    items = ([("32", "道题目"), ("22", "原创精解"), ("10", "真实作业"), ("7", "章解析")] if zh else
             [("32", "PROJECTS"), ("22", "ORIGINAL"), ("10", "REAL"), ("7", "CHAPTERS")])
    for i, (num, label) in enumerate(items):
        x = 10 + i * 140
        c = TEAL if i < 3 else AMBER
        p.append(t(x, 27, num, 19, c, MONO, 700))
        p.append(t(x + 38, 26, label, 11, MUTED, CJK if zh else MONO, 500))
        if i < 3:
            p.append(f'<line x1="{x+128}" y1="8" x2="{x+128}" y2="32" stroke="{GRID}" stroke-width="1"/>')
    p.append('</svg>')
    return "\n".join(p)


for name, content in [
    ("banner.svg", banner(False)),
    ("banner-zh.svg", banner(True)),
    ("strip.svg", strip(False)),
    ("strip-zh.svg", strip(True)),
]:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"wrote {path} ({len(content)} bytes)")
