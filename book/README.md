# 书本构建 / Building the Book

本书用 Quarto 构建，可生成 HTML 网站与 PDF。

## 环境 / Environment

构建环境（conda）：`~/Development_Tools/anaconda3/envs/quarto-book`，Quarto 1.11.9。
如果环境不存在，用以下命令重建（需 conda-forge 可访问）：

```bash
conda create -y -n quarto-book -c conda-forge quarto=1.11.9
# conda 包的 wrapper 缺少 share/version，补一个：
echo "1.11.9" > ~/Development_Tools/anaconda3/envs/quarto-book/share/version
```

## 构建 / Build

用 `scripts/build-book.sh`：

```bash
bash scripts/build-book.sh html   # HTML 网站 → book/_site/
bash scripts/build-book.sh pdf    # PDF（typst 后端）→ book/_book/*.pdf
bash scripts/build-book.sh all    # 两者都构建
```

> 注：PDF 用 typst 后端（`--to typst`），因为本机的 xelatex 字体配置不完整；内容完全相同。

## 结构 / Structure

```text
book/
├── _quarto.yml        # 书籍配置：四卷 + 附录
├── index.qmd          # 前言
├── styles.scss        # 主题
├── references.bib     # 参考文献
├── vol1/              # 卷一：系统基础（3 章）
├── vol2/              # 卷二：算法与数据结构（3 章）
├── vol3/              # 卷三：网络与分布式（2 章）
├── vol4/              # 卷四：智能系统（3 章）
├── vol5/              # 卷五：真实作业集成（导言 + 2 章，023-031 九题）
├── backmatter/        # 总结与阅读指南
├── _site/             # HTML 构建产物（gitignore）
└── _book/             # PDF 构建产物（gitignore）
```

## 内容来源 / Content sources

每章的深入解析与 21 道题的完整 7 章解析位于 `problems/`。书是这些内容的主题化提炼与编排。
