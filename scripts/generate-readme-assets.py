#!/usr/bin/env python3
"""Generate the README's SVG assets from the project's real catalog.

Keeps the artwork in sync with the 32 problems and five volumes.
No third-party dependencies.
"""

import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

INK = "#0F1C2E"
INK2 = "#16263D"
PAPER = "#F7F5EF"
TEAL = "#2DD4BF"
AMBER = "#F2B544"
SLATE = "#8FA3BC"
LINE = "#27405C"

DISPLAY = "'Avenir Next','Segoe UI',system-ui,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Code',monospace"
CJK = "'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif"


def txt(x, y, s, size=16.0, fill=PAPER, family=DISPLAY, weight=400,
        anchor="start", spacing=0.0, opacity=1.0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{ls}{op}>'
            f'{s}</text>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# Real catalog: number -> (volume 1..5, is_real)
# Volumes follow book/_quarto.yml part structure (I systems, II algorithms,
# III networks, IV intelligence, V real assignments).
CATALOG = {
    1: (3, 0), 2: (3, 0), 3: (4, 0), 4: (1, 0), 5: (1, 0),
    6: (1, 0), 7: (4, 0), 8: (1, 0), 9: (4, 0), 10: (4, 0),
    11: (4, 0), 12: (1, 0), 13: (4, 0), 14: (2, 0), 15: (2, 0),
    16: (1, 0), 17: (2, 0), 18: (2, 0), 19: (2, 0), 20: (4, 0),
    21: (2, 0), 22: (1, 0),
    23: (5, 1), 24: (5, 1), 25: (5, 1), 26: (5, 1), 27: (5, 1),
    28: (5, 1), 29: (5, 1), 30: (5, 1), 31: (5, 1), 32: (5, 1),
}

VOLUMES = [
    ("I", "SYSTEMS", 6), ("II", "ALGORITHMS", 6),
    ("III", "NETWORKS", 2), ("IV", "INTELLIGENCE", 7),
    ("V", "REAL ASSIGNMENTS", 10),
]


def node_positions():
    """Cluster the 32 real catalog entries around five volume anchors."""
    rng = random.Random(20261121)
    centers = [(690, 88), (900, 66), (1090, 98), (712, 226), (982, 238)]
    pts = []
    for vol in range(1, 6):
        members = [n for n, (v, _) in CATALOG.items() if v == vol]
        cx, cy = centers[vol - 1]
        for i, n in enumerate(members):
            angle = 2 * math.pi * i / len(members) + vol * 0.7
            radius = 34 + (i % 3) * 13 + rng.random() * 5
            x = cx + radius * math.cos(angle) * 1.35
            y = cy + radius * math.sin(angle) * 0.95
            pts.append((n, vol, CATALOG[n][1], x, y, cx, cy))
    return pts, centers


def hero(zh=False):
    pts, centers = node_positions()
    w, h = 1200, 372
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
             f'width="{w}" height="{h}" role="img" '
             f'aria-label="Coursework workbook hero">']
    parts.append(f'''<defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/>
      </linearGradient>
      <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{AMBER}"/>
      </linearGradient>
      <radialGradient id="glow"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.22"/>
        <stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
      <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
        <path d="M28 0H0V28" fill="none" stroke="{LINE}" stroke-width="0.5" opacity="0.45"/>
      </pattern>
    </defs>''')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#bg)"/>')
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#grid)"/>')
    parts.append('<ellipse cx="920" cy="160" rx="290" ry="180" fill="url(#glow)"/>')

    # Left: title block
    parts.append(f'<rect x="58" y="58" width="4" height="44" fill="{TEAL}"/>')
    if zh:
        parts.append(txt(80, 76, "计算机课程 · 大作业精解库", 27, PAPER, CJK, 700))
        parts.append(txt(80, 108, "从经典项目中学习系统思维", 18, SLATE, CJK, 400))
        parts.append(txt(60, 158, "把名校 CS 大作业拆透：题目背景、设计思路、逐步实现、", 15, SLATE, CJK))
        parts.append(txt(60, 182, "调试过程、踩坑清单与延伸练习 — 全部可运行、可复现。", 15, SLATE, CJK))
    else:
        parts.append(txt(80, 76, "CS COURSE", 27, PAPER, DISPLAY, 700, spacing=2))
        parts.append(txt(80, 108, "PROJECT WORKBOOK", 27, PAPER, DISPLAY, 700, spacing=2))
        parts.append(txt(60, 158, "Deep, runnable walkthroughs of outstanding CS course projects:", 15, SLATE))
        parts.append(txt(60, 182, "design reasoning, implementation, debugging, pitfalls, exercises.", 15, SLATE))
    parts.append(f'<rect x="60" y="204" width="330" height="2" fill="url(#rule)"/>')
    tagline = ("32 道题目 · 7 章精解 · 真实测试输出" if zh else
               "32 ASSIGNMENTS  /  7 CHAPTERS EACH  /  VERIFIED BUILDS")
    parts.append(txt(60, 232, tagline, 13, TEAL, MONO, spacing=1.2))
    linkline = ("22 道原创精解 + 10 道真实高校作业" if zh else
                "22 ORIGINAL STUDIES  +  10 REAL UNIVERSITY ASSIGNMENTS")
    parts.append(txt(60, 254, linkline, 12, SLATE, MONO))

    # Right: knowledge lineage graph
    for n, vol, is_real, x, y, cx, cy in pts:
        color = AMBER if is_real else TEAL
        parts.append(f'<path d="M{cx} {cy} Q{(cx+x)/2} {(cy+y)/2-12} {x} {y}" '
                     f'fill="none" stroke="{color}" stroke-width="0.8" opacity="0.28"/>')
    for i, (roman, name, _) in enumerate(VOLUMES):
        cx, cy = centers[i]
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="19" fill="{INK}" stroke="{TEAL if i<4 else AMBER}" stroke-width="1.4" opacity="0.95"/>')
        parts.append(txt(cx, cy + 4, roman, 12, TEAL if i < 4 else AMBER, MONO, 700, "middle"))
        # Place labels on the side away from the node cloud, with a dark plate
        # so connector lines can never cross the text.
        label_y = cy - 32 if i in (0, 1, 2) else cy + 46
        plate_w = 108 if i < 4 else 148
        parts.append(f'<rect x="{cx-plate_w/2}" y="{label_y-12}" width="{plate_w}" height="17" rx="3" fill="{INK}" opacity="0.92"/>')
        parts.append(txt(cx, label_y, name, 10, SLATE, MONO, 500, "middle", 0.5, 0.95))
    for n, vol, is_real, x, y, cx, cy in pts:
        color = AMBER if is_real else TEAL
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.2" fill="{color}" opacity="0.85"/>')
        parts.append(txt(x, y + 2.5, f"{n:03d}", 6.6, INK, MONO, 700, "middle"))

    # Bottom stats strip
    parts.append(f'<line x1="60" y1="292" x2="1140" y2="292" stroke="{LINE}" stroke-width="1"/>')
    stats = [
        ("32", "ASSIGNMENTS" if not zh else "道题目"),
        ("22", "ORIGINAL" if not zh else "原创精解"),
        ("10", "REAL REPOS" if not zh else "真实作业"),
        ("7", "CHAPTERS" if not zh else "章解析"),
        ("111", "PAGE BOOK" if not zh else "页成书"),
    ]
    for i, (num, label) in enumerate(stats):
        x = 60 + i * 218
        parts.append(txt(x, 326, num, 27, TEAL if i < 4 else AMBER, DISPLAY, 700))
        parts.append(txt(x, 348, label, 10, SLATE, MONO if not zh else CJK, 400, spacing=1))
    parts.append(f'<circle cx="1140" cy="40" r="3" fill="{TEAL}"/>')
    parts.append(f'<circle cx="1152" cy="40" r="3" fill="{AMBER}" opacity="0.6"/>')
    parts.append('</svg>')
    return "\n".join(parts)


