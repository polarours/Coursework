"""Georgia Tech 风格布隆过滤器教学版（独立编写）。

用 k 个哈希函数映射到位数组；假阳性可能，假阴性不可能。
"""

from __future__ import annotations
import hashlib


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        assert size > 0 and num_hashes > 0
        self.size = size
        self.num_hashes = num_hashes
        self.bits = bytearray(size)

    def _hashes(self, item: bytes):
        """用 SHA-256 派生 k 个独立哈希。"""
        h = hashlib.sha256(item).digest()
        for i in range(self.num_hashes):
            chunk = hashlib.sha256(h + str(i).encode()).digest()
            yield int.from_bytes(chunk[:8], "big") % self.size

    def add(self, item: bytes):
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def contains(self, item: bytes) -> bool:
        return all(self.bits[idx] for idx in self._hashes(item))

    def bit_count(self):
        return sum(self.bits)
