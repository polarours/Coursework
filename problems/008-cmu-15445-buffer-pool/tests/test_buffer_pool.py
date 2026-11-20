"""Buffer Pool Manager 测试（LRU 替换、pin 保护、脏页写回）。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from buffer_pool import DiskManager, BufferPoolManager


def main():
    disk = DiskManager()
    bpm = BufferPoolManager(3, disk)  # 3 个页框

    p0, f0 = bpm.new_page()
    p1, _ = bpm.new_page()
    p2, _ = bpm.new_page()
    print(f"[bpm] new_page -> {p0},{p1},{p2}; stats={bpm.stats()}")
    assert (p0, p1, p2) == (0, 1, 2)
    assert bpm.stats()["frames_used"] == 3

    # 全部 unpin；p0 标记为脏并写入数据
    f0.data = b"HELLO-DATA-0123"
    bpm.unpin(p0, dirty=True)
    bpm.unpin(p1)
    bpm.unpin(p2)
    print(f"[bpm] after unpin: stats={bpm.stats()}")

    # 访问 p0 使它成为 MRU；此时 LRU 顺序应为 p1, p2, p0
    bpm.fetch_page(p0)
    bpm.unpin(p0)
    print(f"[bpm] LRU order (frame idx) = {list(bpm.lru.keys())}")

    # 池已满，new_page 必须淘汰 LRU（p1）。验证 p1 被换出、p0 仍在。
    p3, _ = bpm.new_page()
    print(f"[bpm] new_page with full pool -> {p3}; stats={bpm.stats()}")
    assert p3 == 3
    assert p1 not in bpm.page_table, "p1 (LRU) 应被淘汰"
    assert p0 in bpm.page_table, "p0 (MRU) 应保留"
    assert p2 in bpm.page_table, "p2 应保留"

    # 脏页 p0 flush 到磁盘
    ok = bpm.flush(p0)
    print(f"[bpm] flush(p0)={ok}; disk pages={sorted(disk.pages.keys())}")
    assert ok and disk.pages[p0] == b"HELLO-DATA-0123"

    # pin 保护的页不能被淘汰：pin 住 p0，反复 new_page
    bpm.fetch_page(p0)  # pin_count 增加
    for _ in range(6):
        pid, _ = bpm.new_page()
        if pid == -1:
            break
        bpm.unpin(pid)
    still = p0 in bpm.page_table
    print(f"[bpm] pinned page {p0} survived evictions: {still}; stats={bpm.stats()}")
    assert still, "被 pin 的页不应被淘汰"

    # delete_page 清理页表
    bpm.unpin(p0)
    deleted = bpm.delete_page(p0)
    print(f"[bpm] delete_page({p0})={deleted}; stats={bpm.stats()}")
    assert deleted and p0 not in bpm.page_table

    print("--- PASS: test_buffer_pool")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
