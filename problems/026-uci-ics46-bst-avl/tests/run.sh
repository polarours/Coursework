#!/usr/bin/env bash
# 026 UCI ICS46 HW6：用参考实现编译运行自写 gtest
# 说明：upstream 官方 student_gtests.cpp 只有占位用例（真实评测在 Gradescope）
# 本测试按 bst.h 接口语义自写，另含 demo（main.cpp 的 measure 输出）
set -euo pipefail
cd "$(dirname "$0")/.."

g++ -std=c++20 -I solution -I upstream/src tests/tests.cpp \
    solution/bst.cpp solution/bstree.cpp solution/avltree.cpp \
    -lgtest -pthread -o /tmp/ics46_test
/tmp/ics46_test

echo "== demo: measure_BSTs（官方 main.cpp 的行为）=="
g++ -std=c++20 -I solution -I upstream/src \
    solution/bst.cpp solution/bstree.cpp solution/avltree.cpp \
    upstream/src/main.cpp -o /tmp/ics46_main
# main.cpp 用相对路径 src/...，因此在其目录（upstream/）下运行
(cd upstream && /tmp/ics46_main)
