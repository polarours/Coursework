#!/usr/bin/env python3
"""Remove the duplicate manual H1 from every Quarto chapter.

Quarto books render the YAML `title:` as an <h1 class="title"> masthead.
Our earlier heading-flip script also added a literal '# ...' line, producing
two H1s per page (e.g. '22 MIT' in the masthead and '23 MIT' below it).
This script removes that manual H1 so only the masthead remains.
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
changed = 0
for f in glob.glob(os.path.join(BOOK, "**", "*.qmd"), recursive=True):
    with open(f, encoding="utf-8") as fh:
        lines = fh.readlines()
    out, i, removed = [], 0, False
    # skip YAML front matter
    if lines and lines[0].strip() == "---":
        out.append(lines[0]); i = 1
        while i < len(lines) and lines[i].strip() != "---":
            out.append(lines[i]); i += 1
        if i < len(lines):
            out.append(lines[i]); i += 1
    # skip blank lines after front matter, then drop the first H1
    while i < len(lines) and not lines[i].strip():
        out.append(lines[i]); i += 1
    if i < len(lines) and lines[i].startswith("# "):
        removed = True
        i += 1
        # drop following blank line too
        if i < len(lines) and not lines[i].strip():
            i += 1
    out.extend(lines[i:])
    if removed:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("".join(out))
        changed += 1
print(f"removed duplicate H1 from {changed} chapters")
