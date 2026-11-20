"""Scheme 解释器测试：算术、递归、list 原语、词法作用域。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from scheme import run, parse, create_global_env, evaluate


def main():
    cases = [
        ("(+ 1 2 3)", 6),
        ("(* 2 3 4)", 24),
        ("(- 10 3)", 7),
        ("(if (< 1 2) 100 200)", 100),
        ("(car (list 1 2 3))", 1),
        ("(cdr (list 1 2 3))", [2, 3]),
        ("(cons 0 (list 1 2))", [0, 1, 2]),
        ("(null? (list))", 1),
    ]
    for src, expect in cases:
        got = run(src)
        print(f"[scheme] {src} => {got}")
        assert got == expect, f"{src}: got {got}, expect {expect}"

    # 递归阶乘：define + lambda + if
    fact = """
    (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
    (fact 5)
    """
    # run 只返回最后一个表达式，但 define 与调用需要同一环境，手动串起来
    env = create_global_env()
    evaluate(parse("(define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))"), env)
    result = evaluate(parse("(fact 5)"), env)
    print(f"[scheme] factorial(5) = {result}")
    assert result == 120

    # 词法作用域 / closure
    closure = """
    (define make-adder (lambda (x) (lambda (y) (+ x y))))
    """
    evaluate(parse(closure), env)
    evaluate(parse("(define add5 (make-adder 5))"), env)
    r2 = evaluate(parse("(add5 3)"), env)
    print(f"[scheme] closure add5(3) = {r2}")
    assert r2 == 8

    print("--- PASS: test_scheme")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
