#!/usr/bin/env bash
# 用参考实现运行原始 doctest 测试
# main.cpp 放在 tests/ 目录，#include "AList.h" 会通过 -I solution 找到参考实现
set -euo pipefail
cd "$(dirname "$0")/.."
g++ -std=c++17 -I solution tests/main.cpp -o /tmp/alist_test
/tmp/alist_test
