"""MIT 6.006/6.006 风格 LRU Cache 教学版（独立编写）。

用哈希表 + 双向链表实现 O(1) get/put；容量满时淘汰最久未使用项。
"""

from __future__ import annotations


class Node:
    __slots__ = ("key", "value", "prev", "next")
    def __init__(self, key=None, value=None):
        self.key, self.value = key, value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        assert capacity > 0
        self.capacity = capacity
        self.map: dict = {}
        # 哨兵：head.next 是 MRU，tail.prev 是 LRU
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head
        self.evictions = 0

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key not in self.map:
            return None
        node = self.map[key]
        self._remove(node); self._add_front(node)   # 提升为 MRU
        return node.value

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._remove(node); self._add_front(node)
            return
        if len(self.map) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
            self.evictions += 1
        node = Node(key, value)
        self._add_front(node)
        self.map[key] = node

    def keys_mru_to_lru(self):
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur.key)
            cur = cur.next
        return out
