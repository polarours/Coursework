#!/usr/bin/env python3
"""Strip hand-written chapter numbers from book titles and section headings.

Quarto numbers chapters by position in _quarto.yml, but the headings also
carried hard-coded numbers derived from filenames (ch13 is really chapter 19).
The two disagreed on every rendered page. Removing the literal numbers makes
Quarto's automatic numbering the single source of truth.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")

TITLE_EN = re.compile(r"^title:\s*\"Chapter \d+ · ")
TITLE_ZH = re.compile(r"第 \d+ 章 · ")
SECTION_NUM = re.compile(r"\((\d+)\.(\d+) ")

changed = 0
for path in sorted(glob.glob(os.path.join(BOOK, "vol*", "*.qmd"))):
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    out = []
    touched = False
    for line in lines:
        new = line
        if new.startswith("title:"):
            new = TITLE_EN.sub('title: "', new)
            new = TITLE_ZH.sub("", new)
        elif new.startswith("## "):
            new = SECTION_NUM.sub("(", new)
        if new != line:
            touched = True
        out.append(new)
    if touched:
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(out)
        changed += 1

print(f"cleaned headings in {changed} chapter files")
