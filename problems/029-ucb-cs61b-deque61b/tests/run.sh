#!/usr/bin/env bash
# 029 UC Berkeley CS61B proj1a+1b：Deque61B 完整大作业
# proj1a = LinkedListDeque61B（默认包）；proj1b = ArrayDeque61B +
# Maximizer61B + GuitarString（package deque/gh2）+ 官方 GuitarHero 播放编译验证
# 官方测试依赖课程私有库（jh61b/Truth，未公开），本测试按接口 javadoc 自写。
# JUnit5 运行器与 algs4.jar（播放 demo）首次运行自动下载。
set -euo pipefail
cd "$(dirname "$0")/.."

LIBS="$HOME/.local/share/java-libs"
JUNIT="$LIBS/junit-platform-console-standalone.jar"
ALGS4="$LIBS/algs4.jar"
if [ ! -f "$JUNIT" ]; then
  mkdir -p "$LIBS"
  curl -sSL -o "$JUNIT" \
    "https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.10.2/junit-platform-console-standalone-1.10.2.jar"
fi
if [ ! -f "$ALGS4" ]; then
  mkdir -p "$LIBS"
  curl -sSL -o "$ALGS4" "https://algs4.cs.princeton.edu/code/algs4.jar"
fi

BUILD=/tmp/cs61b_build
rm -rf "$BUILD"; mkdir -p "$BUILD"

# ---- proj1a（默认包）----
javac -cp "$JUNIT" -d "$BUILD" \
  upstream/proj1a/src/Deque61B.java \
  solution/proj1a/LinkedListDeque61B.java \
  tests/proj1a/Deque61BTest.java
echo "== proj1a: LinkedListDeque61B =="
java -jar "$JUNIT" execute -cp "$JUNIT:$BUILD" --select-class Deque61BTest --details=summary | grep -E 'tests (successful|failed)'

# ---- proj1b（package deque / gh2）----
javac -cp "$JUNIT" -d "$BUILD" \
  solution/proj1b/deque/Deque61B.java \
  solution/proj1b/deque/ArrayDeque61B.java \
  solution/proj1b/deque/Maximizer61B.java \
  tests/proj1b/deque/ArrayDeque61BTest.java
javac -cp "$JUNIT:$ALGS4:$BUILD" -d "$BUILD" \
  solution/proj1b/deque/Deque61B.java \
  solution/proj1b/deque/ArrayDeque61B.java \
  solution/proj1b/gh2/GuitarString.java \
  tests/proj1b/gh2/GuitarStringTest.java

echo "== proj1b: ArrayDeque61B + Maximizer61B =="
java -jar "$JUNIT" execute -cp "$JUNIT:$BUILD" --select-class deque.ArrayDeque61BTest --details=summary | grep -E 'tests (successful|failed)'
echo "== proj1b: GuitarString（数值仿真，不播放）=="
java -jar "$JUNIT" execute -cp "$JUNIT:$BUILD" --select-class gh2.GuitarStringTest --details=summary | grep -E 'tests (successful|failed)'

# ---- GuitarHero 播放 demo：编译验证（实时音频不自动播放）----
echo "== gh2 播放 demo 编译验证（GuitarHeroLite/GuitarPlayer/TTFAF，需 algs4）=="
javac -cp "$ALGS4:$BUILD" -d "$BUILD" \
  solution/proj1b/deque/Deque61B.java \
  solution/proj1b/deque/ArrayDeque61B.java \
  solution/proj1b/gh2/GuitarString.java \
  solution/proj1b/gh2/GuitarHeroLite.java \
  solution/proj1b/gh2/GuitarPlayer.java \
  solution/proj1b/gh2/TTFAF.java \
  && echo "播放 demo 编译通过（运行需实时音频设备，不自动执行）"
