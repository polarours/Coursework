#!/usr/bin/env bash
# 028 Clemson CPSC2121 Lab 1：官方 13 个样例用例 + 边界测试
# solution 为 upstream 学生实现的修复版（修 5 处真实缺陷，见 README）
set -euo pipefail
cd "$(dirname "$0")/.."
CASES="upstream/Lab 1 - Linked List Based Stacks and Queues/Lab 1 Sample Test Cases"

pass=0; fail=0
for t in "$CASES"/T*.cpp; do
  name=$(basename "$t" .cpp)
  if g++ -std=c++17 -I solution -I "upstream/Lab 1 - Linked List Based Stacks and Queues" "$t" -o "/tmp/clem_$name" 2>/tmp/clem_err.log \
     && "/tmp/clem_$name" >/dev/null 2>&1; then
    echo "[PASS] $name (官方样例)"; pass=$((pass+1))
  else
    echo "[FAIL] $name"; fail=$((fail+1))
  fi
done
echo "官方样例: $pass passed, $fail failed"
[ "$fail" -eq 0 ] || exit 1

echo "== 边界测试（官方用例未覆盖的空表/空栈语义）=="
g++ -std=c++17 -I solution -I "upstream/Lab 1 - Linked List Based Stacks and Queues" tests/edge.cpp -o /tmp/clem_edge
/tmp/clem_edge
