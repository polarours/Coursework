#!/usr/bin/env bash
# 027 CCNY CSC212 Lab 07：回溯三题（N-Queens/Sudoku/Sujiko）参考实现测试
set -euo pipefail
cd "$(dirname "$0")/.."
INC="upstream/Labs/Lab 07 Backtracking/scaffolding"
g++ -std=c++17 -I solution -I "$INC/N_Queens" -I "$INC/Sudoku" -I "$INC/Sujiko" \
    tests/tests.cpp solution/n_queens.cpp solution/sudoku.cpp solution/sujiko.cpp \
    -o /tmp/csc212_bt
/tmp/csc212_bt
