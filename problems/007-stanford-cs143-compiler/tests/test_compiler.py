"""迷你编译器测试：词法、语法树、代码生成、真实执行。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from compiler import lex, Parser, compile_ast, compile_and_run


def main():
    src = """
    let x = 3;
    let y = 4;
    print(x * x + y * y);
    let i = 0;
    while (i < 3) {
        print(i);
        i = i + 1;
    }
    if (x < y) { print(1); } else { print(0); }
    """
    toks, code, out, env = compile_and_run(src)
    print(f"[compiler] tokens({len(toks)}): {toks[:12]} ...")
    print(f"[compiler] instructions({len(code)}): {code[:12]} ...")
    print(f"[compiler] output: {out}")
    assert out == [25, 0, 1, 2, 1], f"unexpected output: {out}"

    # 阶乘程序 / factorial
    fact = """
    let n = 5;
    let result = 1;
    while (n > 1) {
        result = result * n;
        n = n - 1;
    }
    print(result);
    """
    _, _, out2, _ = compile_and_run(fact)
    print(f"[compiler] factorial(5) = {out2}")
    assert out2 == [120]

    # 词法错误 / lex error
    try:
        lex("let a = @;")
        raise AssertionError("should have raised")
    except SyntaxError as e:
        print(f"[compiler] lex error correctly raised: {e}")

    # 语法错误 / parse error
    try:
        compile_and_run("let = 3;")
        raise AssertionError("should have raised")
    except SyntaxError as e:
        print(f"[compiler] parse error correctly raised: {e}")

    print("--- PASS: test_compiler")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