def workflow(zh=False):
    w, h = 1100, 168
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="How to use">']
    p.append(f'''<defs><linearGradient id="wb" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/></linearGradient></defs>''')
    p.append(f'<rect width="{w}" height="{h}" rx="10" fill="url(#wb)"/>')
    steps = [
        ("01", "READ THE CARD", "Prerequisites, scope, expected effort") if not zh else
        ("01", "读题目卡片", "前置知识、范围、预计耗时"),
        ("02", "TRY IT YOURSELF", "Design first — even a rough sketch") if not zh else
        ("02", "先自己做", "哪怕只画出设计草图"),
        ("03", "STUDY 01 → 07", "Compare reasoning with your attempt") if not zh else
        ("03", "读七章精解", "对照自己的思路找差异"),
        ("04", "RUN & EXTEND", "Run tests, then solve the exercises") if not zh else
        ("04", "跑通并拓展", "跑测试，再做延伸练习"),
    ]
    for i, (num, title, desc) in enumerate(steps):
        x = 46 + i * 265
        if i < 3:
            p.append(f'<line x1="{x+210}" y1="80" x2="{x+252}" y2="80" stroke="{LINE}" stroke-width="1.5"/>')
            p.append(f'<path d="M{x+252} 80 l-7 -4 v8 z" fill="{TEAL}" opacity="0.7"/>')
        p.append(txt(x, 50, num, 13, TEAL if i < 3 else AMBER, MONO, 700))
        p.append(txt(x, 84, esc(title), 16 if not zh else 17, PAPER, MONO if not zh else CJK, 700))
        p.append(txt(x, 112, esc(desc), 11.5, SLATE, MONO if not zh else CJK))
        p.append(f'<rect x="{x}" y="126" width="38" height="2" fill="{TEAL if i<3 else AMBER}" opacity="0.8"/>')
    p.append('</svg>')
    return "\n".join(p)


