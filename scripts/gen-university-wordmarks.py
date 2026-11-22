#!/usr/bin/env python3
"""Generate university wordmark tiles for schools without a licensable logo file.

These are typographic identifiers (abbreviation + name), NOT official crests
or seals. Each tile states that explicitly, so the book never implies an
endorsement. Four schools (MIT, Stanford, Berkeley, CMU) use real logo files
from an MIT-licensed open course-map project; the rest get an honest wordmark.

All output is SVG, dependency-free.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "universities", "logos")
os.makedirs(OUT, exist_ok=True)

# id: (abbreviation, full name, accent color, secondary)
SCHOOLS = {
    "princeton": ("P", "PRINCETON", "#E77500", "#231F20"),
    "gatech": ("GT", "GEORGIA TECH", "#B3A369", "#002D72"),
    "cornell": ("C", "CORNELL", "#B31B1B", "#222222"),
    "umd": ("UMD", "MARYLAND", "#E21838", "#231F20"),
    "amirkabir": ("AUT", "AMIRKABIR", "#0E6B4F", "#1A1A1A"),
    "fordham": ("F", "FORDHAM", "#A2997D", "#7A0010"),
    "uci": ("UCI", "UC IRVINE", "#005B94", "#FFCD00"),
    "ccny": ("CCNY", "CITY COLLEGE NY", "#003366", "#B39DDB"),
    "clemson": ("CU", "CLEMSON", "#F66700", "#522D80"),
    "ucsc": ("UCSC", "UC SANTA CRUZ", "#E8B001", "#003C83"),
}

TPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 120" width="320" height="120" role="img" aria-label="{name} wordmark">
  <rect width="320" height="120" rx="8" fill="{dark}"/>
  <rect x="10" y="10" width="300" height="100" rx="5" fill="none" stroke="{accent}" stroke-width="1.5" opacity="0.6"/>
  <text x="26" y="70" font-family="Georgia,serif" font-size="52" font-weight="700" fill="{accent}">{abbr}</text>
  <text x="{tx}" y="62" font-family="Helvetica,Arial,sans-serif" font-size="17" font-weight="700" letter-spacing="1.6" fill="#FFFFFF">{name}</text>
  <text x="{tx}" y="84" font-family="Helvetica,Arial,sans-serif" font-size="9.5" letter-spacing="0.5" fill="#B9C4CC">typographic identifier · not an official crest</text>
</svg>
'''

for sid, (abbr, name, accent, dark) in SCHOOLS.items():
    tx = 26 + (105 if len(abbr) <= 1 else 130)
    svg = TPL.format(name=name, abbr=abbr, accent=accent, dark=dark, tx=tx)
    path = os.path.join(OUT, f"{sid}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.basename(path))
