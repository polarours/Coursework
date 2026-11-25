#!/usr/bin/env bash
# Build and test the Decomment reference implementation.
set -euo pipefail
cd "$(dirname "$0")/.."

BUILD=tests/.build
mkdir -p "$BUILD"

cc -std=c99 -Wall -Wextra -pedantic -O2 -o "$BUILD/decomment" solution/decomment.c
python3 tests/test_decomment.py