def volumes(zh=False):
    w, h = 1100, 168
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Five volumes">']
    p.append(f'<rect width="{w}" height="{h}" rx="10" fill="{INK}"/>')
    names = ["SYSTEMS", "ALGORITHMS", "NETWORKS", "INTELLIGENCE", "REAL REPOS"]
    names_zh = ["系统基础", "算法与数据结构", "网络与分布式", "智能系统", "真实作业"]
    counts = ["4", "5", "2", "10", "10"]
    for i in range(5):
        x = 40 + i * 214
        color = TEAL if i < 4 else AMBER
        # spine as layered plate
        p.append(f'<rect x="{x}" y="36" width="22" height="100" rx="2" fill="{color}" opacity="0.9"/>')
        p.append(f'<rect x="{x+5}" y="36" width="2" height="100" fill="{INK}" opacity="0.35"/>')
        p.append(txt(x + 38, 66, f"VOL. {['I','II','III','IV','V'][i]}", 11, color, MONO, 700))
        p.append(txt(x + 38, 94, names_zh[i] if zh else names[i], 14, PAPER, CJK if zh else DISPLAY, 700))
        p.append(txt(x + 38, 118, f"{counts[i]} cases", 11, SLATE, MONO))
    p.append('</svg>')
    return "\n".join(p)


def divider():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 18" width="1200" height="18" role="presentation">'
            f'<line x1="0" y1="9" x2="520" y2="9" stroke="{LINE}" stroke-width="1"/>'
            f'<path d="M600 3 l6 6 -6 6 -6 -6 z" fill="{TEAL}"/>'
            f'<line x1="680" y1="9" x2="1200" y2="9" stroke="{LINE}" stroke-width="1"/>'
            f'<circle cx="545" cy="9" r="2" fill="{AMBER}" opacity="0.7"/>'
            f'<circle cx="655" cy="9" r="2" fill="{AMBER}" opacity="0.7"/></svg>')


def logo():
    """Compact 128px mark: the five-volume lineage reduced to an icon."""
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128" role="img" aria-label="Coursework mark">']
    p.append(f'''<defs>
      <linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK2}"/>
      </linearGradient>
    </defs>''')
    p.append('<rect x="2" y="2" width="124" height="124" rx="26" fill="url(#lg)" stroke="#27405C" stroke-width="1.5"/>')
    # five volume anchors laid out as a constellation
    anchors = [(64, 30), (98, 52), (88, 94), (40, 94), (30, 52)]
    # connective spine
    p.append(f'<path d="M{anchors[0][0]} {anchors[0][1]} L{anchors[1][0]} {anchors[1][1]} '
             f'L{anchors[2][0]} {anchors[2][1]} L{anchors[3][0]} {anchors[3][1]} '
             f'L{anchors[4][0]} {anchors[4][1]} Z" fill="none" stroke="{TEAL}" stroke-width="1.1" opacity="0.35"/>')
    p.append(f'<line x1="64" y1="64" x2="64" y2="30" stroke="{TEAL}" stroke-width="1" opacity="0.3"/>')
    p.append(f'<line x1="64" y1="64" x2="98" y2="52" stroke="{TEAL}" stroke-width="1" opacity="0.3"/>')
    p.append(f'<line x1="64" y1="64" x2="88" y2="94" stroke="{AMBER}" stroke-width="1" opacity="0.4"/>')
    p.append(f'<line x1="64" y1="64" x2="40" y2="94" stroke="{TEAL}" stroke-width="1" opacity="0.3"/>')
    p.append(f'<line x1="64" y1="64" x2="30" y2="52" stroke="{TEAL}" stroke-width="1" opacity="0.3"/>')
    for i, (x, y) in enumerate(anchors):
        color = AMBER if i == 2 else TEAL
        p.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{INK}" stroke="{color}" stroke-width="2"/>')
    # center core
    p.append(f'<circle cx="64" cy="64" r="13" fill="{INK}"/>')
    p.append(f'<circle cx="64" cy="64" r="11" fill="none" stroke="{PAPER}" stroke-width="1.6"/>')
    p.append(txt(64, 69, "32", 13, PAPER, MONO, 700, "middle"))
    p.append('</svg>')
    return "\n".join(p)


def catalog_strip():
    """Small inline band used under the title: counts only, no prose."""
    w, h = 520, 34
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="catalog counts">']
    items = [("32", "problems"), ("22", "original"), ("10", "real repos"), ("7", "chapters")]
    for i, (num, label) in enumerate(items):
        x = 8 + i * 130
        color = TEAL if i < 3 else AMBER
        p.append(txt(x, 23, num, 16, color, MONO, 700))
        p.append(txt(x + 30, 22, label, 10, SLATE, MONO))
        if i < 3:
            p.append(f'<line x1="{x+118}" y1="7" x2="{x+118}" y2="27" stroke="{LINE}" stroke-width="1"/>')
    p.append('</svg>')
    return "\n".join(p)


for name, content in [
    ("logo.svg", logo()),
    ("catalog-strip.svg", catalog_strip()),
    ("hero.svg", hero(False)),
    ("hero-zh.svg", hero(True)),
    ("workflow.svg", workflow(False)),
    ("workflow-zh.svg", workflow(True)),
    ("volumes.svg", volumes(False)),
    ("volumes-zh.svg", volumes(True)),
    ("divider.svg", divider()),
]:
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"wrote {path} ({len(content)} bytes)")
