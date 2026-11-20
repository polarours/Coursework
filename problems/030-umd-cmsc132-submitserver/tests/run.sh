#!/usr/bin/env bash
# 030 UMD CMSC132 Project1 SubmitServer：官方 PublicTests + 边界补充测试
# upstream 自带学生参考实现（Anna Blendermann），本脚本验证其通过官方测试。
# JUnit4 运行器首次运行自动从 Maven Central 下载。
set -euo pipefail
cd "$(dirname "$0")/.."

LIBS="$HOME/.local/share/java-libs"
J4="$LIBS/junit-4.13.2.jar"
HC="$LIBS/hamcrest-core-1.3.jar"
if [ ! -f "$J4" ] || [ ! -f "$HC" ]; then
  mkdir -p "$LIBS"
  [ -f "$J4" ] || curl -sSL -o "$J4" "https://repo1.maven.org/maven2/junit/junit/4.13.2/junit-4.13.2.jar"
  [ -f "$HC" ] || curl -sSL -o "$HC" "https://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.3/hamcrest-core-1.3.jar"
fi

U="upstream/project1"
BUILD=/tmp/cmsc132_build
rm -rf "$BUILD"; mkdir -p "$BUILD"

echo "== 官方 PublicTests（15 tests）=="
javac -cp "$J4:$HC" -d "$BUILD" "$U/submitserver/SubmitServer.java" "$U/tests/PublicTests.java"
java -cp "$J4:$HC:$BUILD" org.junit.runner.JUnitCore tests.PublicTests | tail -3

echo "== 边界补充测试 =="
javac -cp "$J4:$HC:$BUILD" -d "$BUILD" tests/EdgeTests.java
java -cp "$J4:$HC:$BUILD" org.junit.runner.JUnitCore tests.EdgeTests | tail -3
