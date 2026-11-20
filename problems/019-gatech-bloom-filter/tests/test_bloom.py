"""布隆过滤器测试：无假阴性、可控假阳性、位数组行为。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from bloom import BloomFilter


def main():
    bf = BloomFilter(size=256, num_hashes=3)
    items = [b"apple", b"banana", b"cherry"]
    for x in items:
        bf.add(x)
    print(f"[bloom] bit_count={bf.bit_count()}/256")
    for x in items:
        assert bf.contains(x), f"假阴性！{x} 应存在"
    print("[bloom] no false negatives for inserted items")

    # 找一批不存在但被误判的项，统计假阳性率
    false_pos = 0
    for i in range(1000):
        if bf.contains(f"absent-{i}".encode()):
            false_pos += 1
    print(f"[bloom] false positives: {false_pos}/1000 = {false_pos/10:.1f}%")
    assert false_pos < 200, "假阳性率过高"

    # 更大过滤器假阳性更低
    bf2 = BloomFilter(size=8192, num_hashes=3)
    for x in items: bf2.add(x)
    fp2 = sum(bf2.contains(f"absent-{i}".encode()) for i in range(1000))
    print(f"[bloom] larger filter false positives: {fp2}/1000")
    assert fp2 <= false_pos

    print("--- PASS: test_bloom")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
