#!/usr/bin/env python3
"""Catch overflowing or overlapping text in generated SVGs without rendering.

Estimates each <text> element's bounding box from its content, font size and
text-anchor, then reports text that leaves the canvas or collides with other
text. Not a substitute for looking at a figure, but it catches the errors that
are otherwise only visible after export.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS = os.path.join(ROOT, "book", "figures")

SIZES = {"lbl": 12.0, "sm": 10.5, "ttl": 13.0, "cell": 12.5, "mono": 11.0}
DEFAULT_SIZE = 12.0


def char_width(ch, size):
    code = ord(ch)
    if code > 0x2E80:          # CJK and full-width punctuation
        return size
    if ch in "ilI.,:;'|! ":
        return size * 0.30
    if ch.isupper():
        return size * 0.66
    return size * 0.53


def text_width(s, size):
    return sum(char_width(ch, size) for ch in s)


def boxes(path):
    """Yield (label, left, top, right, bottom) for every text element."""
    tree = ET.parse(path)
    root = tree.getroot()
    vb = root.get("viewBox", "").split()
    if len(vb) != 4:
        return [], 0, 0
    width, height = float(vb[2]), float(vb[3])
    out = []
    for el in root.iter():
        if not el.tag.endswith("text"):
            continue
        content = "".join(el.itertext()).strip()
        if not content:
            continue
        cls = (el.get("class") or "").split()
        size = next((SIZES[c] for c in cls if c in SIZES), DEFAULT_SIZE)
        w = text_width(content, size)
        x = float(el.get("x", 0))
        y = float(el.get("y", 0))
        anchor = el.get("text-anchor", "start")
        if anchor == "middle":
            left, right = x - w / 2, x + w / 2
        elif anchor == "end":
            left, right = x - w, x
        else:
            left, right = x, x + w
        top, bottom = y - size * 0.80, y + size * 0.24
        out.append((content, left, top, right, bottom))
    return out, width, height


def check(path):
    items, width, height = boxes(path)
    name = os.path.basename(path)
    problems = []

    for content, l, t, r, b in items:
        if l < -1 or r > width + 1:
            problems.append(f"{name}: {content[:26]!r} spans {l:.0f}..{r:.0f} "
                            f"(canvas 0..{width:.0f})")
        if t < -1 or b > height + 1:
            problems.append(f"{name}: {content[:26]!r} at y={t:.0f}..{b:.0f} "
                            f"(canvas 0..{height:.0f})")

    # Text-text collisions: require a meaningful overlap on both axes so that
    # adjacent labels sharing a baseline are not flagged.
    for i in range(len(items)):
        ci, li, ti, ri, bi = items[i]
        for j in range(i + 1, len(items)):
            cj, lj, tj, rj, bj = items[j]
            ox = min(ri, rj) - max(li, lj)
            oy = min(bi, bj) - max(ti, tj)
            if ox > 2 and oy > 2:
                problems.append(f"{name}: {ci[:22]!r} overlaps {cj[:22]!r} "
                                f"({ox:.0f}x{oy:.0f}px)")
    return problems


def main():
    files = sorted(glob.glob(os.path.join(FIGS, "*.svg")))
    all_problems = []
    for f in files:
        all_problems.extend(check(f))
    if all_problems:
        print("Figure text problems:")
        for p in all_problems:
            print(" -", p)
        return 1
    print(f"Checked {len(files)} figures: no overflow, no text collisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
