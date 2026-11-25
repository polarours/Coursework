# 题面要求摘录 / Assignment requirements

> 原文 / Source: <https://www.cs.princeton.edu/courses/archive/fall26/cos217/assignment1.php>
> 起始仓库 / Starter repo: <https://github.com/COS217/Decomment>
> 本文件只摘录判定行为所必需的规定，完整措辞以原文为准。
> Only the rules that determine observable behaviour are excerpted here.

## 任务 / The task

写一个 Linux 过滤器 `decomment`：从标准输入读 C 源码，把每个 **C90 注释**替换为一个空格后写到标准输出，错误写到标准错误。

```bash
./decomment < somefile.c > somefileWithoutComments.c 2> errorsAndWarnings
```

## 行为规定 / Behavioural rules

| 规定 / Rule | 含义 / Meaning |
|---|---|
| 注释形式 | 只认 `/* ... */`。`// ...` **不是**注释（C90） |
| 单行注释 | 整段替换为**一个**空格 |
| 多行注释 | 替换为一个空格，再补齐注释内部出现的每个换行，以保持行号 |
| 不识别嵌套 | `/* a /* b */ c */` 在第一个 `*/` 处结束 |
| 字符串字面量 | `"..."` 内的 `/*` 与 `*/` 是普通字符 |
| 字符字面量 | `'...'` 内的 `/*` 与 `*/` 是普通字符 |
| 转义 | 字符串/字符内的 `\` 使下一个字符失去特殊含义 |
| 字面量中的换行 | 允许，不报警告（真实 C 编译器会报错，本题不要求） |
| 未终止的字符串/字符 | 允许，不报警告 |
| 未终止的注释 | 到达 EOF 时注释仍未闭合 → 报错 |
| 行长度 | 必须支持任意长度 |
| 续行 | 可假定输入中不存在 `\` + 换行 |

## 错误格式 / Error format

```
Error: line X: unterminated comment
```

`X` 是注释**开始**的那一行（1 起）。消息写到标准错误。

## 退出码 / Exit status

- 检测到未终止注释 → `EXIT_FAILURE`
- 其他情况 → `EXIT_SUCCESS`

## 挑战部分 / Challenge part

不使用任何**全局变量**（在函数外定义的变量）。类型定义（如 `enum`）不受限制。

> 课程建议的三种做法：把状态处理设计成只需返回一个值；用指针参数回传；用 `struct` 打包多个返回值。本题参考实现采用第三种。
