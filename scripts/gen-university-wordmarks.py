#!/usr/bin/env python3
"""Generate editorial nameplates for universities without a licensable logo.

These are deliberately NOT imitations of official crests: each is a typographic
nameplate with the full institution name, founding year, country, and an
accent rule in the school's representative colour. Honest and trademark-safe.
Four schools (MIT, Stanford, Berkeley, CMU) use real logo files from an
MIT-licensed open course-map project instead.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "book", "universities", "logos")
os.makedirs(OUT, exist_ok=True)

# id: (full name, short, founded, place, accent, ink)
SCHOOLS = {
 "princeton": ("PRINCETON UNIVERSITY", "P", "1746", "NEW JERSEY, USA", "#E77500", "#1A1A1A"),
 "gatech": ("GEORGIA INSTITUTE OF TECHNOLOGY", "GT", "1885", "ATLANTA, USA", "#B3A369", "#0B2452"),
 "cornell": ("CORNELL UNIVERSITY", "C", "1865", "ITHACA, USA", "#B31B1B", "#1E1E1E"),
 "umd": ("UNIVERSITY OF MARYLAND", "UMD", "1856", "COLLEGE PARK, USA", "#E21838", "#1A1A1A"),
 "amirkabir": ("AMIRKABIR UNIVERSITY OF TECHNOLOGY", "AUT", "1958", "TEHRAN, IRAN", "#0E6B4F", "#12211B"),
 "fordham": ("FORDHAM UNIVERSITY", "F", "1841", "NEW YORK, USA", "#A2997D", "#6B1020"),
 "uci": ("UNIVERSITY OF CALIFORNIA, IRVINE", "UCI", "1965", "IRVINE, USA", "#005B94", "#101820"),
 "ccny": ("CITY COLLEGE OF NEW YORK", "CCNY", "1847", "NEW YORK, USA", "#4C6FA8", "#152238"),
 "clemson": ("CLEMSON UNIVERSITY", "CU", "1889", "SOUTH CAROLINA, USA", "#F66700", "#3A2258"),
 "ucsc": ("UNIVERSITY OF CALIFORNIA, SANTA CRUZ", "UCSC", "1965", "SANTA CRUZ, USA", "#C99700", "#0B3565"),
}

TPL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 150" width="560" height="150" role="img" aria-label="{name} nameplate">
  <rect width="560" height="150" rx="4" fill="{ink}"/>
  <rect x="0" y="0" width="8" height="150" fill="{accent}"/>
  <g opacity="0.18"><circle cx="500" cy="118" r="92" fill="none" stroke="{accent}" stroke-width="1"/>
  <circle cx="500" cy="118" r="66" fill="none" stroke="{accent}" stroke-width="1"/>
  <circle cx="500" cy="118" r="40" fill="none" stroke="{accent}" stroke-width="1"/></g>
  <text x="34" y="66" font-family="Georgia,serif" font-size="60" font-weight="700" fill="{accent}">{short}</text>
  <line x1="34" y1="84" x2="410" y2="84" stroke="{accent}" stroke-width="1.5" opacity="0.8"/>
  <text x="34" y="108" font-family="Helvetica,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="1.1" fill="#FFFFFF">{name}</text>
  <text x="34" y="131" font-family="Helvetica,Arial,sans-serif" font-size="10" letter-spacing="1.6" fill="#9FB0BE">EST. {founded} &#160;&#183;&#160; {place}</text>
</svg>
'''

for sid, (name, short, founded, place, accent, ink) in SCHOOLS.items():
    with open(os.path.join(OUT, f"{sid}.svg"), "w", encoding="utf-8") as f:
        f.write(TPL.format(name=name, short=short, founded=founded, place=place, accent=accent, ink=ink))
    print("wrote", sid + ".svg")
