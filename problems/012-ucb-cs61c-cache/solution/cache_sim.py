"""UC Berkeley CS61C Cache Simulator 教学版（独立编写）。

支持直接映射与 N 路组相联；统计 hit/miss/eviction，写回策略。
"""

from __future__ import annotations
from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class CacheSet:
    """一个组：tag -> 最近使用顺序（用 OrderedDict 实现 LRU）。"""
    lines: OrderedDict[int, bool] = None  # type: ignore[assignment]  # tag -> dirty
    max_ways: int = 1

    def __post_init__(self):
        if self.lines is None:
            self.lines = OrderedDict()


class Cache:
    def __init__(self, num_sets: int, block_size: int, ways: int = 1):
        assert (block_size & (block_size - 1)) == 0, "block_size 必须是 2 的幂"
        assert (num_sets & (num_sets - 1)) == 0, "num_sets 必须是 2 的幂"
        self.num_sets = num_sets
        self.block_size = block_size
        self.ways = ways
        self.sets = [CacheSet(max_ways=ways) for _ in range(num_sets)]
        self.hits = self.misses = self.evictions = 0
        self.writebacks = 0

    def _split(self, addr: int) -> tuple[int, int, int]:
        offset = addr % self.block_size
        block_addr = addr // self.block_size
        set_idx = block_addr % self.num_sets
        tag = block_addr // self.num_sets
        return tag, set_idx, offset

    def access(self, addr: int, write: bool = False) -> str:
        tag, s, _ = self._split(addr)
        lines = self.sets[s].lines
        if tag in lines:
            self.hits += 1
            lines.move_to_end(tag)
            if write:
                lines[tag] = True  # 标脏
            return "hit"
        # miss
        self.misses += 1
        if len(lines) >= self.ways:
            _, dirty = lines.popitem(last=False)
            self.evictions += 1
            if dirty:
                self.writebacks += 1
        lines[tag] = write  # 新行，dirty=write
        return "miss"

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "hits": self.hits, "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total else 0,
            "evictions": self.evictions, "writebacks": self.writebacks,
        }
