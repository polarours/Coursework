#!/usr/bin/env bash
# 032 UCSC CSE140 p1：Pacman 搜索大作业（pacai v2.1.0）
# 官方评测在课程 autograder（不公开），本地按题面语义设计用例矩阵：
#   board 与问题的正确配对：maze-* → position，corners-* → corners，search-* → food/greedy
# 断言锚点：Record: Win + Path found 的 steps/cost/expanded 数
set -euo pipefail
cd "$(dirname "$0")/.."

# ---- 依赖自举 / harness bootstrap ----
VENV="$HOME/.local/share/pacai-venv"
if [ ! -x "$VENV/bin/python" ] || ! "$VENV/bin/python" -c "import PIL, edq.util.serial" 2>/dev/null; then
  echo "== 构建 pacai venv（Pillow + edq-utils，PyPI 直连）=="
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q Pillow edq-utils
fi

# ---- 构建副本树（upstream 原样保留，student 文件替换为 solution）----
BUILD=/tmp/pacai_build/pacai-tree
rm -rf /tmp/pacai_build; mkdir -p /tmp/pacai_build
cp -r upstream "$BUILD"
cp solution/singlesearch.py "$BUILD/pacai/student/singlesearch.py"

run_case() {   # run_case <期望标签> <args...>
  local label="$1"; shift
  local out
  out=$(timeout 120 env PYTHONPATH="$BUILD" "$VENV/bin/python" -m pacai.pacman "$@" 2>&1 \
        | grep -E 'Record:|Path found' | head -2)
  local win steps
  win=$(echo "$out" | grep -oE 'Win|Loss' | head -1)
  steps=$(echo "$out" | grep -oE 'with [0-9]+ steps and a total cost of [0-9.]+' | head -1)
  if [ "$win" = "Win" ]; then
    echo "[PASS] $label — $steps"
  else
    echo "[FAIL] $label (record=$win)"; echo "$out" | head -4
    return 1
  fi
}

fail=0

echo "== Q1 位置搜索：maze-tiny 四求解器 =="
run_case "DFS  位置搜索" --board maze-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-position --agent-arg 0::solver=search-solver-dfs || fail=1
run_case "BFS  位置搜索" --board maze-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-position --agent-arg 0::solver=search-solver-bfs || fail=1
run_case "UCS  位置搜索" --board maze-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-position --agent-arg 0::solver=search-solver-ucs || fail=1
run_case "A*   位置搜索（曼哈顿启发）" --board maze-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-position --agent-arg 0::solver=search-solver-astar \
  --agent-arg 0::heuristic=heuristic-manhattan || fail=1

echo "== Q2 四角问题：corners-tiny + corners-medium =="
run_case "A*+corners_h corners-tiny" --board corners-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-corners --agent-arg 0::solver=search-solver-astar \
  --agent-arg 0::heuristic=heuristic-corners || fail=1
run_case "A*+corners_h corners-medium（大板）" --board corners-medium --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-corners --agent-arg 0::solver=search-solver-astar \
  --agent-arg 0::heuristic=heuristic-corners || fail=1

echo "== Q3 食物搜索 =="
run_case "A*+food_h search-tiny" --board search-tiny --pacman agent-search-problem \
  --agent-arg 0::problem=search-problem-food --agent-arg 0::solver=search-solver-astar \
  --agent-arg 0::heuristic=heuristic-food || fail=1

echo "== Q4/Q5 贪心与近似 =="
run_case "ClosestDot search-medium" --board search-medium --pacman agent-search-closest-dot || fail=1
run_case "Approximate search-medium" --board search-medium --pacman agent-search-approx || fail=1

# ---- 最优性交叉验证：BFS/UCS/A* 的 steps 应一致（跑一次提取）----
echo "== 最优性交叉验证（BFS/UCS/A* 同 cost；DFS 只需到达）=="
for slv in bfs ucs astar; do
  timeout 60 env PYTHONPATH="$BUILD" "$VENV/bin/python" -m pacai.pacman --board maze-tiny \
    --pacman agent-search-problem --agent-arg 0::problem=search-problem-position \
    --agent-arg 0::solver=search-solver-$slv \
    --agent-arg 0::heuristic=heuristic-manhattan 2>&1 \
    | grep -oE 'total cost of [0-9.]+' | head -1 | sed "s/^/$slv: /"
done

if [ "$fail" -eq 0 ]; then echo "ALL CASES PASSED"; else echo "SOME CASES FAILED"; exit 1; fi
