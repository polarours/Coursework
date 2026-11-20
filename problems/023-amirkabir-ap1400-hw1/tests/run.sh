#!/usr/bin/env bash
# 用参考实现运行原始 gtest 测试（原测试被 /* */ 注释，此处用激活版）
# 本机 gtest 1.18 要求 C++17（原作业 C++14），这是环境适配
set -euo pipefail
cd "$(dirname "$0")/.."
g++ -std=c++17 -I solution tests/unit_test_active.cpp solution/hw1.cpp \
    -lgtest -lgtest_main -pthread -o /tmp/hw1_gtest
/tmp/hw1_gtest
