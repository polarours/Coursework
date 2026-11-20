"""Stanford CS155 密码学 lab 教学版：Miller-Rabin、RSA、Merkle 树（独立编写）。"""

from __future__ import annotations
import hashlib
import random


def mod_pow(a: int, d: int, n: int) -> int:
    """快速模幂 / fast modular exponentiation."""
    res = 1
    a %= n
    while d:
        if d & 1:
            res = res * a % n
        a = a * a % n
        d >>= 1
    return res


def is_prime(n: int, rounds: int = 8) -> bool:
    """Miller-Rabin 素性测试（概率性）。"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    rng = random.Random(12345)
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = mod_pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits: int = 16, seed: int = 2024) -> int:
    """生成素数；seed 不同则结果不同（避免固定种子导致重复）。"""
    rng = random.Random(seed)
    while True:
        cand = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(cand):
            return cand


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_inv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    assert g == 1
    return x % m


class RSA:
    def __init__(self, bits: int = 16):
        p = gen_prime(bits, seed=2024)
        q = gen_prime(bits, seed=7777)   # 不同种子 → 不同素数
        while p == q:
            q = gen_prime(bits, seed=7778)
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.e = 65537
        while egcd(self.e, phi)[0] != 1:
            self.e += 2
        self.d = mod_inv(self.e, phi)
        self.p, self.q = p, q

    def encrypt(self, m: int) -> int:
        return mod_pow(m, self.e, self.n)

    def decrypt(self, c: int) -> int:
        return mod_pow(c, self.d, self.n)

    def sign(self, m: int) -> int:
        return mod_pow(m, self.d, self.n)

    def verify(self, m: int, sig: int) -> bool:
        return mod_pow(sig, self.e, self.n) == m


def merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves:
        return hashlib.sha256(b"").digest()
    layer = [hashlib.sha256(x).digest() for x in leaves]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            pair = layer[i] + (layer[i + 1] if i + 1 < len(layer) else layer[i])
            nxt.append(hashlib.sha256(pair).digest())
        layer = nxt
    return layer[0]
