#!/usr/bin/env bash
# Build and test the CS61C "snek" reference implementation.
#
# Two layers, both from the official starter:
#   1. the 21 integration tests (input board -> reference board after one tick)
#   2. the 1708-line official unit test suite for the individual tasks
set -euo pipefail
cd "$(dirname "$0")/.."

BUILD=tests/.build
rm -rf "$BUILD"
mkdir -p "$BUILD"

cc -std=c99 -Wall -Wextra -O2 -o "$BUILD/snake" \
   solution/snake.c solution/game.c solution/snake_utils.c

cc -std=c99 -Wall -O2 -o "$BUILD/unit-tests" \
   solution/unit_tests.c solution/snake_utils.c solution/asserts.c

pass=0
fail=0
for f in upstream/tests/*-in.snk; do
  base=$(basename "$f" -in.snk)
  out="$BUILD/$base-out.snk"
  if "$BUILD/snake" -i "$f" -o "$out" 2>/dev/null &&
     diff -q "$out" "upstream/tests/$base-ref.snk" >/dev/null 2>&1; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    echo "FAIL: $base"
  fi
done
echo "integration tests: $pass passed, $fail failed"
[ "$fail" -eq 0 ] || exit 1

# The unit tests read boards through the relative path "tests/...", so give
# them a working directory that has one.
ln -sfn "$(cd upstream/tests && pwd)" "$BUILD/tests"
if (cd "$BUILD" && ./unit-tests > unit-tests.log 2>&1); then
  echo "unit tests: PASS"
else
  echo "unit tests: FAIL"
  tail -25 "$BUILD/unit-tests.log"
  exit 1
fi

echo
echo "ALL PASS"
