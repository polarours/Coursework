"""xv6 模拟器测试：调度与内存分配。"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from xv6sim import Proc, fcfs, round_robin, mlfq, BuddyAllocator


def procs():
    return [Proc(1, 0, 5), Proc(2, 1, 3), Proc(3, 2, 7)]


def main():
    for name, r in [
        ("FCFS", fcfs(procs())),
        ("RoundRobin(q=2)", round_robin(procs(), 2)),
        ("MLFQ(q=2)", mlfq(procs(), 2)),
    ]:
        print(f"[{name}] order={r.order} timeline={r.timeline} "
              f"avg_wait={r.avg_wait:.2f} avg_turnaround={r.avg_turnaround:.2f}")

    a = BuddyAllocator(64)
    x, y, z = a.alloc(7), a.alloc(8), a.alloc(4)
    print(f"[allocator] alloc(7)={x} alloc(8)={y} alloc(4)={z}")
    print(f"[allocator] blocks before free: {[(b.start,b.size,b.free) for b in a.blocks]}")
    a.free(y)
    print(f"[allocator] after free({y}) free_list={a.free_list()}")
    a.free(x)
    print(f"[allocator] after free({x}) free_list={a.free_list()}")
    assert a.free(x) is False, "double free should fail"
    print("--- PASS: test_xv6sim")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
