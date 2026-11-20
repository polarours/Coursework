#!/usr/bin/env bash
# 025 UCI ECS36C HW1：用参考实现运行 gtest 测试
# LinkedList 测试来自 upstream（已激活的 4 个官方用例）；
# Stack/Queue 测试基于官方示例解除注释 + 接口语义补全
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== LinkedList tests (upstream official) =="
g++ -std=c++17 -I solution -I upstream/lib upstream/tests/LinkedListTest.cpp \
    -lgtest -lgtest_main -pthread -o /tmp/hw1_ll
/tmp/hw1_ll

echo "== Stack & Queue tests =="
g++ -std=c++17 -I solution -I upstream/lib tests/StackQueueTest.cpp \
    -lgtest -lgtest_main -pthread -o /tmp/hw1_sq
/tmp/hw1_sq
