#!/usr/bin/env bash
# 运行 Raft 参考实现的全部测试（真实执行，输出见 05-调试与测试.md）
set -euo pipefail
cd "$(dirname "$0")/../solution"
go test ./... -v -count=1 -timeout 120s
