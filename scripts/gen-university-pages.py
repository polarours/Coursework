#!/usr/bin/env python3
"""Generate university profile pages from auditable structured data.

Each page now has a distinct narrative angle (narrative.py) rather than the
same five-section encyclopedia template. Notable people and courses are
tables, not run-on sentences; a bridge paragraph connects the school's
tradition to the actual projects in this book.

Usage: python3 scripts/gen-university-pages.py
"""
import importlib.util
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
OUT = os.path.join(BOOK, "universities")


def load(name):
    path = os.path.join(OUT, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


UNIVERSITIES = load("data").UNIVERSITIES
NARR = load("narrative")
TPL = '''---
title: "{en} <span class='zh-inline'>({zh})</span>"
---

<img src="logos/{logo}" alt="{en}" width="420" class="uni-plate">

<p class="uni-credit">{logo_credit}</p>

**{signature}**

> {signature_zh}

## Why it matters (为何重要)

{tradition}

> {tradition_zh}

## Background (背景)

{bg_en}

> {bg_zh}

## People (人物)

| Person | Connection to computing |
|:--|:--|
{people_rows}

> {people_zh}

## Courses (课程)

| Course | Title |
|:--|:--|
{course_rows}

> {courses_zh}

## In this book (本书收录)

{problem_rows}

**{bridge_en}**

> {bridge_zh}

## Sources (来源)

{source_list}

---

*University identifiers are editorial nameplates, not official crests. Logos for MIT, Stanford, Berkeley and CMU are redistributed under an MIT-licensed open course-map project. All other institutions are represented by nameplates generated from `scripts/gen-university-wordmarks.py`.*
'''


def split_people(text):
    """Split '**Name** — claim. **Name2** — claim.' into table rows."""
    parts = re.split(r'(?=\*\*[^*]+\*\*\s*[—–-])', text)
    rows = []
    for p in parts:
        p = p.strip().rstrip('.').strip()
        if not p:
            continue
        m = re.match(r'\*\*(.+?)\*\*\s*[—–-]\s*(.+)', p, re.S)
        if m:
            name, claim = m.group(1).strip(), m.group(2).strip().rstrip('.')
            rows.append(f"| {name} | {claim} |")
    return "\n".join(rows) if rows else f"| — | {text} |"


def split_courses(text):
    """Split '6.001 Title · 6.006 Title · ...' into table rows."""
    items = [x.strip().rstrip('.') for x in text.split('·') if x.strip()]
    rows = []
    for item in items:
        m = re.match(r'^([A-Za-z0-9.]+\s?\d+[A-Za-z0-9.]*)\s+(.+)$', item)
        if m:
            rows.append(f"| {m.group(1)} | {m.group(2)} |")
        else:
            rows.append(f"| — | {item} |")
    return "\n".join(rows)


def render(u):
    nid = u['id']
    sig, tradition = NARR.NARRATIVE[nid]
    sig_zh, tradition_zh = NARR.NARRATIVE_ZH[nid]
    bridge_en, bridge_zh = NARR.BRIDGE[nid]
    problems = "\n".join(
        f"- [{p} · {title}](https://github.com/polarours/Coursework/tree/master/problems/{path})"
        for p, path, title in u["problems"]
    ) or "_No projects from this school in this book._"
    sources = "\n".join(f"- <{url}>" for url in u["sources"])
    logo_credit = ("Official mark, redistributed under an MIT-licensed open course-map project."
                   if u['logo'].endswith(('.png', '.svg')) and nid in ('mit','stanford','berkeley','cmu')
                   else "Editorial nameplate — not an official crest. Generated from `scripts/gen-university-wordmarks.py`.")
    return TPL.format(
        **u,
        logo_credit=logo_credit,
        signature=sig, signature_zh=sig_zh,
        tradition=tradition, tradition_zh=tradition_zh,
        people_rows=split_people(u['people_en']),
        course_rows=split_courses(u['courses_en']),
        problem_rows=problems,
        bridge_en=bridge_en, bridge_zh=bridge_zh,
        source_list=sources,
    )


for u in UNIVERSITIES:
    with open(os.path.join(OUT, f"{u['id']}.qmd"), "w", encoding="utf-8") as f:
        f.write(render(u))
    print("wrote", u['id'] + ".qmd")
