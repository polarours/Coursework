#!/usr/bin/env python3
"""Generate flat-square README badges as local SVGs.

shields.io is the usual choice, but it is one more network dependency between a
reader and the first line of the README. These are generated here, weigh under
a kilobyte each, and use the book's own palette. The CI badge stays remote
because only GitHub knows the answer.

Run: python3 scripts/gen-badges.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "badges")

INK = "#0B1626"
TEAL = "#3EE0C8"
AMBER = "#F5BE5C"
PAPER = "#F4F8FC"
GREY = "#93A9C4"

BADGES = [
    ("problems", "34", TEAL, INK),
    ("universities", "14", AMBER, INK),
    ("pages", "229", GREY, INK),
    ("license", "CC BY-NC-SA 4.0", PAPER, INK),
]


def text_width(s, size=11):
    total = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            total += size
        elif ch.isupper():
            total += size * 0.66
        elif ch in " .,:;'|!":
            total += size * 0.32
        else:
            total += size * 0.56
    return total


def badge(label, message, msg_bg, msg_fg):
    pad = 6.0
    lw = text_width(label) + 2 * pad
    mw = text_width(message) + 2 * pad
    w = lw + mw
    h = 20
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h}" role="img" aria-label="{label}: {message}">
  <title>{label}: {message}</title>
  <rect width="{w:.0f}" height="{h}" rx="3" fill="{INK}"/>
  <rect x="{lw:.0f}" width="{mw:.0f}" height="{h}" rx="3" fill="{msg_bg}"/>
  <rect x="{lw:.0f}" width="3" height="{h}" fill="{msg_bg}"/>
  <g font-family="Noto Sans, Helvetica, Arial, sans-serif" font-size="11" fill="{PAPER}">
    <text x="{lw / 2:.1f}" y="14" text-anchor="middle">{label}</text>
  </g>
  <g font-family="Noto Sans, Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="{msg_fg}">
    <text x="{lw + mw / 2:.1f}" y="14" text-anchor="middle">{message}</text>
  </g>
</svg>
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    for label, message, bg, fg in BADGES:
        path = os.path.join(OUT, f"{label}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(badge(label, message, bg, fg))
        print(f"wrote assets/badges/{label}.svg")


if __name__ == "__main__":
    main()
