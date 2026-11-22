#!/usr/bin/env python3
"""Flip book headings to English-first (Chinese retained in parentheses).

Content bodies stay bilingual; this pass touches only YAML titles, part
names in _quarto.yml, and markdown headings so the default reading
experience is English-led.
"""
import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(BASE, "book")

# canonical English-first titles for YAML + first H1 of each qmd
TITLES = {
    "index.qmd": ("Preface", "前言"),
    "backmatter/summary.qmd": ("Summary", "总结"),
    "backmatter/how-to-use.qmd": ("How to Use This Book", "如何使用本书"),
    "vol1/index.qmd": ("Volume I · Systems Foundations", "卷一 · 系统基础"),
    "vol1/ch01-foundations.qmd": ("Chapter 1 · Foundations of Memory and Execution", "第 1 章 · 内存与执行的基础"),
    "vol1/ch02-memory.qmd": ("Chapter 2 · Memory Hierarchy and Caches", "第 2 章 · 存储层次与缓存"),
    "vol1/ch03-processes.qmd": ("Chapter 3 · Processes and the Shell", "第 3 章 · 进程接口与 Shell"),
    "vol1/ch12-workshop.qmd": ("Chapter 12 · Assignment Workshop", "第 12 章 · 作业工坊"),
    "vol2/index.qmd": ("Volume II · Algorithms and Data Structures", "卷二 · 算法与数据结构"),
    "vol2/ch04-search.qmd": ("Chapter 4 · Heuristic Search", "第 4 章 · 启发式搜索"),
    "vol2/ch05-graphs.qmd": ("Chapter 5 · Graph Algorithms and Greedy Methods", "第 5 章 · 图算法与贪心"),
    "vol2/ch06-heuristics.qmd": ("Chapter 6 · Probabilistic Structures and Caches", "第 6 章 · 概率结构与缓存抽象"),
    "vol3/index.qmd": ("Volume III · Networks and Distributed Systems", "卷三 · 网络与分布式"),
    "vol3/ch07-reliable-transport.qmd": ("Chapter 7 · Reliable Transport", "第 7 章 · 可靠传输"),
    "vol3/ch08-consensus.qmd": ("Chapter 8 · Distributed Consensus", "第 8 章 · 分布式共识"),
    "vol4/index.qmd": ("Volume IV · Intelligent Systems", "卷四 · 智能系统"),
    "vol4/ch09-learning.qmd": ("Chapter 9 · Neural Networks and Gradients", "第 9 章 · 神经网络与梯度"),
    "vol4/ch10-search-and-learning.qmd": ("Chapter 10 · AI Search and Reinforcement Learning", "第 10 章 · AI 搜索与强化学习"),
    "vol4/ch11-crypto.qmd": ("Chapter 11 · Cryptographic Primitives", "第 11 章 · 密码学构件"),
    "vol5/index.qmd": ("Volume V · Real Assignments", "卷五 · 真实作业集成"),
    "vol5/ch13-cxx-assignments.qmd": ("Chapter 13 · Six Real C++ Assignments", "第 13 章 · C++ 真实作业六题"),
    "vol5/ch14-java-python-assignments.qmd": ("Chapter 14 · Java and Python Assignments", "第 14 章 · Java 与 Python 真实作业"),
}

def flip_title(en, zh):
    return f"{en} <span class='zh-inline'>({zh})</span>"

changed = 0
for rel, (en, zh) in TITLES.items():
    path = os.path.join(BOOK, rel)
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    new = flip_title(en, zh)
    # YAML title
    txt2 = re.sub(r'^title: ".*?"$', f'title: "{new}"', txt, count=1, flags=re.M)
    # first markdown H1 (chapter headline), keep any existing content after slash
    lines = txt2.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i] = "# " + new
            break
    txt2 = "\n".join(lines)
    if txt2 != txt:
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt2)
        changed += 1

print(f"flipped {changed} qmd titles")

# _quarto.yml book title + parts
qc = os.path.join(BOOK, "_quarto.yml")
with open(qc, encoding="utf-8") as f:
    y = f.read()
y = y.replace('title: "计算机课程大作业精解"',
              'title: "Coursework · A Capstone Atlas"')
y = y.replace('subtitle: "从知名高校期末项目中学习系统思维 / Learning Systems Thinking through Capstone Projects"',
              'subtitle: "Learning Systems Thinking through Capstone Projects"')
parts = {
    "卷一 · 系统基础 / Systems Foundations": "Volume I · Systems Foundations",
    "卷二 · 算法与数据结构 / Algorithms and Data Structures": "Volume II · Algorithms and Data Structures",
    "卷三 · 网络与分布式 / Networks and Distributed Systems": "Volume III · Networks and Distributed Systems",
    "卷四 · 智能系统 / Intelligent Systems": "Volume IV · Intelligent Systems",
    "卷五 · 真实作业集成 / Real Assignments": "Volume V · Real Assignments",
    "附录 / Appendices": "Appendices",
}
for a, b in parts.items():
    y = y.replace(f'part: "{a}"', f'part: "{b}"')
with open(qc, "w", encoding="utf-8") as f:
    f.write(y)
print("updated _quarto.yml")
