"""MIT 6.1810 (xv6) 核心 lab 的教学版模拟器（独立编写）。

模拟：进程调度（FCFS / Round Robin / MLFQ）与内存分配（隐式空闲链表 + 首次适应）。
"""

from __future__ import annotations
from dataclasses import dataclass, field


# ---------------------------------------------------------------- 进程调度

@dataclass
class Proc:
    pid: int
    arrival: int
    burst: int          # 总 CPU 时间
    priority: int = 1   # 数字越小优先级越高
    remaining: int = 0
    wait_time: int = 0
    turnaround: int = 0
    last_run: int = 0   # 上次运行结束时刻（用于正确计算等待）
    origin: int = 0     # 最初到达时刻（不被重新入队修改）

    def __post_init__(self):
        self.remaining = self.burst
        self.last_run = self.arrival
        self.origin = self.arrival


@dataclass
class ScheduleResult:
    order: list[int] = field(default_factory=list)
    timeline: list[tuple[int, int]] = field(default_factory=list)  # (pid, duration)
    avg_wait: float = 0.0
    avg_turnaround: float = 0.0

    def finish(self, procs: list[Proc]):
        # 只补仍未被各算法显式设置的 turnaround
        for p in procs:
            if not p.turnaround:
                p.turnaround = p.wait_time + p.burst
        self.avg_wait = sum(p.wait_time for p in procs) / len(procs)
        self.avg_turnaround = sum(p.turnaround for p in procs) / len(procs)


def fcfs(procs: list[Proc]) -> ScheduleResult:
    """先来先服务：按到达时间排序，非抢占。"""
    r = ScheduleResult()
    t = 0
    for p in sorted(procs, key=lambda x: (x.arrival, x.pid)):
        t = max(t, p.arrival)
        p.wait_time = t - p.arrival
        r.order.append(p.pid)
        r.timeline.append((p.pid, p.burst))
        t += p.burst
        p.turnaround = t - p.arrival
    r.finish(procs)
    return r


def round_robin(procs: list[Proc], quantum: int) -> ScheduleResult:
    """时间片轮转：就绪队列 FIFO，每次运行至多 quantum。"""
    r = ScheduleResult()
    queue = sorted(procs, key=lambda x: x.origin)
    t = 0
    while queue:
        p = queue.pop(0)
        if p.origin > t:
            t = p.origin
        p.wait_time += t - p.last_run       # 从上次运行结束到现在的等待
        run = min(quantum, p.remaining)
        r.order.append(p.pid)
        r.timeline.append((p.pid, run))
        t += run
        p.remaining -= run
        p.last_run = t
        if p.remaining > 0:
            queue.append(p)
        else:
            p.turnaround = t - p.origin
    r.finish(procs)
    return r


def mlfq(procs: list[Proc], quantum: int, n_queues: int = 3) -> ScheduleResult:
    """多级反馈队列：高层时间片小；用完时间片降级；I/O 让出保持层级（教学简化）。"""
    r = ScheduleResult()
    queues: list[list[Proc]] = [[] for _ in range(n_queues)]
    t = 0
    remaining = sorted(procs, key=lambda x: x.origin)
    while remaining or any(queues):
        while remaining and remaining[0].origin <= t:
            p = remaining.pop(0)
            queues[0].append(p)
        # 找最高优先级非空队列
        for qi, q in enumerate(queues):
            if q:
                p = q.pop(0)
                p.wait_time += t - p.last_run
                qrun = quantum * (2 ** qi)  # 低优先级时间片更长
                run = min(qrun, p.remaining)
                r.order.append(p.pid)
                r.timeline.append((p.pid, run))
                t += run
                p.remaining -= run
                p.last_run = t
                if p.remaining > 0:
                    next_q = min(qi + 1, n_queues - 1)
                    queues[next_q].append(p)
                else:
                    p.turnaround = t - p.origin
                break
        else:
            if remaining:
                t = remaining[0].origin
    r.finish(procs)
    return r


# ---------------------------------------------------------------- 内存分配

@dataclass
class Block:
    start: int
    size: int
    free: bool = True


class BuddyAllocator:
    """简化的伙伴分配器：按需分裂，释放后与空闲伙伴合并。"""

    def __init__(self, total: int):
        self.total = total
        self.blocks = [Block(0, total, True)]

    def alloc(self, size: int) -> int | None:
        # 向上取整到 2 的幂
        target = 1 << (size - 1).bit_length() if size > 1 else 1
        for i, b in enumerate(self.blocks):
            if b.free and b.size >= target:
                while b.size > target:
                    half = b.size // 2
                    b.size = half
                    self.blocks.insert(i + 1, Block(b.start + half, half, True))
                    b = self.blocks[i]
                b.free = False
                return b.start
        return None

    def free(self, start: int) -> bool:
        for i, b in enumerate(self.blocks):
            if b.start == start and not b.free:
                b.free = True
                self._coalesce()
                return True
        return False

    def _coalesce(self):
        changed = True
        while changed:
            changed = False
            self.blocks.sort(key=lambda b: b.start)
            for i in range(len(self.blocks) - 1):
                a, b = self.blocks[i], self.blocks[i + 1]
                if a.free and b.free and a.start + a.size == b.start and a.size == b.size:
                    a.size *= 2
                    del self.blocks[i + 1]
                    changed = True
                    break

    def free_list(self) -> list[tuple[int, int]]:
        return [(b.start, b.size) for b in self.blocks if b.free]
