# 题面要求摘录 / Assignment requirements

> 原文 / Source: <https://cs61c.org/fa26/projects/proj1/>
> 起始仓库 / Starter repo: <https://github.com/61c-teach/sp26-proj1-starter>
> 本文件摘录判定行为所必需的规定，完整措辞以原文为准。
> Only the rules that determine observable behaviour are excerpted here.

## 目标 / Goal

实现一个贪吃蛇游戏引擎：读入棋盘、初始化蛇、推进一个时间步、输出棋盘。

```bash
./snake -i tests/01-simple-in.snk -o out.snk   # 从文件读
./snake --stdin < board.snk                     # 从标准输入读
./snake                                         # 默认棋盘
```

## 棋盘字符 / Board alphabet

| 字符 | 含义 |
|---|---|
| `#` | 墙 |
| ` ` | 空 |
| `*` | 食物 |
| `W A S D` | 蛇头，字母表示朝向（上/左/下/右） |
| `^ < v >` | 蛇身 |
| `w a s d` | 蛇尾（小写，方向与蛇身一致） |
| `x` | 死蛇的头 |

每个蛇格的方向字符同时编码了“下一步往哪走”，因此不需要额外的速度/方向数组。

## 七个任务 / Seven tasks

| Task | 函数 | 要求 |
|---|---|---|
| 1 | `create_default_game` | 18×20 默认棋盘，食物 (2,9)，尾 (2,2)，头 (2,4)，**含 1 条蛇** |
| 2 | `free_game` | 释放棋盘每行、棋盘数组、蛇数组、结构体本身 |
| 3 | `print_board` | 把每行写到给定 `FILE *` |
| 4.1 | 七个 helper | `is_tail`/`is_head`/`is_snake`/`body_to_tail`/`head_to_body`/`get_next_row`/`get_next_col` |
| 4.2 | `next_square` | 返回蛇头将进入的格子字符，不修改任何状态 |
| 4.3 | `update_head` | 旧头变蛇身，新头位置放原头字符，更新结构体 |
| 4.4 | `update_tail` | 旧尾清空，新尾位置由蛇身字符转成尾字符，更新结构体 |
| 4.5 | `update_game` | 推进所有活蛇一步 |
| 5.1 | `read_line` | 用 `fgets` 读一行到堆上，EOF 返回 `NULL` |
| 5.2 | `load_board` | 用 `read_line` 逐行构建棋盘，行长可不同，内存按需分配 |
| 6.1 | `find_head` | 从尾沿方向字符走到头 |
| 6.2 | `initialize_snakes` | 扫描棋盘找所有尾，建蛇数组并填头位置 |
| 7 | `main` | 三条输入路径 + 推进 + 输出 + 释放 |

## 移动规则 / Movement rules

1. 每条活蛇朝头部字符指示的方向移动一格。
2. 头撞墙或撞到**任何**蛇的身体/头（包括自己）→ 蛇死亡，头变成 `x`，之后不再移动。
3. 头进入 `*` → 吃掉食物，长度 +1（只更新头，不更新尾），并调用 `add_food` 生成新食物。
4. 否则头尾都更新，长度不变。

`add_food` 以函数指针传入，`main` 传的是 `snake_utils.c` 里的 `deterministic_food`（确定性伪随机，便于比对）。

## 约束 / Constraints

- `load_board` 必须用 `fgets` 读取，不能用 `fseek`/`rewind`（要支持 stdin）
- 内存按需分配，不能为短行分配大块
- 单元测试 `unit_tests.c` 直接 `#include "game.c"`（为了测 `static` 函数），因此不能与 `game.c` 重复链接
