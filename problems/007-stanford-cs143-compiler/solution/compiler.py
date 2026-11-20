"""Stanford CS143 编译器教学版：词法 → 语法 → AST → 栈式虚拟机代码 → 执行。

独立于官方框架编写的迷你编译器，编译一个带变量、算术、比较与 if/while/print 的语言。
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


# ---------------------------------------------------------------- 1. 词法分析

@dataclass
class Token:
    type: str
    value: str
    pos: int

    def __repr__(self):
        return f"Token({self.type},{self.value!r})"


KEYWORDS = {"if", "else", "while", "print", "let", "true", "false"}


def lex(src: str) -> list[Token]:
    toks = []
    i = 0
    n = len(src)
    while i < n:
        ch = src[i]
        if ch.isspace():
            i += 1
        elif ch.isalpha():
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            word = src[i:j]
            toks.append(Token(word if word in KEYWORDS else "ID", word, i))
            i = j
        elif ch.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            toks.append(Token("NUM", src[i:j], i))
            i = j
        elif src[i:i+2] in ("<=", ">=", "==", "!="):
            toks.append(Token("OP", src[i:i+2], i))
            i += 2
        elif ch in "<>":
            # 单字符比较符归为 OP，与双字符（<= >=）一致；= 留给赋值
            toks.append(Token("OP", ch, i))
            i += 1
        elif ch in "+-*/();{}=,":
            toks.append(Token(ch, ch, i))
            i += 1
        else:
            raise SyntaxError(f"未知字符 {ch!r} @ {i}")
    toks.append(Token("EOF", "", n))
    return toks


# ---------------------------------------------------------------- 2. AST 节点

@dataclass
class Num: value: int
@dataclass
class Var: name: str
@dataclass
class Bin: op: str; left: Any; right: Any
@dataclass
class Assign: name: str; expr: Any
@dataclass
class Print: expr: Any
@dataclass
class If: cond: Any; then: list; els: list
@dataclass
class While: cond: Any; body: list
@dataclass
class Block: stmts: list


# ---------------------------------------------------------------- 3. 递归下降语法分析

class Parser:
    def __init__(self, toks: list[Token]):
        self.toks = toks
        self.i = 0

    def peek(self) -> Token:
        return self.toks[self.i]

    def eat(self, t: str) -> Token:
        tok = self.peek()
        if tok.type != t:
            raise SyntaxError(f"期望 {t}，实际 {tok.type} @ {tok.pos}")
        self.i += 1
        return tok

    def parse(self) -> Block:
        return self.block()

    def block(self) -> Block:
        stmts = []
        while self.peek().type not in ("EOF", "}"):
            stmts.append(self.stmt())
            # 语句以分号结束（if/while 的花括号块本身已消费结束符）
            if self.peek().type == ";":
                self.eat(";")
        return Block(stmts)

    def stmt(self) -> Any:
        t = self.peek().type
        if t == "print":
            self.eat("print"); self.eat("(")
            e = self.expr(); self.eat(")")
            return Print(e)
        if t == "let":
            self.eat("let")
            name = self.eat("ID").value
            self.eat("=")
            return Assign(name, self.expr())
        if t == "if":
            self.eat("if"); self.eat("(")
            cond = self.expr(); self.eat(")")
            then = self.block_no_brace()
            els = []
            if self.peek().type == "else":
                self.eat("else")
                els = self.block_no_brace()
            return If(cond, then, els)
        if t == "while":
            self.eat("while"); self.eat("(")
            cond = self.expr(); self.eat(")")
            return While(cond, self.block_no_brace())
        if t == "ID":
            name = self.eat("ID").value
            self.eat("=")
            return Assign(name, self.expr())
        raise SyntaxError(f"未知语句 {self.peek()}")

    def block_no_brace(self) -> list:
        self.eat("{")
        b = self.block()
        self.eat("}")
        return b.stmts

    def expr(self) -> Any:
        return self.compare()

    def compare(self) -> Any:
        node = self.add()
        while self.peek().type == "OP" and self.peek().value in ("<", ">", "<=", ">=", "==", "!="):
            op = self.eat("OP").value
            node = Bin(op, node, self.add())
        return node

    def add(self) -> Any:
        node = self.mul()
        while self.peek().type in ("+", "-"):
            op = self.eat(self.peek().type).value
            node = Bin(op, node, self.mul())
        return node

    def mul(self) -> Any:
        node = self.atom()
        while self.peek().type in ("*", "/"):
            op = self.eat(self.peek().type).value
            node = Bin(op, node, self.atom())
        return node

    def atom(self) -> Any:
        tok = self.peek()
        if tok.type == "ID":
            return Var(self.eat("ID").value)
        if tok.type == "NUM":
            return Num(int(self.eat("NUM").value))
        if tok.type == "(":
            self.eat("("); e = self.expr(); self.eat(")")
            return e
        raise SyntaxError(f"期望表达式，实际 {tok}")


# ---------------------------------------------------------------- 4. 代码生成（栈式虚拟机）

def compile_ast(node: Any, code: list) -> None:
    if isinstance(node, Num):
        code.append(("PUSH", node.value))
    elif isinstance(node, Var):
        code.append(("LOAD", node.name))
    elif isinstance(node, Bin):
        compile_ast(node.left, code)
        compile_ast(node.right, code)
        code.append(("BINOP", node.op))
    elif isinstance(node, Assign):
        compile_ast(node.expr, code)
        code.append(("STORE", node.name))
    elif isinstance(node, Print):
        compile_ast(node.expr, code)
        code.append(("PRINT",))
    elif isinstance(node, Block):
        for s in node.stmts:
            compile_ast(s, code)
    elif isinstance(node, If):
        compile_ast(node.cond, code)
        jf = len(code); code.append(("JZ", None))
        for s in node.then: compile_ast(s, code)
        if node.els:
            jmp = len(code); code.append(("JMP", None))
            code[jf] = ("JZ", len(code))
            for s in node.els: compile_ast(s, code)
            code[jmp] = ("JMP", len(code))
        else:
            code[jf] = ("JZ", len(code))
    elif isinstance(node, While):
        start = len(code)
        compile_ast(node.cond, code)
        jz = len(code); code.append(("JZ", None))
        for s in node.body: compile_ast(s, code)
        code.append(("JMP", start))
        code[jz] = ("JZ", len(code))
    else:
        raise TypeError(f"未知 AST 节点 {node}")


BINOPS = {
    "+": lambda a, b: a + b, "-": lambda a, b: a - b,
    "*": lambda a, b: a * b, "/": lambda a, b: a // b,
    "<": lambda a, b: int(a < b), ">": lambda a, b: int(a > b),
    "<=": lambda a, b: int(a <= b), ">=": lambda a, b: int(a >= b),
    "==": lambda a, b: int(a == b), "!=": lambda a, b: int(a != b),
}


def execute(code: list, out: list) -> dict:
    stack, env, pc = [], {}, 0
    while pc < len(code):
        op = code[pc]
        kind = op[0]
        if kind == "PUSH": stack.append(op[1])
        elif kind == "LOAD": stack.append(env.get(op[1], 0))
        elif kind == "STORE": env[op[1]] = stack.pop()
        elif kind == "BINOP":
            b = stack.pop(); a = stack.pop()
            stack.append(BINOPS[op[1]](a, b))
        elif kind == "PRINT": out.append(stack.pop())
        elif kind == "JZ":
            if stack.pop() == 0: pc = op[1]; continue
        elif kind == "JMP":
            pc = op[1]; continue
        pc += 1
    return env


def compile_and_run(src: str) -> tuple[list[Token], list, list, dict]:
    toks = lex(src)
    ast = Parser(toks).parse()
    code: list = []
    compile_ast(ast, code)
    out: list = []
    env = execute(code, out)
    return toks, code, out, env
