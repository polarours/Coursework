#!/usr/bin/env python3
"""Turn each problems/*/README.md into a page in the book.

The book previously covered twelve themes and mentioned only some of the 34
assignments, so the site's search index had nothing for a problem number. This
script gives every problem its own page: metadata, why it is included, the
measured results, and links to the seven-chapter walkthrough in the repo.

Run it after adding a problem; it is idempotent.
"""
import glob
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = os.path.join(ROOT, "problems")
OUT = os.path.join(ROOT, "book", "problems")

REPO = "https://github.com/polarours/Coursework"
BRANCH = "blob/master"
CHAPTERS = [
    "01-题目解读.md", "02-设计思路.md", "03-逐步实现.md",
    "04-正确性与复杂度.md", "05-调试与测试.md", "06-踩坑清单.md", "07-延伸练习.md",
]
LANGS = ["C++", "Java", "Python", "OCaml", "Scheme", "Rust", "Go",
         "JavaScript", "TypeScript", "SQL", "C"]
CHAPTER_TITLES = [
    "题目解读", "设计思路", "逐步实现", "正确性与复杂度",
    "调试与测试", "踩坑清单", "延伸练习",
]


def field(text, *names):
    for name in names:
        m = re.search(rf"^- {re.escape(name)}:[ \t]*(.+)$", text, re.M)
        if m:
            return m.group(1).strip()
    return ""


def section(text, *heads):
    """Return the body of a '## ...' section whose title starts with any head."""
    for head in heads:
        m = re.search(rf"^## {re.escape(head)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if m:
            return m.group(1).strip()
    return ""


def bullets(body):
    """Keep only '- ' lines and strip markers; drop *English:* duplicates."""
    out = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:].strip())
        elif s and not out and not s.startswith("*"):
            out.append(s)
    return out


EXT_LANG = {
    ".py": "Python", ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".hpp": "C++",
    ".java": "Java", ".c": "C", ".h": "C", ".go": "Go", ".rs": "Rust",
    ".ml": "OCaml", ".mli": "OCaml", ".scm": "Scheme", ".ss": "Scheme",
    ".js": "JavaScript", ".ts": "TypeScript", ".sql": "SQL",
}


def infer_language(text, title, course, dirpath):
    """Prefer what the README declares, then what solution/ actually contains —
    the file extensions are the one signal that cannot be aspirational."""
    declared = field(text, "实现语言 / Language")
    if declared:
        return declared
    sol = os.path.join(dirpath, "solution")
    if os.path.isdir(sol):
        counts = {}
        for dirpath2, _, files in os.walk(sol):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in EXT_LANG:
                    counts[EXT_LANG[ext]] = counts.get(EXT_LANG[ext], 0) + 1
        if counts:
            return max(counts, key=counts.get)
    hay = f"{title} {course}"
    for lang in LANGS:
        if re.search(rf"(?<![A-Za-z+]){re.escape(lang)}(?![A-Za-z+])", hay):
            if lang == "C" and re.search(r"C\+\+|CS|CIS|CSE", hay):
                continue
            return lang
    return ""


def infer_difficulty(text, dirpath):
    """Real assignments rarely declare a difficulty. Rather than invent one,
    derive it from the size of the code that actually ships, and say so on the
    index page."""
    declared = field(text, "难度 / Difficulty")
    if declared:
        return declared
    for sub in ("solution", "upstream"):
        base = os.path.join(dirpath, sub)
        if not os.path.isdir(base):
            continue
        total = 0
        for dp, _, files in os.walk(base):
            for f in files:
                if os.path.splitext(f)[1].lower() not in EXT_LANG:
                    continue
                try:
                    with open(os.path.join(dp, f), encoding="utf-8", errors="ignore") as fh:
                        total += sum(1 for _ in fh)
                except OSError:
                    pass
        if total:
            if total < 200:
                return "入门 / Introductory"
            if total < 600:
                return "进阶 / Intermediate"
            return "硬核 / Advanced"
    return ""


