#!/usr/bin/env python3
"""Exercise the exact grading script used in the browser, locally.

The browser runs a Python snippet through Pyodide. This reproduces that snippet
with the CPython on this machine, against both the reference solution (which
must pass every case) and the starter (which must fail at least one). It proves
the comparison logic and the generated expectations are sound, independently of
whether the CDN happens to be reachable from a given network.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(ROOT, "book", "exercises", "problems.json")

SOLUTIONS = {
    "014": "problems/014-princeton-cos226-8puzzle/solution/puzzle.py",
    "018": "problems/018-mit-6602-lru-cache/solution/lru.py",
    "021": "problems/021-stanford-kruskal/solution/kruskal.py",
}

GRADER = r'''
import io, json, contextlib
ns = {}
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(_user_code, ns)
        if _setup:
            exec(_setup, ns)
        got = repr(eval(_expr, ns))
    _result = json.dumps({"ok": got == _expect, "got": got, "printed": buf.getvalue()})
except BaseException as exc:
    _result = json.dumps({"ok": False, "got": "", "error": repr(exc), "printed": buf.getvalue()})
'''


def grade(code, test):
    g = {"_user_code": code, "_setup": test["setup"],
         "_expr": test["expr"], "_expect": test["expect"]}
    exec(compile(GRADER, "<grader>", "exec"), g)
    return json.loads(g["_result"])


def main():
    bank = json.load(open(BANK, encoding="utf-8"))
    failures = []
    for p in bank:
        solution = open(os.path.join(ROOT, SOLUTIONS[p["id"]]), encoding="utf-8").read()
        passed = 0
        for t in p["tests"]:
            r = grade(solution, t)
            if r["ok"]:
                passed += 1
            else:
                failures.append(f"{p['id']} {t['name']}: expected {t['expect']}, got {r}")
        starter_hits = sum(1 for t in p["tests"] if grade(p["starter"], t)["ok"])
        print(f"{p['id']}: solution {passed}/{len(p['tests'])} pass; "
              f"starter {starter_hits}/{len(p['tests'])} pass")
        if passed != len(p["tests"]):
            failures.append(f"{p['id']}: reference solution did not pass all cases")
        if starter_hits:
            failures.append(f"{p['id']}: starter already passes {starter_hits} cases — too easy")

    if failures:
        print("\nPROBLEMS:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll cases: reference passes, starter fails. Grading script verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
