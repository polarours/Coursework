"""CMU 15-445 Buffer Pool Manager 的教学版实现（独立编写）。

模拟磁盘页与内存页框，实现 LRU 替换、pin/unpin、脏页写回。
"""

from __future__ import annotations
from collections import OrderedDict
from dataclasses import dataclass, field


@dataclass
class Frame:
    """一个内存页框。index 在缓冲池初始化时绑定，之后不变。"""

    index: int
    page_id: int | None = None
    pin_count: int = 0
    dirty: bool = False
    data: bytes = b""


class DiskManager:
    """模拟磁盘：page_id -> bytes。"""

    def __init__(self):
        self.pages: dict[int, bytes] = {}

    def read(self, page_id: int) -> bytes:
        return self.pages.get(page_id, b"\x00" * 16)

    def write(self, page_id: int, data: bytes) -> None:
        self.pages[page_id] = data


class BufferPoolManager:
    """固定数量页框的缓冲池，LRU 替换（只在 pin_count==0 时可淘汰）。"""

    def __init__(self, num_frames: int, disk: DiskManager):
        self.disk = disk
        self.frames = [Frame(index=i) for i in range(num_frames)]
        self.page_table: dict[int, int] = {}   # page_id -> frame index
        self.lru: OrderedDict[int, None] = OrderedDict()  # frame index，LRU 在前
        self.next_page_id = 0

    def new_page(self) -> tuple[int, Frame | None]:
        """分配一个新页，返回 (page_id, frame)；无可用页框返回 (-1, None)。"""
        frame = self._find_victim()
        if frame is None:
            return -1, None
        page_id = self.next_page_id
        self.next_page_id += 1
        self._free_frame(frame)
        frame.page_id = page_id
        frame.pin_count = 1
        frame.dirty = True
        frame.data = b"\x00" * 16
        self.page_table[page_id] = frame.index
        self._touch(frame.index)
        return page_id, frame

    def fetch_page(self, page_id: int) -> Frame | None:
        """取页：命中则 pin+1；未命中则找 victim 从磁盘读入。"""
        if page_id in self.page_table:
            frame = self.frames[self.page_table[page_id]]
            frame.pin_count += 1
            self._touch(frame.index)
            return frame
        frame = self._find_victim()
        if frame is None:
            return None
        self._free_frame(frame)
        frame.page_id = page_id
        frame.pin_count = 1
        frame.dirty = False
        frame.data = self.disk.read(page_id)
        self.page_table[page_id] = frame.index
        self._touch(frame.index)
        return frame

    def unpin(self, page_id: int, dirty: bool = False) -> bool:
        if page_id not in self.page_table:
            return False
        frame = self.frames[self.page_table[page_id]]
        frame.pin_count = max(0, frame.pin_count - 1)
        if dirty:
            frame.dirty = True
        return True

    def flush(self, page_id: int) -> bool:
        if page_id not in self.page_table:
            return False
        frame = self.frames[self.page_table[page_id]]
        if frame.dirty and frame.page_id is not None:
            self.disk.write(frame.page_id, frame.data)
            frame.dirty = False
            return True
        return False

    def delete_page(self, page_id: int) -> bool:
        if page_id not in self.page_table:
            return False
        idx = self.page_table.pop(page_id)
        frame = self.frames[idx]
        frame.page_id = None
        frame.pin_count = 0
        frame.dirty = False
        frame.data = b""
        self.lru.pop(idx, None)
        return True

    def _find_victim(self) -> Frame | None:
        """优先找空闲页框，再找 pin_count==0 的 LRU 页框。"""
        for f in self.frames:
            if f.page_id is None:
                return f
        for idx in self.lru:
            if self.frames[idx].pin_count == 0:
                return self.frames[idx]
        return None

    def _free_frame(self, frame: Frame) -> None:
        """淘汰前：脏页写回磁盘，清除页表与 LRU 记录。"""
        if frame.page_id is not None:
            if frame.dirty:
                self.disk.write(frame.page_id, frame.data)
            self.page_table.pop(frame.page_id, None)
            self.lru.pop(frame.index, None)

    def _touch(self, idx: int) -> None:
        self.lru.pop(idx, None)
        self.lru[idx] = None

    def stats(self) -> dict:
        return {
            "frames_used": sum(1 for f in self.frames if f.page_id is not None),
            "pinned": sum(1 for f in self.frames if f.pin_count > 0),
            "dirty": sum(1 for f in self.frames if f.dirty),
            "disk_pages": len(self.disk.pages),
        }
