#!/usr/bin/env python3
"""Flip bilingual H2/H3 headings to English-first: '中文 / English' -> 'English (中文)'."""
import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(BASE, "book")
CJK = re.compile(r'[\u3400-\u9fff]')

def flip(heading):
    # Patterns like "4.1 可采纳性 / Admissibility" or "Purpose / 本章目标"
    parts = [p.strip() for p in heading.split('/')]
    if len(parts) != 2:
        return None
    a, b = parts
    a_cjk, b_cjk = bool(CJK.search(a)), bool(CJK.search(b))
    if a_cjk and not b_cjk:
        return f"{b} ({a})"
    if b_cjk and not a_cjk:
        return f"{a} ({b})"
    return None

changed = 0
for f in sorted(glob.glob(os.path.join(BOOK, "**", "*.qmd"), recursive=True)):
    with open(f, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    out = []
    touched = False
    for line in lines:
        m = re.match(r'^(#{2,3})\s+(.*)$', line)
        if m:
            new = flip(m.group(2))
            if new:
                line = f"{m.group(1)} {new}"
                touched = True
        out.append(line)
    if touched:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out))
        changed += 1
print(f"flipped bilingual headings in {changed} chapters")
