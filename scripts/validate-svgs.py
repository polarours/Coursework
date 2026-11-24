#!/usr/bin/env python3
"""Fail the build if any SVG in the book is not well-formed XML.

A generated nameplate once used `&nbsp;`, which browsers silently refuse to
render (broken image) while curl still returned HTTP 200. Validating here
catches that class of error before deployment.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(
    set(glob.glob(os.path.join(ROOT, "assets", "*.svg")))
    | set(glob.glob(os.path.join(ROOT, "book", "universities", "logos", "*.svg")))
)
bad = []
for path in files:
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        bad.append(f"{os.path.relpath(path, ROOT)}: {exc}")
if bad:
    print("Invalid SVG assets:")
    for item in bad:
        print(" -", item)
    sys.exit(1)
print(f"Validated {len(files)} SVG assets")
