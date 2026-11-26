#!/usr/bin/env python3
"""Second batch of book figures: search, consensus, backprop, bloom, enigma.

Same ink/teal/amber vocabulary as the first batch. Every quantitative figure
uses numbers measured elsewhere in this project, never invented ones.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "figures")

INK = "#1B2A38"
MUTED = "#5B6B73"
LINE = "#C9D4DC"
TEAL = "#159F8C"
TEAL_L = "#D6F2ED"
AMBER = "#C98A22"
AMBER_L = "#FBEBD0"
GREY_L = "#EEF2F5"
WHITE = "#FFFFFF"
FONT = "Helvetica, Arial, sans-serif"


def svg(width, height, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img">\n'
        f'  <style>\n'
        f'    text {{ font-family: {FONT}; fill: {INK}; }}\n'
        f'    .lbl {{ font-size: 12px; }}\n'
        f'    .sm  {{ font-size: 10.5px; fill: {MUTED}; }}\n'
        f'    .ttl {{ font-size: 13px; font-weight: 600; }}\n'
        f'    .cell {{ font-size: 12.5px; font-weight: 600; }}\n'
        f'    .mono {{ font-family: "DejaVu Sans Mono", monospace; font-size: 11px; }}\n'
        f'  </style>\n'
        f'{body}\n</svg>\n'
    )


def figure_astar_expansion():
    """Log-scale bar chart of nodes expanded under three heuristics."""
    W, H = 720, 300
    x0, y_base, plot_h = 110, 232, 150
    bars = [("h = 0\n(Dijkstra)", 48390, GREY_L, INK),
            ("曼哈顿", 283, TEAL_L, TEAL),
            ("曼哈顿 + 线性冲突", 166, AMBER_L, AMBER)]
    import math
    max_log = math.log10(48390)
    bar_w, gap = 118, 62

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="60" y="34" class="ttl">同一局面、三种启发式：展开节点数（对数刻度）</text>')
    p.append(f'  <text x="60" y="52" class="sm">三者的解路径长度都是 20 步——启发式只改变看多少</text>')

    # baseline
    p.append(f'  <line x1="{x0 - 10}" y1="{y_base}" x2="{x0 + 3 * (bar_w + gap)}" y2="{y_base}" '
             f'stroke="{INK}" stroke-width="1.2"/>')

    x = x0
    for label, value, fill, accent in bars:
        h = plot_h * (math.log10(value) / max_log)
        y = y_base - h
        p.append(f'  <rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{fill}" '
                 f'stroke="{accent}" stroke-width="1.2"/>')
        p.append(f'  <text x="{x + bar_w / 2}" y="{y - 8}" class="cell" '
                 f'text-anchor="middle">{value:,}</text>')
        for i, line in enumerate(label.split("\n")):
            p.append(f'  <text x="{x + bar_w / 2}" y="{y_base + 18 + i * 14}" class="sm" '
                     f'text-anchor="middle">{line}</text>')
        x += bar_w + gap

    # ratio annotations
    p.append(f'  <text x="{x0 + bar_w + gap / 2}" y="{y_base - plot_h * 0.85:.0f}" '
             f'class="sm" text-anchor="middle">171×</text>')
    p.append(f'  <text x="{x0 + 2 * (bar_w + gap) - gap * 0.15:.0f}" y="{y_base - plot_h * 0.80:.0f}" '
             f'class="sm" text-anchor="middle">1.7×</text>')

    p.append(f'  <text x="60" y="{H - 16}" class="sm">'
             f'状态空间共 181440 个可解局面；Dijkstra 的 48390 个节点接近四分之一</text>')
    return svg(W, H, "\n".join(p))


def figure_raft_terms():
    """Terms, leaders and a log that gets overwritten (Figure 8 shape)."""
    W, H = 720, 288
    x0 = 92
    term_y = 78
    lanes = [("S1", 128), ("S2", 166), ("S5", 204)]
    cell_w, cell_h, cell_gap = 82, 26, 6

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="60" y="34" class="ttl">任期与日志：多数派复制不等于提交</text>')
    p.append(f'  <text x="60" y="52" class="sm">旧任期条目可能被后来的 leader 覆盖（Raft 论文 Figure 8）</text>')

    # term axis
    p.append(f'  <line x1="{x0}" y1="{term_y}" x2="{x0 + 3 * 150}" y2="{term_y}" '
             f'stroke="{INK}" stroke-width="1.4"/>')
    for i in range(3):
        cx = x0 + i * 150
        p.append(f'  <line x1="{cx}" y1="{term_y - 6}" x2="{cx}" y2="{term_y + 6}" '
                 f'stroke="{INK}" stroke-width="1.4"/>')
        p.append(f'  <text x="{cx + 75}" y="{term_y - 10}" class="sm" text-anchor="middle">'
                 f'term {i + 1}</text>')
    p.append(f'  <text x="{x0 + 3 * 150 + 78}" y="{term_y - 26}" class="sm" text-anchor="end">时间 →</text>')

    # leader bars (who led, roughly)
    leader_spans = [(0, "S1"), (1, "S5"), (2, "S1")]
    for i, who in leader_spans:
        cx = x0 + i * 150 + 10
        p.append(f'  <rect x="{cx}" y="{term_y + 8}" width="130" height="16" rx="3" '
                 f'fill="{TEAL_L}" stroke="{TEAL}" stroke-width="1"/>')
        p.append(f'  <text x="{cx + 65}" y="{term_y + 20}" class="sm" text-anchor="middle">'
                 f'leader {who}</text>')

    # log rows
    for idx, (name, y) in enumerate(lanes):
        p.append(f'  <text x="60" y="{y + 18}" class="lbl">{name}</text>')
        # X occupies index 2 in term 2 and only reaches S1 and S2 (2 of 5
        # nodes). S5 later writes its own entry at index 2 in term 3, which is
        # why a bare majority copy of X would not have protected it.
        entries = {
            "S1": [("1", "t1"), ("2", "t2"), ("", "")],
            "S2": [("1", "t1"), ("2", "t2"), ("", "")],
            "S5": [("1", "t1"), ("2", "t3"), ("3", "t3")],
        }[name]
        x = x0 + 8
        for label, term in entries:
            fill = WHITE
            stroke = LINE
            if term == "t3":
                fill = AMBER_L
                stroke = AMBER
            elif term == "t4":
                fill = GREY_L
                stroke = MUTED
            p.append(f'  <rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="3" '
                     f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            if label:
                p.append(f'  <text x="{x + cell_w / 2}" y="{y + 12}" class="cell" '
                         f'text-anchor="middle">{label}</text>')
                p.append(f'  <text x="{x + cell_w / 2}" y="{y + 23}" class="sm" '
                         f'text-anchor="middle">{term}</text>')
            x += cell_w + cell_gap

    p.append(f'  <text x="{x0 + 8}" y="{H - 22}" class="sm">'
             f'X（index 2，term 2）只到达 S1、S2 —— 5 个节点里 2 个，未过半</text>')
    p.append(f'  <text x="{x0 + 8}" y="{H - 8}" class="sm">'
             f'S5 在 term 3 当选时日志没有 X，可以合法覆盖 index 2：多数派复制并不构成承诺</text>')
    return svg(W, H, "\n".join(p))


def figure_backprop():
    """Forward and backward pass with tensor shapes."""
    W, H = 720, 250
    boxes = [
        ("X", "N×D"),
        ("S1 = X·W1+b1", "N×H"),
        ("A1 = ReLU(S1)", "N×H"),
        ("S2 = A1·W2+b2", "N×C"),
        ("P = softmax", "N×C"),
        ("L", "标量"),
    ]
    bw, bh, gap = 96, 40, 18
    x_start, y_mid = 34, 118

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="{x_start}" y="34" class="ttl">前向四步，反向四步</text>')
    p.append(f'  <text x="{x_start}" y="52" class="sm">每个盒子的形状必须能写出来；转置错在反向才会暴露</text>')

    xs = []
    x = x_start
    for i, (name, shape) in enumerate(boxes):
        xs.append(x)
        fill = TEAL_L if i in (0, len(boxes) - 1) else WHITE
        stroke = TEAL if i in (0, len(boxes) - 1) else LINE
        p.append(f'  <rect x="{x}" y="{y_mid - bh / 2}" width="{bw}" height="{bh}" rx="4" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        p.append(f'  <text x="{x + bw / 2}" y="{y_mid - 2}" class="cell" text-anchor="middle">{name}</text>')
        p.append(f'  <text x="{x + bw / 2}" y="{y_mid + 13}" class="sm" text-anchor="middle">{shape}</text>')
        if i < len(boxes) - 1:
            ax = x + bw
            p.append(f'  <line x1="{ax + 2}" y1="{y_mid}" x2="{ax + gap - 4}" y2="{y_mid}" '
                     f'stroke="{TEAL}" stroke-width="1.6"/>')
            p.append(f'  <path d="M {ax + gap - 8} {y_mid - 4} L {ax + gap - 2} {y_mid} '
                     f'L {ax + gap - 8} {y_mid + 4}" fill="none" stroke="{TEAL}" stroke-width="1.6"/>')
        x += bw + gap

    # backward band
    y_back = y_mid + 74
    p.append(f'  <text x="{x_start}" y="{y_mid + bh}" class="sm">前向：左 → 右　　'
             f'反向：右 → 左，每步乘上局部导数</text>')
    p.append(f'  <line x1="{x_start + bw + gap - 10}" y1="{y_back}" '
             f'x2="{xs[-1] + bw - 10}" y2="{y_back}" stroke="{AMBER}" stroke-width="1.4" '
             f'stroke-dasharray="5 3"/>')
    p.append(f'  <path d="M {x_start + bw + gap - 16} {y_back - 4} L {x_start + bw + gap - 24} {y_back} '
             f'L {x_start + bw + gap - 16} {y_back + 4}" fill="none" stroke="{AMBER}" stroke-width="1.4"/>')
    p.append(f'  <text x="{x_start + bw + gap - 30}" y="{y_back - 8}" class="sm" '
             f'text-anchor="end">dS = P − y 从这里开始</text>')

    p.append(f'  <text x="{x_start}" y="{H - 16}" class="sm">'
             f'softmax 与交叉熵复合后梯度化简为 p − y，因此反向的第一个张量形状与 P 相同</text>')
    return svg(W, H, "\n".join(p))


def figure_bloom():
    """Bit array with three hash positions marked."""
    W, H = 720, 268
    n_bits = 16
    cell, gap = 34, 4
    x0 = 96
    y_bar = 126

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="60" y="34" class="ttl">布隆过滤器：一个位数组，k 个哈希</text>')
    p.append(f'  <text x="60" y="52" class="sm">位只会从 0 变 1，所以不会漏报已插入的元素</text>')

    # inserted key arrows
    hits = [2, 7, 12]
    p.append(f'  <text x="{x0 - 26}" y="{y_bar - 30}" class="sm" text-anchor="end">key "alpha"</text>')
    for i, bit in enumerate(hits):
        bx = x0 + bit * (cell + gap) + cell / 2
        p.append(f'  <path d="M {x0 - 24} {y_bar - 34} C {x0 - 4} {y_bar - 58}, '
                 f'{bx} {y_bar - 58}, {bx} {y_bar - 12}" fill="none" stroke="{TEAL}" '
                 f'stroke-width="1.2" opacity="0.75"/>')
        p.append(f'  <text x="{bx}" y="{y_bar - 46}" class="sm" text-anchor="middle">h{i + 1}</text>')

    for i in range(n_bits):
        x = x0 + i * (cell + gap)
        is_set = i in hits
        fill = TEAL if is_set else WHITE
        p.append(f'  <rect x="{x}" y="{y_bar}" width="{cell}" height="{cell}" rx="3" '
                 f'fill="{fill}" stroke="{INK if is_set else LINE}" stroke-width="1.2"/>')
        p.append(f'  <text x="{x + cell / 2}" y="{y_bar + cell / 2 + 4}" '
                 f'class="sm" text-anchor="middle" '
                 f'fill="{"#FFFFFF" if is_set else MUTED}">{1 if is_set else 0}</text>')
        if i % 4 == 0:
            p.append(f'  <text x="{x + cell / 2}" y="{y_bar + cell + 14}" class="sm" '
                     f'text-anchor="middle">{i}</text>')

    # query result illustration
    qy = y_bar + 74
    p.append(f'  <text x="{x0}" y="{qy}" class="sm">查询任意元素：只要有一位是 0 → 一定不存在</text>')
    p.append(f'  <text x="{x0}" y="{qy + 18}" class="sm">'
             f'k 位全为 1 → 可能存在（假阳性来自其他元素恰好置了这些位）</text>')
    p.append(f'  <text x="{x0}" y="{qy + 44}" class="sm">'
             f'删除会清掉共享位 → 制造假阴性，所以标准结构不支持删除</text>')
    return svg(W, H, "\n".join(p))


def figure_enigma():
    """Signal path through plugboard, rotors and reflector, and back."""
    W, H = 720, 250
    stages = ["键盘", "插线板", "转子 I", "转子 II", "转子 III", "反射器"]
    bw, bh = 86, 34
    gap = 20
    x0, y_top = 40, 96
    y_bot = 176

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="{x0}" y="34" class="ttl">Enigma：信号穿过转子与反射器，再原路返回</text>')
    p.append(f'  <text x="{x0}" y="52" class="sm">'
             f'反射器让信号走对称路径，因此加密与解密是同一个操作</text>')

    xs = []
    x = x0
    for i, name in enumerate(stages):
        xs.append(x)
        fill = AMBER_L if name == "反射器" else WHITE
        stroke = AMBER if name == "反射器" else LINE
        p.append(f'  <rect x="{x}" y="{y_top}" width="{bw}" height="{bh}" rx="4" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
        p.append(f'  <text x="{x + bw / 2}" y="{y_top + bh / 2 + 4}" class="cell" '
                 f'text-anchor="middle">{name}</text>')
        x += bw + gap

    # forward path (teal) above boxes
    p.append(f'  <line x1="{x0 + bw}" y1="{y_top - 10}" x2="{xs[-1] + bw}" y2="{y_top - 10}" '
             f'stroke="{TEAL}" stroke-width="1.6"/>')
    p.append(f'  <path d="M {xs[-1] + bw - 6} {y_top - 14} L {xs[-1] + bw} {y_top - 10} '
             f'L {xs[-1] + bw - 6} {y_top - 6}" fill="none" stroke="{TEAL}" stroke-width="1.6"/>')
    p.append(f'  <text x="{x0 + 6}" y="{y_top - 16}" class="sm">明文 →</text>')

    # return path (amber) below boxes
    p.append(f'  <line x1="{xs[-1] + bw - 10}" y1="{y_top + bh + 12}" '
             f'x2="{x0 + bw - 10}" y2="{y_top + bh + 12}" stroke="{AMBER}" stroke-width="1.6" '
             f'stroke-dasharray="5 3"/>')
    p.append(f'  <path d="M {x0 + bw - 4} {y_top + bh + 8} L {x0 + bw - 12} {y_top + bh + 12} '
             f'L {x0 + bw - 4} {y_top + bh + 16}" fill="none" stroke="{AMBER}" stroke-width="1.6"/>')
    p.append(f'  <text x="{x0 + bw - 18}" y="{y_top + bh + 8}" class="sm" text-anchor="end">← 密文</text>')

    p.append(f'  <text x="{x0}" y="{y_top + bh + 44}" class="sm">'
             f'正向：明文经转子逐级替换，到反射器折返；反向：同一组转子逆序替换，回到灯板</text>')
    p.append(f'  <text x="{x0}" y="{y_top + bh + 62}" class="sm">'
             f'每加密一个字符转子前移一格，因此同一个字母在不同位置映射到不同的密文</text>')
    p.append(f'  <text x="{x0}" y="{H - 12}" class="sm">'
             f'对称是设计缺陷：拿到同样的机器就能解密，盟军正是这样破译的</text>')
    return svg(W, H, "\n".join(p))


def main():
    os.makedirs(OUT, exist_ok=True)
    figures = {
        "astar-expansion.svg": figure_astar_expansion(),
        "raft-terms.svg": figure_raft_terms(),
        "backprop.svg": figure_backprop(),
        "bloom-bits.svg": figure_bloom(),
        "enigma-path.svg": figure_enigma(),
    }
    for name, content in figures.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"wrote {name} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
