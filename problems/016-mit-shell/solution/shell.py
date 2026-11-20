"""MIT 6.858 风格 shell 的词法/解析器教学版（独立编写）。

支持：命令分割、管道 |、重定向 > < >>、单双引号、环境变量 $VAR 展开。
"""

from __future__ import annotations
import shlex


class Command:
    def __init__(self, argv):
        self.argv: list[str] = argv
        self.input: str | None = None
        self.output: str | None = None
        self.append: bool = False

    def __repr__(self):
        return f"Command({self.argv}, in={self.input}, out={self.output}, append={self.append})"


def parse(line: str, env: dict | None = None) -> list[Command]:
    """把一行命令解析为命令列表（管道分隔）。"""
    env = env or {}
    # 先按 | 分割（简化：不处理引号内的 |）
    segments = [s.strip() for s in line.split("|") if s.strip()]
    commands = []
    for seg in segments:
        tokens = shlex.split(seg)
        cmd = Command([])
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t == ">":
                cmd.output = tokens[i+1]; cmd.append = False; i += 2
            elif t == ">>":
                cmd.output = tokens[i+1]; cmd.append = True; i += 2
            elif t == "<":
                cmd.input = tokens[i+1]; i += 2
            elif t.startswith("$"):
                name = t[1:]
                cmd.argv.append(env.get(name, ""))
                i += 1
            else:
                cmd.argv.append(t)
                i += 1
        commands.append(cmd)
    return commands
