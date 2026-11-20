"""TCP 核心机制的教学版实现（独立于 CS144 官方框架编写）。

实现：ByteStream、Reassembler、TCPReceiver（含 32 位序列号回绕）、
TCPSender（滑动窗口、超时重传、指数退避）。
"""

from __future__ import annotations
from dataclasses import dataclass, field

MOD = 1 << 32


def wrap_add(x: int, n: int) -> int:
    """32 位回绕加法 / 32-bit wrapping addition."""
    return (x + n) % MOD


def wrap_sub(a: int, b: int) -> int:
    """32 位回绕差值 / 32-bit wrapping difference (distance from b to a)."""
    return (a - b) % MOD


class ByteStream:
    """带容量限制的字节流：writer 写入，reader 读取。"""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._buf = bytearray()
        self.eof = False
        self.bytes_popped = 0

    def push(self, data: bytes) -> int:
        """写入数据，返回实际接收的字节数 / returns number of bytes accepted."""
        room = self.capacity - len(self._buf)
        take = data[:room]
        self._buf.extend(take)
        return len(take)

    def close(self) -> None:
        self.eof = True

    def peek(self, n: int) -> bytes:
        return bytes(self._buf[:n])

    def pop(self, n: int) -> bytes:
        n = min(n, len(self._buf))
        out = bytes(self._buf[:n])
        del self._buf[:n]
        self.bytes_popped += n
        return out

    def all_eaten(self) -> bool:
        return self.eof and len(self._buf) == 0

    def remaining(self) -> int:
        return self.capacity - len(self._buf)

    def buffer_size(self) -> int:
        return len(self._buf)


class Reassembler:
    """把乱序到达的子串重组为连续字节流。"""

    def __init__(self, first_index: int, capacity: int):
        self._first = first_index          # 第一个未装配的绝对 index
        self._pending: dict[int, int] = {}  # index -> byte
        self._output = ByteStream(capacity)
        self._eof_index: int | None = None
        self.duplicate_bytes = 0

    def insert(self, index: int, data: bytes, is_last: bool) -> None:
        if is_last:
            self._eof_index = index + len(data)
        for i, b in enumerate(data):
            pos = index + i
            if pos < self._first:
                self.duplicate_bytes += 1
                continue
            self._pending[pos] = b
        self._drain()

    def _drain(self) -> None:
        while self._first in self._pending:
            b = self._pending.pop(self._first)
            if self._output.remaining() == 0:
                # 容量已满：退回，等待 reader 消费（教学版简化为暂停装配）
                self._pending[self._first] = b
                break
            self._output.push(bytes([b]))
            self._first += 1
        if self._eof_index is not None and self._first >= self._eof_index:
            self._output.close()

    def first_unassembled(self) -> int:
        return self._first

    def output(self) -> ByteStream:
        return self._output


@dataclass
class Segment:
    """一个 TCP 段 / a TCP segment."""

    seqno: int
    payload: bytes = b""
    syn: bool = False
    fin: bool = False
    retransmit: int = 0

    def length(self) -> int:
        """占用的序列号个数：SYN/FIN 各占一个 / SYN and FIN each consume one seqno."""
        return len(self.payload) + int(self.syn) + int(self.fin)


class TCPReceiver:
    """接收端：处理 SYN/FIN，重组数据，计算 ackno 与窗口。"""

    def __init__(self, capacity: int, isn: int):
        self.isn = isn
        self._reassembler = Reassembler(0, capacity)
        self.syn_received = False

    def receive(self, seg: Segment) -> None:
        if seg.syn and not self.syn_received:
            self.syn_received = True
            # SYN 之后的 payload 从绝对 index 0 开始
            self._reassembler.insert(0, seg.payload, seg.fin)
            return
        if not self.syn_received:
            return
        data_index = wrap_sub(seg.seqno, wrap_add(self.isn, 1))
        self._reassembler.insert(data_index, seg.payload, seg.fin)

    def ackno(self) -> int | None:
        """确认号 = ISN + 1（SYN）+ 已装配字节数。"""
        if not self.syn_received:
            return None
        return wrap_add(self.isn, 1 + self._reassembler.first_unassembled())

    def window_size(self) -> int:
        return self._reassembler.output().remaining()

    def stream(self) -> ByteStream:
        return self._reassembler.output()


class TCPSender:
    """发送端：滑动窗口、超时重传、指数退避（使用确定性虚拟时钟）。"""

    def __init__(self, stream: ByteStream, isn: int, initial_window: int = 4,
                 initial_rto: int = 10):
        self.stream = stream
        self.isn = isn
        self.window = initial_window
        self.rto = initial_rto
        self.syn_sent = False
        self.fin_sent = False
        self.next_seq = isn
        self.ackno = isn
        self.outstanding: list[Segment] = []
        self.bytes_in_flight = 0
        self.now = 0
        self.timer_running = False
        self.timer_start = 0
        self.consecutive_retrans = 0
        self.retransmission_events: list[Segment] = []

    def send_segments(self) -> list[Segment]:
        """在窗口允许范围内尽可能发送新数据 / fill the window with new segments."""
        sent: list[Segment] = []
        while self.bytes_in_flight < self.window:
            if not self.syn_sent:
                seg = Segment(self.next_seq, b"", syn=True)
                self.syn_sent = True
            else:
                room = self.window - self.bytes_in_flight
                data = self.stream.peek(room)
                if data:
                    seg = Segment(self.next_seq, data)
                    self.stream.pop(len(data))
                elif not self.fin_sent and self.stream.all_eaten():
                    seg = Segment(self.next_seq, b"", fin=True)
                    self.fin_sent = True
                else:
                    break

            length = seg.length()
            if length > self.window - self.bytes_in_flight:
                # 理论上不会发生（room 已限制），保留防御 / defensive guard
                break

            self.outstanding.append(seg)
            self.bytes_in_flight += length
            self.next_seq = wrap_add(self.next_seq, length)
            if not self.timer_running:
                self.timer_running = True
                self.timer_start = self.now
            sent.append(seg)
        return sent

    def receive_ack(self, ackno: int, window: int) -> None:
        """处理 ACK：滑动窗口、移除已确认段、重置或重启定时器。"""
        self.window = max(window, 1)  # 零窗口探测：窗口为 0 时按 1 处理
        advance = wrap_sub(ackno, self.ackno)
        max_advance = wrap_sub(self.next_seq, self.ackno)
        if advance == 0 or advance > max_advance:
            return  # 重复或非法 ACK

        self.ackno = ackno
        while self.outstanding:
            seg = self.outstanding[0]
            if wrap_sub(ackno, seg.seqno) >= seg.length():
                self.bytes_in_flight -= seg.length()
                self.outstanding.pop(0)
            else:
                break

        if not self.outstanding:
            self.timer_running = False
            self.consecutive_retrans = 0
        else:
            self.timer_start = self.now
            self.rto = self._initial_rto
            self.consecutive_retrans = 0

    _initial_rto: int = 10

    def __post_init__(self) -> None:
        self._initial_rto = self.rto

    def tick(self, elapsed: int) -> int:
        """推进虚拟时钟；返回超时重传次数 / advance virtual clock; return #timeouts."""
        self.now += elapsed
        count = 0
        while self.timer_running and self.now - self.timer_start >= self.rto:
            self.timer_start = self.now
            self.rto *= 2  # 指数退避 / exponential backoff
            self.consecutive_retrans += 1
            count += 1
            if self.outstanding:
                earliest = self.outstanding[0]
                earliest.retransmit += 1
                self.retransmission_events.append(earliest)
        return count
