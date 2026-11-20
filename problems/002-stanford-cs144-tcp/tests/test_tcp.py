"""CS144 TCP 教学实现的测试（确定性，无真实 sleep）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))

from tcp import (ByteStream, Reassembler, Segment, TCPReceiver, TCPSender,
                 wrap_add, wrap_sub, MOD)


def test_reassembler():
    r = Reassembler(0, 64)
    r.insert(3, b"def", False)
    r.insert(0, b"abc", False)
    r.insert(2, b"cde", False)  # 与已有数据部分重叠
    r.insert(6, b"g", True)
    out = r.output()
    print(f"[test_reassembler] first_unassembled={r.first_unassembled()}")
    print(f"[test_reassembler] stream={out.peek(100)!r} eof={out.eof} "
          f"duplicate_bytes={r.duplicate_bytes}")
    assert out.peek(100) == b"abcdefg"
    assert out.eof
    assert r.duplicate_bytes > 0


def test_wraparound():
    isn = MOD - 5
    assert wrap_add(isn, 10) == 5                 # MOD-5 + 10 = 5
    assert wrap_sub(5, isn) == 10
    print(f"[test_wraparound] ISN={isn} +10 -> {wrap_add(isn, 10)}, "
          f"distance back = {wrap_sub(wrap_add(isn, 10), isn)}")


def test_receiver():
    isn = 1000
    rx = TCPReceiver(64, isn)
    # SYN seqno = 1000, 之后数据 seqno = 1001
    rx.receive(Segment(isn, b"", syn=True))
    print(f"[test_receiver] after SYN ackno={rx.ackno()} window={rx.window_size()}")
    assert rx.ackno() == 1001
    rx.receive(Segment(wrap_add(isn, 6), b"world", fin=True))  # 乱序：先发 index 5
    rx.receive(Segment(wrap_add(isn, 1), b"hello"))            # 再补 index 0
    print(f"[test_receiver] after reassembly ackno={rx.ackno()} "
          f"stream={rx.stream().peek(100)!r} eof={rx.stream().eof}")
    assert rx.ackno() == 1011
    assert rx.stream().peek(100) == b"helloworld"
    assert rx.stream().eof


def test_sender_retransmission():
    stream = ByteStream(64)
    stream.push(b"abcdefgh")
    stream.close()
    tx = TCPSender(stream, isn=500, initial_window=4, initial_rto=10)
    sent = tx.send_segments()
    print(f"[test_sender_retransmission] sent={sent}")
    assert sent[0].syn and len(sent[0].payload) == 0
    n = tx.tick(10)
    print(f"[test_sender_retransmission] tick(10) -> timeouts={n}, "
          f"rto={tx.rto}, retransmit_events={len(tx.retransmission_events)}")
    assert n == 1 and tx.rto == 20
    n = tx.tick(9)
    print(f"[test_sender_retransmission] tick(9) -> timeouts={n} (should be 0)")
    assert n == 0
    n = tx.tick(11)
    print(f"[test_sender_retransmission] tick(11) -> timeouts={n}, rto={tx.rto}")
    assert n == 1 and tx.rto == 40


def test_sender_window_and_ack():
    stream = ByteStream(64)
    stream.push(b"abcdefghij")
    stream.close()
    tx = TCPSender(stream, isn=0, initial_window=4, initial_rto=10)
    first = tx.send_segments()
    payloads = [s.payload for s in first if s.payload]
    print(f"[test_sender_window_and_ack] window=4 first flight payloads={payloads}")
    assert b"".join(payloads) == b"abc"
    # ack 到 SYN+abc：seqno 0(SYN) 1..3(abc) => ackno=4
    tx.receive_ack(4, 4)
    more = tx.send_segments()
    payloads2 = [s.payload for s in more if s.payload]
    print(f"[test_sender_window_and_ack] after ACK(4) next flight payloads={payloads2}")
    assert b"".join(payloads2) == b"defg"
    # 确认 defg（ackno 从 4 前进到 8）
    tx.receive_ack(8, 4)
    rest = tx.send_segments()  # 剩余 hij + FIN，共 3+1=4 字节
    print(f"[test_sender_window_and_ack] final flight={rest}")
    assert rest[-1].fin and b"".join(s.payload for s in rest) == b"hij"
    # 确认全部（8 + hij 3 + FIN 1 = 12）
    tx.receive_ack(12, 4)
    print(f"[test_sender_window_and_ack] after final ACK: outstanding={len(tx.outstanding)} "
          f"timer_running={tx.timer_running} fin_sent={tx.fin_sent}")
    assert len(tx.outstanding) == 0 and not tx.timer_running


def test_end_to_end():
    """发送端字节流 -> 段 -> 接收端字节流（无丢失）。"""
    src = ByteStream(64)
    src.push(b"the quick brown fox")
    src.close()
    tx = TCPSender(src, isn=12345, initial_window=8, initial_rto=10)
    rx = TCPReceiver(64, isn=12345)
    delivered: list[Segment] = []
    for _ in range(20):
        for seg in tx.send_segments():
            delivered.append(seg)
            rx.receive(seg)
        if tx.fin_sent and not tx.outstanding:
            break
        ack = rx.ackno()
        win = rx.window_size()
        if ack is not None:
            tx.receive_ack(ack, win)
    result = rx.stream().peek(100)
    print(f"[test_end_to_end] segments={len(delivered)} result={result!r} "
          f"eof={rx.stream().eof}")
    assert result == b"the quick brown fox"
    assert rx.stream().eof


def main():
    tests = [test_reassembler, test_wraparound, test_receiver,
             test_sender_retransmission, test_sender_window_and_ack,
             test_end_to_end]
    for t in tests:
        t()
        print(f"--- PASS: {t.__name__}")
    print(f"ALL {len(tests)} TESTS PASSED")


if __name__ == "__main__":
    main()