def parse(path):
    text = open(path, encoding="utf-8").read()
    d = os.path.dirname(path)
    slug = os.path.basename(d)
    num = slug[:3]

    title_raw = re.search(r"^# (.+)$", text, re.M)
    title = title_raw.group(1) if title_raw else slug

    uni = re.search(r"来源高校 / University profile: \[(.+?)\]\((.+?)\)", text)
    uni_name = uni.group(1) if uni else ""
    uni_id = ""
    if uni:
        m = re.search(r"universities/([a-z]+)\.html", uni.group(2))
        uni_id = m.group(1) if m else ""

    return {
        "slug": slug,
        "num": num,
        "title": title,
        "uni_name": uni_name,
        "uni_id": uni_id,
        "school": field(text, "学校 / University"),
        "course": field(text, "课程 / Course", "课程风格 / Course style"),
        "area": field(text, "方向 / Area"),
        "difficulty": infer_difficulty(text, os.path.dirname(path)),
        "effort": field(text, "预计耗时 / Estimated effort"),
        "language": field(text, "实现语言 / Language"),
        "upstream": field(text, "上游仓库 / Upstream"),
        "lang_inferred": infer_language(text, title, field(text, "课程 / Course", "课程风格 / Course style"), d),
        "why": section(text, "为什么收录", "背景"),
        "verified": section(text, "实测结果", "实测"),
        "dir": d,
    }


REL_LINK = re.compile(r"\]\((\d{2}-[^)]+\.md)\)")


def absolutise(text, slug):
    """A link like 05-调试与测试.md only resolves inside the repo, not in the book."""
    def repl(m):
        return f"]({REPO}/{BRANCH}/problems/{slug}/{quote(m.group(1))})"
    return REL_LINK.sub(repl, text)


CJK = re.compile(r"[\u3400-\u9fff]")


def split_bilingual(text):
    """Insert a blank line where a Chinese line is immediately followed by a
    pure-English one; without it Markdown joins them into a single paragraph."""
    lines = text.split("\n")
    out = []
    for line in lines:
        if out and line.strip() and not CJK.search(line) and CJK.search(out[-1] or ""):
            out.append("")
        out.append(line)
    return "\n".join(out)


def render(p):
    rows = []
    if p["uni_name"]:
        if p["uni_id"]:
            rows.append(("学校", f"[{p['uni_name']}](../universities/{p['uni_id']}.qmd)"))
        else:
            rows.append(("学校", p["uni_name"]))
    elif p["school"]:
        rows.append(("学校", p["school"]))
    if p["course"]:
        rows.append(("课程", p["course"]))
    if p["area"]:
        rows.append(("方向", p["area"]))
    if p["language"]:
        rows.append(("语言", p["language"]))
    if p["difficulty"]:
        rows.append(("难度", p["difficulty"]))
    if p["effort"]:
        rows.append(("预计耗时", p["effort"]))
    if p["upstream"]:
        m = re.search(r"https://\S+", p["upstream"])
        if m:
            rows.append(("上游仓库", f"[{m.group(0)}]({m.group(0)})"))

    parts = [
        "---",
        f'title: "{p["num"]} · ' + re.sub(r"（真实高校作业[^）]*）", "", p["title"].split("·", 1)[-1]).strip() + '"',
        "number-sections: false",
        "---",
        "",
    ]

    if rows:
        table = ["| 项目 | 内容 |", "|---|---|"]
        table += [f"| {k} | {v} |" for k, v in rows]
        parts += ["\n".join(table), ""]

    if p["why"]:
        body = split_bilingual(absolutise(p["why"], p["slug"]))
        # Keep the first prose paragraph plus any English italic gloss.
        parts += ["## 为什么收录", body, ""]

    if p["verified"]:
        items = bullets(absolutise(p["verified"], p["slug"]))
        if items:
            parts += ["## 实测结果", ""]
            parts += [f"- {i}" for i in items]
            parts += [""]

    # Walkthrough links point at the repository, where the full chapters live.
    links = []
    for name, label in zip(CHAPTERS, CHAPTER_TITLES):
        path = os.path.join(p["dir"], name)
        if os.path.exists(path):
            url = f"{REPO}/{BRANCH}/problems/{p['slug']}/{quote(name)}"
            links.append(f"[{label}]({url})")
    if links:
        parts += ["## 七章解析", "", " · ".join(links), ""]

    parts += [
        "## 源码与测试",
        "",
        f"[题目目录]({REPO}/tree/master/problems/{p['slug']})　·　"
        f"[参考实现]({REPO}/tree/master/problems/{p['slug']}/solution)　·　"
        f"[测试]({REPO}/tree/master/problems/{p['slug']}/tests)",
        "",
    ]
    return "\n".join(parts)


