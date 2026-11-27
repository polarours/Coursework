#!/usr/bin/env python3
"""Generate the social preview card (1200x630) and its PNG.

Shared links currently unfurl into a blank card, which wastes the one moment
where someone decides whether to click. The card states what the project is
and how big it is, in the same ink/teal palette as the book.

Run: python3 scripts/gen-og-image.py   (needs rsvg-convert on PATH)
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets")
SVG_PATH = os.path.join(OUT_DIR, "og-image.svg")
PNG_PATH = os.path.join(OUT_DIR, "og-image.png")

INK = "#0B1626"
INK_2 = "#12233B"
TEAL = "#3EE0C8"
AMBER = "#F5BE5C"
PAPER = "#F4F8FC"
MUTED = "#93A9C4"

W, H = 1200, 630


def build():
    stats = [("34", "assignments"), ("14", "universities"), ("229", "pages")]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        '<defs>',
        f'  <linearGradient id="bg" x1="0" y1="0" x2="0.7" y2="1">',
        f'    <stop offset="0" stop-color="{INK}"/>',
        f'    <stop offset="1" stop-color="{INK_2}"/>',
        f'  </linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        # faint rule grid, suggesting a page of typeset notes
        '<g stroke="#FFFFFF" stroke-opacity="0.04" stroke-width="1">',
    ]
    for y in range(70, H, 44):
        parts.append(f'  <line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    parts.append('</g>')

    # left accent bar
    parts.append(f'<rect x="80" y="96" width="4" height="188" fill="{TEAL}"/>')

    parts += [
        f'<text x="108" y="160" font-family="Noto Serif, Georgia, serif" font-size="72" '
        f'font-weight="600" fill="{PAPER}">Coursework</text>',
        f'<text x="110" y="216" font-family="Noto Serif, Georgia, serif" font-size="34" '
        f'fill="{TEAL}">A Capstone Atlas</text>',
        f'<text x="110" y="262" font-family="Noto Sans, Helvetica, sans-serif" font-size="20" '
        f'fill="{MUTED}">Learning systems thinking through capstone assignments, solved and measured</text>',
        f'<text x="110" y="292" font-family="Noto Sans CJK SC, Noto Sans, sans-serif" font-size="20" '
        f'fill="{MUTED}">三十四道大作业，每一道都跑过、量过、写下来</text>',
    ]

    # statistics row
    x = 110
    for value, label in stats:
        parts += [
            f'<text x="{x}" y="432" font-family="Noto Serif, Georgia, serif" font-size="62" '
            f'font-weight="600" fill="{PAPER}">{value}</text>',
            f'<text x="{x + 2}" y="462" font-family="Noto Sans, Helvetica, sans-serif" '
            f'font-size="18" letter-spacing="1.6" fill="{AMBER}">{label.upper()}</text>',
        ]
        x += 250

    parts += [
        f'<line x1="80" y1="520" x2="{W - 80}" y2="520" stroke="{PAPER}" stroke-opacity="0.16"/>',
        f'<text x="80" y="562" font-family="Noto Sans, Helvetica, sans-serif" font-size="20" '
        f'fill="{MUTED}">Bilingual · Chinese and English · every number from a real run</text>',
        f'<text x="{W - 80}" y="562" text-anchor="end" font-family="Noto Sans, Helvetica, sans-serif" '
        f'font-size="20" fill="{TEAL}">polarours.github.io/Coursework</text>',
        '</svg>',
    ]
    return "\n".join(parts)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build()
    with open(SVG_PATH, "w", encoding="utf-8") as fh:
        fh.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H),
                    "-o", PNG_PATH, SVG_PATH], check=True)

    # Quarto only copies what the book declares, so the card also lives inside
    # book/ where the site can serve it from the same origin.
    book_assets = os.path.join(ROOT, "book", "assets")
    os.makedirs(book_assets, exist_ok=True)
    deployed = os.path.join(book_assets, "og-image.png")
    with open(PNG_PATH, "rb") as src, open(deployed, "wb") as dst:
        dst.write(src.read())

    size = os.path.getsize(PNG_PATH)
    print(f"wrote {os.path.relpath(SVG_PATH, ROOT)} and .png ({size // 1024} KB), "
          f"deployed copy in book/assets/")


if __name__ == "__main__":
    main()
