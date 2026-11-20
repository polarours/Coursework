"""密码学实现测试：RSA 加解密/签名、Merkle 树、素性测试。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from crypto import RSA, is_prime, mod_pow, merkle_root
import hashlib


def main():
    primes = [n for n in range(2, 200) if is_prime(n)]
    print(f"[crypto] primes under 200 (count={len(primes)}): {primes[:15]} ...")
    assert 2 in primes and 199 in primes and 4 not in primes
    assert mod_pow(2, 10, 1000) == 24

    rsa = RSA(16)
    print(f"[crypto] RSA n={rsa.n} (p={rsa.p}, q={rsa.q}), e={rsa.e}, d={rsa.d}")
    m = 4242
    c = rsa.encrypt(m)
    dec = rsa.decrypt(c)
    print(f"[crypto] encrypt({m})={c}; decrypt -> {dec}")
    assert dec == m
    sig = rsa.sign(m)
    print(f"[crypto] sign({m}) verified: {rsa.verify(m, sig)}; tampered: {rsa.verify(m+1, sig)}")
    assert rsa.verify(m, sig) and not rsa.verify(m + 1, sig)

    leaves = [b"tx1", b"tx2", b"tx3", b"tx4"]
    root = merkle_root(leaves)
    print(f"[crypto] merkle root = {root.hex()[:32]} ...")
    print(f"[crypto] root changes on tamper: {merkle_root([b'tx1',b'BAD',b'tx3',b'tx4']) != root}")
    assert merkle_root(leaves) == merkle_root(leaves)
    assert merkle_root([b"tx1", b"BAD", b"tx3", b"tx4"]) != root

    print("--- PASS: test_crypto")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
