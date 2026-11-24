#!/usr/bin/env python3
"""Add a 'Projects & universities in this chapter' line after each chapter's
Purpose callout (vol1-vol4), linking to the relevant university profiles.

Mapping is by chapter content (verified against each chapter's body).
Idempotent.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")

# chapter file -> [(problem number, university id, university label)]
CHAPTERS = {
 "vol1/ch01-foundations.qmd": [("005", "mit", "MIT"), ("006", "cmu", "CMU")],
 "vol1/ch02-memory.qmd": [("012", "berkeley", "UC Berkeley"), ("018", "mit", "MIT")],
 "vol1/ch03-processes.qmd": [("016", "mit", "MIT")],
 "vol1/ch12-workshop.qmd": [("022", "stanford", "Stanford")],
 "vol2/ch04-search.qmd": [("014", "princeton", "Princeton"), ("015", "stanford", "Stanford")],
 "vol2/ch05-graphs.qmd": [("021", "stanford", "Stanford")],
 "vol2/ch06-heuristics.qmd": [("019", "gatech", "Georgia Tech")],
 "vol3/ch07-reliable-transport.qmd": [("002", "stanford", "Stanford")],
 "vol3/ch08-consensus.qmd": [("001", "mit", "MIT")],
 "vol4/ch09-learning.qmd": [("011", "stanford", "Stanford")],
 "vol4/ch10-search-and-learning.qmd": [("003", "berkeley", "UC Berkeley")],
 "vol4/ch11-crypto.qmd": [("009", "stanford", "Stanford"), ("020", "cornell", "Cornell")],
}

MARK = "::: {.callout-tip collapse=\"true\"}"
changed = 0
for rel, items in CHAPTERS.items():
    path = os.path.join(BOOK, rel)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if "Projects in this chapter" in text:
        continue
    links = " · ".join(
        f"[{num} {label}](../universities/{uid}.qmd)" for num, uid, label in items
    )
    block = (
        f"\n::: {{.callout-tip}}\n"
        f"## Projects in this chapter (本章项目与来源高校)\n\n"
        f"{links}\n:::\n"
    )
    # insert after the first callout block ends (the Purpose callout)
    m = re.search(r'^(::: \{[^}]*\}\n[\s\S]*?\n:::\n)', text, re.M)
    if m:
        text = text[:m.end()] + block + text[m.end():]
    else:
        # fallback: insert after front matter
        m2 = re.search(r'^---\n[\s\S]*?\n---\n', text, re.M)
        pos = m2.end() if m2 else 0
        text = text[:pos] + block + text[pos:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    changed += 1
print(f"annotated {changed} chapters")
