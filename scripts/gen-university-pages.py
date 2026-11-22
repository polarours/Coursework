#!/usr/bin/env python3
"""Generate one Quarto chapter per university from structured data.

Data lives in universities.yaml-like Python dict below (easy to audit and
update). Each generated page is bilingual, English-first, with a logo,
background, notable people, notable CS courses, and the problems in this
book that come from that school.

Usage: python3 scripts/gen-university-pages.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "universities")
os.makedirs(OUT, exist_ok=True)

# Filled from verified research; each entry must carry sources.
UNIVERSITIES = []
# populated by a separate data file that the research step writes
DATA = os.path.join(OUT, "data.py")
if os.path.exists(DATA):
    import importlib.util
    spec = importlib.util.spec_from_file_location("uni_data", DATA)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    UNIVERSITIES = mod.UNIVERSITIES

TPL = '''---
title: "{en} <span class='zh-inline'>({zh})</span>"
---

# {en} <span class='zh-inline'>({zh})</span>

<img src="logos/{logo}" alt="{en} identifier" width="150" style="display:block;margin:0 0 1.4rem 0">

{intro_en}

> {intro_zh}

## Background (背景)

{bg_en}

> {bg_zh}

## Notable people (名人)

{people_en}

> {people_zh}

## Notable CS courses (著名计算机课程)

{courses_en}

> {courses_zh}

## In this book (本书收录)

{problem_list}

## Sources (来源)

{source_list}
'''

def render(u):
    problems = "\n".join(
        f"- [{p}](https://github.com/polarours/Coursework/tree/master/problems/{path}) — {title}"
        for p, path, title in u["problems"]
    ) or "_No projects from this school in this book._"
    sources = "\n".join(f"- <{url}>" for url in u["sources"])
    return TPL.format(**u, problem_list=problems, source_list=sources)

for u in UNIVERSITIES:
    path = os.path.join(OUT, f"{u['id']}.qmd")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(u))
    print("wrote", os.path.basename(path))
