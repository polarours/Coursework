#!/usr/bin/env python3
"""Generate the technical figures used in the book.

Every figure is drawn from the same optical vocabulary as the site: thin ink
lines, one teal accent, one amber accent, no decoration that does not carry
meaning. Output is SVG so both the HTML site and the typst PDF can render it.
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
        f'    .cell {{ font-size: 13px; font-weight: 600; }}\n'
        f'  </style>\n'
        f'{body}\n</svg>\n'
    )


def figure_addr_split():
    """32-bit address sliced into tag / index / offset."""
    W, H = 720, 190
    x0, y0, bar_h = 60, 74, 46
    total = 640
    widths = [total * 22 // 32, total * 6 // 32, total * 4 // 32]
    fills = [GREY_L, TEAL_L, AMBER_L]
    labels = ["tag · 22 位", "index · 6 位", "offset · 4 位"]
    subs = ["bit 31–10", "bit 9–4", "bit 3–0"]
    notes = ["与缓存行的 tag 比较", "选中哪一组", "组内第几个字节"]

    parts = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    parts.append(
        f'  <text x="{x0}" y="34" class="ttl">32 位地址 → tag / index / offset</text>'
    )
    parts.append(f'  <text x="{x0}" y="52" class="sm">块大小 16 字节、64 组时的位切分</text>')

    x = x0
    for w, fill, label, sub in zip(widths, fills, labels, subs):
        parts.append(
            f'  <rect x="{x}" y="{y0}" width="{w}" height="{bar_h}" fill="{fill}" '
            f'stroke="{LINE}" stroke-width="1"/>'
        )
        parts.append(
            f'  <text x="{x + w / 2}" y="{y0 + 22}" class="cell" text-anchor="middle">{label}</text>'
        )
        parts.append(
            f'  <text x="{x + w / 2}" y="{y0 + 38}" class="sm" text-anchor="middle">{sub}</text>'
        )
        # bit tick at the boundary
        parts.append(
            f'  <line x1="{x}" y1="{y0 - 8}" x2="{x}" y2="{y0}" stroke="{INK}" stroke-width="1"/>'
        )
        x += w
    parts.append(
        f'  <line x1="{x}" y1="{y0 - 8}" x2="{x}" y2="{y0}" stroke="{INK}" stroke-width="1"/>'
    )
    parts.append(
        f'  <text x="{x}" y="{y0 - 12}" class="sm" text-anchor="end">bit 0</text>'
    )
    parts.append(
        f'  <text x="{x0}" y="{y0 - 12}" class="sm">bit 31</text>'
    )

    # annotations under each band
    x = x0
    for w, note in zip(widths, notes):
        parts.append(
            f'  <text x="{x + w / 2}" y="{y0 + bar_h + 24}" class="sm" '
            f'text-anchor="middle">{note}</text>'
        )
        x += w

    parts.append(
        f'  <text x="{x0}" y="176" class="sm">'
        f'一次访问：用 index 选组 → 并行比较该组所有路的 tag → 命中则用 offset 取字节</text>'
    )
    return svg(W, H, "\n".join(parts))


def figure_fork_exec():
    """Parent and child timelines across fork, exec and wait."""
    W, H = 720, 268
    y_parent, y_child = 92, 168
    x_start, x_fork, x_exec, x_wait, x_end = 90, 240, 410, 540, 610

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="60" y="34" class="ttl">fork 复制，exec 替换，wait 回收</text>')
    p.append(f'  <text x="60" y="52" class="sm">一次调用返回两次；成功 exec 不再返回</text>')

    # lanes
    p.append(f'  <text x="60" y="{y_parent + 4}" class="lbl">父进程</text>')
    p.append(f'  <text x="60" y="{y_child + 4}" class="lbl">子进程</text>')
    p.append(
        f'  <line x1="{x_start}" y1="{y_parent}" x2="{x_end}" y2="{y_parent}" '
        f'stroke="{INK}" stroke-width="1.6"/>'
    )
    p.append(
        f'  <line x1="{x_fork}" y1="{y_child}" x2="{x_end}" y2="{y_child}" '
        f'stroke="{INK}" stroke-width="1.6"/>'
    )
    # fork branch
    p.append(
        f'  <path d="M {x_fork} {y_parent} C {x_fork + 30} {y_parent}, '
        f'{x_fork + 20} {y_child}, {x_fork + 56} {y_child}" '
        f'fill="none" stroke="{TEAL}" stroke-width="1.8"/>'
    )
    p.append(
        f'  <line x1="{x_fork}" y1="{y_parent - 26}" x2="{x_fork}" y2="{y_child + 26}" '
        f'stroke="{LINE}" stroke-width="1" stroke-dasharray="4 3"/>'
    )
    p.append(f'  <text x="{x_fork}" y="{y_parent - 20}" class="sm" text-anchor="middle">fork()</text>')

    # parent return value
    p.append(
        f'  <text x="{x_fork + 6}" y="{y_parent - 10}" class="sm">返回子进程 PID</text>'
    )
    p.append(
        f'  <text x="{x_fork + 60}" y="{y_child + 22}" class="sm">返回 0</text>'
    )

    # exec marker on child lane
    p.append(
        f'  <rect x="{x_exec}" y="{y_child - 30}" width="86" height="22" rx="3" '
        f'fill="{TEAL_L}" stroke="{TEAL}" stroke-width="1"/>'
    )
    p.append(
        f'  <text x="{x_exec + 43}" y="{y_child - 15}" class="sm" text-anchor="middle">exec：映像替换</text>'
    )
    p.append(
        f'  <line x1="{x_exec + 43}" y1="{y_child - 8}" x2="{x_exec + 43}" y2="{y_child}" '
        f'stroke="{TEAL}" stroke-width="1"/>'
    )
    p.append(
        f'  <text x="{x_exec + 43}" y="{y_child + 22}" class="sm" text-anchor="middle">PID 不变</text>'
    )

    # wait
    p.append(
        f'  <line x1="{x_wait}" y1="{y_parent}" x2="{x_wait}" y2="{y_child}" '
        f'stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="5 3"/>'
    )
    p.append(
        f'  <rect x="{x_wait - 26}" y="{y_parent - 44}" width="96" height="22" rx="3" '
        f'fill="{AMBER_L}" stroke="{AMBER}" stroke-width="1"/>'
    )
    p.append(
        f'  <text x="{x_wait + 22}" y="{y_parent - 29}" class="sm" text-anchor="middle">wait：回收状态</text>'
    )

    # end markers
    p.append(f'  <circle cx="{x_end}" cy="{y_parent}" r="3.5" fill="{INK}"/>')
    p.append(f'  <circle cx="{x_end}" cy="{y_child}" r="3.5" fill="{INK}"/>')
    p.append(
        f'  <text x="{x_end + 8}" y="{y_parent + 4}" class="sm">继续读下一行</text>'
    )
    p.append(f'  <text x="{x_end + 8}" y="{y_child + 4}" class="sm">退出</text>')

    p.append(
        f'  <text x="60" y="{H - 18}" class="sm">'
        f'父进程的 fork 返回值正是子进程的 PID；子进程看到 0，因此两者走不同分支</text>'
    )
    return svg(W, H, "\n".join(p))


def figure_tcp_window():
    """Sender-side sliding window over the sequence space."""
    W, H = 720, 210
    x0, y0, h = 60, 92, 44
    seg = [170, 170, 170, 110]  # acknowledged, in flight, sendable, unopened
    fills = [GREY_L, TEAL_L, AMBER_L, WHITE]
    titles = ["已确认", "已发送未确认", "可发送", "窗口外"]
    subs = ["acked", "in flight", "usable", "not yet"]

    p = [f'  <rect width="{W}" height="{H}" fill="{WHITE}"/>']
    p.append(f'  <text x="{x0}" y="34" class="ttl">发送窗口：三个游标划分序列号空间</text>')
    p.append(f'  <text x="{x0}" y="52" class="sm">窗口 = 已发送未确认 + 可发送；ACK 到来后整体右移</text>')

    x = x0
    for w, fill, t, s in zip(seg, fills, titles, subs):
        p.append(
            f'  <rect x="{x}" y="{y0}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{LINE}" stroke-width="1"/>'
        )
        p.append(
            f'  <text x="{x + w / 2}" y="{y0 + 20}" class="cell" text-anchor="middle">{t}</text>'
        )
        p.append(
            f'  <text x="{x + w / 2}" y="{y0 + 35}" class="sm" text-anchor="middle">{s}</text>'
        )
        x += w

    # cursor labels
    # send_base separates acked from in-flight; next_seq separates in-flight
    # from sendable; window_end closes the usable region.
    cursors = [
        (x0 + seg[0], "send_base", "已确认的边界"),
        (x0 + seg[0] + seg[1], "next_seq", "下一个要发的字节"),
        (x0 + seg[0] + seg[1] + seg[2], "window_end", "窗口右边界"),
    ]
    p.append(
        f'  <text x="{x0}" y="{y0 + h + 14}" class="sm">序列空间起点</text>'
    )

    for cx, name, desc in cursors:
        p.append(
            f'  <line x1="{cx}" y1="{y0 - 10}" x2="{cx}" y2="{y0 + h + 10}" '
            f'stroke="{TEAL}" stroke-width="1.4"/>'
        )
        p.append(
            f'  <circle cx="{cx}" cy="{y0 - 10}" r="3" fill="{TEAL}"/>'
        )
        p.append(
            f'  <text x="{cx}" y="{y0 - 16}" class="sm" text-anchor="middle">{name}</text>'
        )

    p.append(
        f'  <text x="{x0}" y="{y0 + h + 32}" class="sm">'
        f'{cursors[0][2]} ← 收到 ACK 就前移，窗口随之滑动</text>'
    )
    p.append(
        f'  <text x="{x0}" y="{y0 + h + 50}" class="sm">'
        f'实际可发字节数 = min(接收窗口, 拥塞窗口) − 已发送未确认</text>'
    )
    return svg(W, H, "\n".join(p))


def main():
    os.makedirs(OUT, exist_ok=True)
    figures = {
        "addr-split.svg": figure_addr_split(),
        "fork-exec.svg": figure_fork_exec(),
        "tcp-window.svg": figure_tcp_window(),
    }
    for name, content in figures.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"wrote {name} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
