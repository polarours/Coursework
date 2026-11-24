#!/usr/bin/env python3
"""Link each problem README to its university profile in the book.

Adds a single line near the top of every problem README:
  - 来源高校 / University profile: [Name](https://polarours.github.io/Coursework/universities/<id>.html)

Idempotent: safe to re-run.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = os.path.join(ROOT, "problems")
SITE = "https://polarours.github.io/Coursework/universities"

# problem number -> (university id, display name)
MAP = {
 "001": ("mit", "MIT"), "002": ("stanford", "Stanford University"),
 "003": ("berkeley", "UC Berkeley"), "004": ("berkeley", "UC Berkeley"),
 "005": ("mit", "MIT"), "006": ("cmu", "Carnegie Mellon University"),
 "007": ("stanford", "Stanford University"), "008": ("cmu", "Carnegie Mellon University"),
 "009": ("stanford", "Stanford University"), "010": ("stanford", "Stanford University"),
 "011": ("stanford", "Stanford University"), "012": ("berkeley", "UC Berkeley"),
 "013": ("berkeley", "UC Berkeley"), "014": ("princeton", "Princeton University"),
 "015": ("stanford", "Stanford University"), "016": ("mit", "MIT"),
 "017": ("cmu", "Carnegie Mellon University"), "018": ("mit", "MIT"),
 "019": ("gatech", "Georgia Institute of Technology"), "020": ("cornell", "Cornell University"),
 "021": ("stanford", "Stanford University"), "022": ("stanford", "Stanford University"),
 "023": ("amirkabir", "Amirkabir University of Technology"), "024": ("fordham", "Fordham University"),
 "025": ("uci", "UC Irvine"), "026": ("uci", "UC Irvine"),
 "027": ("ccny", "City College of New York"), "028": ("clemson", "Clemson University"),
 "029": ("berkeley", "UC Berkeley"), "030": ("umd", "University of Maryland"),
 "031": ("ucsc", "UC Santa Cruz"), "032": ("ucsc", "UC Santa Cruz"),
}

changed = 0
for d in sorted(os.listdir(PROBLEMS)):
    if not d[:3].isdigit():
        continue
    num = d[:3]
    if num not in MAP:
        continue
    uid, name = MAP[num]
    path = os.path.join(PROBLEMS, d, "README.md")
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if "Coursework/universities/" in text:
        continue
    line = f"- 来源高校 / University profile: [{name}]({SITE}/{uid}.html)\n"
    # Insert right after the title line (first line starting with '# ')
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("# "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, line.rstrip("\n"))
            break
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    changed += 1

print(f"linked {changed} problem READMEs to their university profiles")
