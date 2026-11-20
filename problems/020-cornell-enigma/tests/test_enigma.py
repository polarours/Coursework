"""Enigma 测试：加解密对称、转子状态、非字母保持。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from enigma import Rotor, Enigma


def make_machine():
    r1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)  # I 型
    r2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4)   # II 型
    r3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21) # III 型
    ref = "YRUHQSLDPXNGOKMIEBFZCWVJAT"          # reflector B
    return Enigma([r1, r2, r3], ref)


def main():
    m1 = make_machine()
    ct = m1.encode("HELLO")
    print(f"[enigma] HELLO -> {ct}")
    assert len(ct) == 5 and ct != "HELLO"

    # 对称性：重置机器后用同样设置解密应得到原文
    m2 = make_machine()
    pt = m2.encode(ct)
    print(f"[enigma] {ct} -> {pt}")
    assert pt == "HELLO"

    # 非字母保持不变
    m3 = make_machine()
    out = m3.encode("HI, WORLD! 123")
    print(f"[enigma] 'HI, WORLD! 123' -> {out}")
    assert out[2] == "," and out[-3:] == "123"

    # 转子推进：连续两次编码同一字母结果不同
    m4 = make_machine()
    a = m4.encode_char("A"); b = m4.encode_char("A")
    print(f"[enigma] consecutive 'A' -> {a}, {b} (should differ)")
    assert a != b

    print("--- PASS: test_enigma")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
