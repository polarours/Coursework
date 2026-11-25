#!/usr/bin/env python3
"""Test suite for the COS 217 Decomment assignment.

Two independent layers:

1. Golden cases transcribed from the assignment specification. Each entry is
   an (input, expected stdout, expected stderr, expected exit code) tuple
   taken verbatim from the published spec tables, so a failure here means the
   implementation disagrees with Princeton's own examples.

2. The 70+ sample inputs shipped in the official starter repository. The spec
   does not publish expected outputs for those files, so they are checked
   against an independent Python oracle written with a different structure
   (index-based scanning rather than a streaming getchar loop). This catches
   drift without pretending to be an official reference.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BINARY = os.path.join(ROOT, "tests", ".build", "decomment")
UPSTREAM = os.path.join(ROOT, "upstream")

# (name, input, expected stdout, expected stderr, expected exit code)
GOLDEN = [
    ("single-line comment replaced by one space",
     "abc/*def*/ghi\n", "abc ghi\n", "", 0),
    ("trailing space after comment is kept",
     "abc/*def*/ ghi\n", "abc  ghi\n", "", 0),
    ("space before comment is kept",
     "abc /*def*/ghi\n", "abc  ghi\n", "", 0),
    ("double slash is not a C90 comment",
     "abc//def\n", "abc//def\n", "", 0),
    ("multi-line comment collapses to space plus newline",
     "abc/*def\nghi*/jkl\nmno\n", "abc \njkl\nmno\n", "", 0),
    ("multi-line comment keeps every newline",
     "abc/*def\nghi\njkl*/mno\npqr\n", "abc \n\nmno\npqr\n", "", 0),
    ("nested comment start is not special",
     "abc/*def/*ghi*/jkl*/mno\n", "abc jkl*/mno\n", "", 0),
    ("comment markers inside a string are literal",
     'abc"def/*ghi*/jkl"mno\n', 'abc"def/*ghi*/jkl"mno\n', "", 0),
    ("comment containing quotes still closes",
     'abc/*def"ghi"jkl*/mno\n', "abc mno\n", "", 0),
    ("comment containing an opening quote still closes",
     'abc/*def"ghijkl*/mno\n', "abc mno\n", "", 0),
    ("comment markers inside a char literal are literal",
     "abc'def/*ghi*/jkl'mno\n", "abc'def/*ghi*/jkl'mno\n", "", 0),
    ("comment containing char quotes still closes",
     "abc/*def'ghi'jkl*/mno\n", "abc mno\n", "", 0),
    ("comment containing an opening char quote still closes",
     "abc/*def'ghijkl*/mno\n", "abc mno\n", "", 0),
    ("escaped quote does not end the string",
     'abc"def\\"ghi"jkl\n', 'abc"def\\"ghi"jkl\n', "", 0),
    ("escaped single quote inside a string is literal",
     'abc"def\\\'ghi"jkl\n', 'abc"def\\\'ghi"jkl\n', "", 0),
    ("comment after an escaped-quote string is removed",
     'abc"def\\"ghi"jkl/*mno*/pqr\n', 'abc"def\\"ghi"jkl pqr\n', "", 0),
    ("escaped backslash ends the string before the comment",
     'abc"def\\\\"ghi"jkl/*mno*/pqr"stu\n',
     'abc"def\\\\"ghi"jkl/*mno*/pqr"stu\n', "", 0),
    ("escaped quote does not end the char literal",
     "abc'def\\'ghi'jkl\n", "abc'def\\'ghi'jkl\n", "", 0),
    ("escaped double quote inside a char literal is literal",
     "abc'def\\\"ghi'jkl\n", "abc'def\\\"ghi'jkl\n", "", 0),
    ("comment after an escaped-quote char literal is removed",
     "abc'def\\'ghi'jkl/*mno*/pqr\n", "abc'def\\'ghi'jkl pqr\n", "", 0),
    ("newline inside a string is allowed",
     'abc"def\nghi"jkl\n', 'abc"def\nghi"jkl\n', "", 0),
    ("comment after a multi-line string is removed",
     'abc"def\nghi\njkl"mno/*pqr*/stu\n',
     'abc"def\nghi\njkl"mno stu\n', "", 0),
    ("newline inside a char literal is allowed",
     "abc'def\nghi'jkl\n", "abc'def\nghi'jkl\n", "", 0),
    ("comment after a multi-line char literal is removed",
     "abc'def\nghi\njkl'mno/*pqr*/stu\n",
     "abc'def\nghi\njkl'mno stu\n", "", 0),
    ("unterminated string swallows the comment",
     'abc"def/*ghi*/jkl\n', 'abc"def/*ghi*/jkl\n', "", 0),
    ("unterminated char literal swallows the comment",
     "abc'def/*ghi*/jkl\n", "abc'def/*ghi*/jkl\n", "", 0),
    ("unterminated comment reports its first line",
     "abc/*def\nghi\n", "abc \n\n",
     "Error: line 1: unterminated comment\n", 1),
    ("unterminated comment on line 2",
     "abc\ndef/*ghi\njkl\n", "abc\ndef \n\n",
     "Error: line 2: unterminated comment\n", 1),
    ("stray slash inside a comment does not close it",
     "abc/*def/ghi\njkl\n", "abc \n\n",
     "Error: line 1: unterminated comment\n", 1),
    ("single star inside a comment does not close it",
     "abc/*def*ghi\njkl\n", "abc \n\n",
     "Error: line 1: unterminated comment\n", 1),
    ("star at end of line does not close the comment",
     "abc/*def\nghi*\n", "abc \n\n",
     "Error: line 1: unterminated comment\n", 1),
    ("slash at end of line does not close the comment",
     "abc/*def\nghi/\n", "abc \n\n",
     "Error: line 1: unterminated comment\n", 1),
    ("empty input yields empty output",
     "", "", "", 0),
    ("empty comment becomes a single space",
     "/**/\n", " \n", "", 0),
    ("comment at start of file",
     "/*x*/abc\n", " abc\n", "", 0),
    ("two adjacent comments give two spaces",
     "a/*x*//*y*/b\n", "a  b\n", "", 0),
    ("trailing slash at end of file is emitted",
     "abc/", "abc/", "", 0),
    ("file ending in an opener is unterminated",
     "abc/*", "abc ", "Error: line 1: unterminated comment\n", 1),
]


def oracle(text):
    """Independent reference: index-based scan, not a streaming automaton."""
    out = []
    i, n = 0, len(text)
    line = 1
    while i < n:
        ch = text[i]

        # Look ahead for a comment opener anywhere outside literals.
        if text.startswith("/*", i):
            start_line = line
            out.append(" ")          # the comment collapses to one space...
            i += 2
            closed = False
            while i < n:
                if text.startswith("*/", i):
                    i += 2
                    closed = True
                    break
                if text[i] == "\n":
                    line += 1
                    out.append("\n")
                i += 1
            if not closed:
                return "".join(out), start_line
            continue

        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            while i < n:
                out.append(text[i])
                if text[i] == "\\" and i + 1 < n:
                    out.append(text[i + 1])
                    if text[i + 1] == "\n":
                        line += 1
                    i += 2
                    continue
                if text[i] == quote:
                    i += 1
                    break
                if text[i] == "\n":
                    line += 1
                i += 1
            continue

        if ch == "\n":
            line += 1
        out.append(ch)
        i += 1
    return "".join(out), None


def run_binary(data):
    proc = subprocess.run([BINARY], input=data.encode(), capture_output=True)
    return (proc.stdout.decode(errors="replace"),
            proc.stderr.decode(errors="replace"),
            proc.returncode)


def main():
    failures = []

    # Layer 1: specification examples.
    for name, src, want_out, want_err, want_code in GOLDEN:
        got_out, got_err, got_code = run_binary(src)
        if (got_out, got_err, got_code) != (want_out, want_err, want_code):
            failures.append(
                f"GOLDEN: {name}\n  input   {src!r}\n"
                f"  expected out={want_out!r} err={want_err!r} code={want_code}\n"
                f"  got      out={got_out!r} err={got_err!r} code={got_code}")
    print(f"golden cases: {len(GOLDEN) - len(failures)}/{len(GOLDEN)} passed")

    # Layer 2: official sample inputs against the independent oracle.
    files = sorted(f for f in os.listdir(UPSTREAM) if f.endswith(".txt"))
    mismatches = 0
    for name in files:
        with open(os.path.join(UPSTREAM, name), encoding="utf-8", errors="replace") as fh:
            src = fh.read()
        want_out, unterminated = oracle(src)
        want_err = (f"Error: line {unterminated}: unterminated comment\n"
                    if unterminated else "")
        want_code = 1 if unterminated else 0
        got_out, got_err, got_code = run_binary(src)
        if (got_out, got_err, got_code) != (want_out, want_err, want_code):
            mismatches += 1
            failures.append(
                f"ORACLE: {name}\n  expected code={want_code} err={want_err!r}\n"
                f"  got      code={got_code} err={got_err!r}\n"
                f"  out match: {got_out == want_out}")
    print(f"oracle cases: {len(files) - mismatches}/{len(files)} passed")

    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f in failures[:12]:
            print(f)
        return 1
    print("\nALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