def write_index(items):
    """A single table, grouped by university, so the page is scannable."""
    groups = {}
    for p in items:
        key = p["uni_name"] or p["school"] or "原创 / Original"
        groups.setdefault(key, []).append(p)

    order = sorted(groups, key=lambda k: (-len(groups[k]), k))
    lines = [
        "---",
        'title: "Problem Index <span class=\'zh-inline\'>(题目索引)</span>"',
        "---",
        "",
        f"{len(items)} 道题，按学校分组。每道题都有独立的页面：元信息、实测结果、七章解析入口。",
        "",
        "> 22 道自主解析题（001–022）与 12 道真实课程作业（023–034）。真实作业的原始仓库以 submodule 形式引入，"
        "参考实现独立编写并跑通原测试。",
        "",
        "标为「入门 / 进阶 / 硬核」的难度，未由课程声明者按随仓库发布的代码规模推定"
        "（<200 / 200–600 / >600 行），不是对课程难度的官方评价。",
        "",
        "在 PDF 中这些档案页带有章号（第 37 章起）：章号是**排版顺序**，题号 001–034 是**收录序号**，两者无关。"
        "网页版关闭了章号，只显示题号。",
        "",
    ]
    for name in order:
        rows = groups[name]
        lines += [f"## {name}", "", "| # | 题目 | 语言 | 难度 |", "|---|---|---|---|"]
        for p in sorted(rows, key=lambda x: x["num"]):
            title = p["title"].split("·", 1)[-1].strip() if "·" in p["title"] else p["title"]
            for prefix in (p["uni_name"], p["school"]):
                if prefix:
                    first = prefix.split()[0]
                    if title.startswith(first + " "):
                        title = title[len(first) + 1:]
                    if title.startswith(prefix + " "):
                        title = title[len(prefix) + 1:]
            title = re.sub(r"（真实高校作业[^）]*）", "", title).strip()
            raw_lang = p["language"] or p.get("lang_inferred") or ""
            lang = raw_lang.split(" / ")[0] if raw_lang else "—"
            diff = p["difficulty"].split(" / ")[0] if p["difficulty"] else "—"
            lines.append(f"| {p['num']} | [{title}]({p['slug']}.qmd) | {lang} | {diff} |")
        lines.append("")
    with open(os.path.join(OUT, "index.qmd"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def update_quarto_yml(slugs):
    """Quarto does not expand globs in a book's chapter list, so the list has to
    be written out. Keeping it in this script means adding a problem is one
    command, not two edits that can drift apart."""
    yml_path = os.path.join(ROOT, "book", "_quarto.yml")
    text = open(yml_path, encoding="utf-8").read()
    block = ["    - part: \"Problems (题目档案)\"", "      chapters:",
             "        - problems/index.qmd"]
    block += [f"        - problems/{s}.qmd" for s in sorted(slugs)]
    new_block = "\n".join(block)
    pattern = re.compile(
        r'    - part: "Problems \(题目档案\)"\n      chapters:\n(?:        - .*\n?)+', re.M)
    if pattern.search(text):
        text = pattern.sub(new_block + "\n", text)
    else:
        text = text.replace('    - part: "Appendices"', new_block + "\n\n    - part: \"Appendices\"")
    open(yml_path, "w", encoding="utf-8").write(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    items = []
    for readme in sorted(glob.glob(os.path.join(PROBLEMS, "*", "README.md"))):
        p = parse(readme)
        items.append(p)
        with open(os.path.join(OUT, f"{p['slug']}.qmd"), "w", encoding="utf-8") as fh:
            fh.write(render(p))
    write_index(items)
    update_quarto_yml([p["slug"] for p in items])
    print(f"generated {len(items)} problem pages, an index, and the book TOC")


if __name__ == "__main__":
    main()
