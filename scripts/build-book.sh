#!/usr/bin/env bash
# 构建书籍：HTML 与 PDF 并存 / Build the book as HTML and PDF side by side
# Quarto book 每次 render 会清空并重建整个 _book 目录，
# 因此先把 HTML 产物移出 _book（到 _site），再构建 PDF，
# 最后把 PDF 复制回 _site，让站点可以直接下载。
set -euo pipefail

E="$HOME/Development_Tools/anaconda3/envs/quarto-book"
export QUARTO_DENO="$E/bin/deno"
export QUARTO_DENO_DOM="$E/lib/libdeno_dom.so"
export QUARTO_PANDOC="$E/bin/pandoc"
export QUARTO_ESBUILD="$E/bin/esbuild"
export QUARTO_TYPST="$E/bin/typst"
export QUARTO_TYPST_GATHER="$E/bin/typst-gather"
export QUARTO_DART_SASS="$E/bin/sass"
export QUARTO_SHARE_PATH="$E/share/quarto"
export QUARTO_CONDA_PREFIX="$E"

cd "$(dirname "$0")/../book"
target="${1:-all}"

# Quarto 以书名生成 PDF 文件名（含中文与中点），改成稳定的 ASCII 名，
# 避开 URL 编码问题，也让下载链接可以写死。
PDF_NAME="coursework-atlas.pdf"

build_html() {
  "$E/bin/quarto" render --to html
  rm -rf _site
  mv _book _site
  echo "HTML -> _site/"
}

build_pdf() {
  "$E/bin/quarto" render --to typst
  local produced
  produced=$(find _book -maxdepth 1 -name '*.pdf' -print -quit)
  if [ -z "$produced" ]; then
    echo "错误：未生成 PDF" >&2
    return 1
  fi
  mkdir -p _site
  cp "$produced" "_site/$PDF_NAME"
  echo "PDF  -> _site/$PDF_NAME"
}

case "$target" in
  html) build_html ;;
  pdf)  build_pdf ;;
  all)  build_html && build_pdf ;;
  *) echo "用法: build-book.sh [html|pdf|all]"; exit 1 ;;
esac
