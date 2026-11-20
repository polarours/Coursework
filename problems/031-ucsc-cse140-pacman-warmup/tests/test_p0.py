"""031 UCSC CSE140 p0：CS188 风格 warmup 测试
期望输出直接来自题目注释（buyLotsOfFruit.py / shopSmart.py docstring）。"""
import sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))

from buyLotsOfFruit import buyLotsOfFruit, FRUIT_PRICES
from shopSmart import shopSmart
from shop import FruitShop


def test_buyLots():
    order = [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)]
    assert abs(buyLotsOfFruit(order) - 12.25) < 1e-9, \
        "题目注释期望 12.25"

def test_buyLots_missing_fruit():
    assert buyLotsOfFruit([('durian', 1.0)]) is None, \
        "店里没有的水果应返回 None"

def test_buyLots_empty():
    assert buyLotsOfFruit([]) == 0.0

def test_shopSmart():
    dir1 = {'apples': 2.0, 'oranges': 1.0}
    dir2 = {'apples': 1.0, 'oranges': 5.0}
    shop1 = FruitShop('shop1', dir1)
    shop2 = FruitShop('shop2', dir2)
    shops = [shop1, shop2]

    # 题目注释期望的两个用例
    order1 = [('apples', 1.0), ('oranges', 3.0)]   # shop1: 2+3=5, shop2: 1+15=16
    assert shopSmart(order1, shops) is shop1
    order2 = [('apples', 3.0)]                    # shop1: 6, shop2: 3
    assert shopSmart(order2, shops) is shop2

def test_shopSmart_expected_output():
    """跑 shopSmart.py 的 main，对照题目注释的输出。"""
    out = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent.parent / "solution" / "shopSmart.py")],
        capture_output=True, text=True, timeout=30).stdout
    # 注：upstream 的 docstring 写 "best shop is shop1."，但 shop.py 的 main
    # 实际打印 "the best shop is shop1."（题目注释与代码输出有一处不一致）
    assert "For orders: [('apples', 1.0), ('oranges', 3.0)] the best shop is shop1." in out
    assert "For orders: [('apples', 3.0)] the best shop is shop2." in out

def test_buyLots_expected_output():
    out = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent.parent / "solution" / "buyLotsOfFruit.py")],
        capture_output=True, text=True, timeout=30).stdout
    assert "Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25" in out


if __name__ == "__main__":
    for name, fn in sorted([(n, f) for n, f in globals().items() if n.startswith("test_")]):
        fn()
        print(f"[PASS] {name}")
    print("ALL TESTS PASSED")
