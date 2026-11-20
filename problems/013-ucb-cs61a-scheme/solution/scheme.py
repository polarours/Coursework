"""UC Berkeley CS61A Scheme 解释器教学版（独立编写）。

支持：quote、原子、define、lambda、if、begin、算术、比较、list 原语。
"""

from __future__ import annotations
from dataclasses import dataclass


class Symbol(str):
    pass


@dataclass
class Procedure:
    params: list[Symbol]
    body: object
    env: "Env"


class Env:
    def __init__(self, parent: "Env | None" = None):
        self.vars: dict[str, object] = {}
        self.parent = parent

    def lookup(self, name: str):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.lookup(name)
        raise NameError(f"unbound symbol: {name}")

    def define(self, name: str, value) -> None:
        self.vars[name] = value


def tokenize(src: str) -> list[str]:
    return src.replace("(", " ( ").replace(")", " ) ").split()


def parse(src: str):
    toks = tokenize(src)
    pos = 0

    def expr():
        nonlocal pos
        t = toks[pos]; pos += 1
        if t == "(":
            lst = []
            while toks[pos] != ")":
                lst.append(expr())
            pos += 1
            return lst
        if t == "'":
            return [Symbol("quote"), expr()]
        if t.lstrip("-").isdigit():
            return int(t)
        return Symbol(t)

    result = expr()
    return result


def scheme_list(items) -> list:
    return list(items)


def car(obj):
    if not isinstance(obj, list) or not obj:
        raise ValueError("car of non-list")
    return obj[0]


def cdr(obj):
    if not isinstance(obj, list) or not obj:
        raise ValueError("cdr of non-list")
    return obj[1:]


def evaluate(expr, env: Env):
    if isinstance(expr, int):
        return expr
    if isinstance(expr, Symbol):
        return env.lookup(str(expr))
    if not isinstance(expr, list):
        return expr
    if not expr:
        raise ValueError("empty application")
    op = expr[0]
    name = str(op) if isinstance(op, Symbol) else None

    if name == "quote":
        return expr[1]
    if name == "define":
        env.define(str(expr[1]), evaluate(expr[2], env))
        return str(expr[1])
    if name == "lambda":
        return Procedure(list(expr[1]), expr[2], env)
    if name == "if":
        cond = evaluate(expr[1], env)
        return evaluate(expr[2] if cond else expr[3], env)
    if name == "begin":
        result = None
        for e in expr[1:]:
            result = evaluate(e, env)
        return result

    # 应用：先求过程，再求参数
    proc = evaluate(op, env)
    args = [evaluate(a, env) for a in expr[1:]]
    return apply_proc(proc, args)


def apply_proc(proc, args):
    # 内置过程（用 Python 名字标记）
    if isinstance(proc, str) and proc.startswith("#builtin:"):
        return BUILTINS[proc[len("#builtin:"):]](*args)
    if isinstance(proc, Procedure):
        new_env = Env(proc.env)
        for p, a in zip(proc.params, args):
            new_env.define(str(p), a)
        return evaluate(proc.body, new_env)
    raise TypeError(f"not a procedure: {proc}")


BUILTINS = {
    "+": lambda *a: sum(a),
    "-": lambda a, b: a - b,
    "*": lambda *a: __import__("math").prod(a),
    "=": lambda a, b: int(a == b),
    "<": lambda a, b: int(a < b),
    ">": lambda a, b: int(a > b),
    "car": car,
    "cdr": cdr,
    "cons": lambda a, b: [a] + list(b),
    "list": lambda *a: list(a),
    "null?": lambda a: int(a == []),
    "print": lambda a: a,
}


def create_global_env() -> Env:
    env = Env()
    for name in BUILTINS:
        env.define(name, "#builtin:" + name)
    return env


def run(src: str) -> object:
    return evaluate(parse(src), create_global_env())
