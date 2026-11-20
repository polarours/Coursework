"""Shell 解析器测试：管道、重定向、引号、变量展开。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from shell import parse


def main():
    cmds = parse("cat input.txt | grep hello > out.txt")
    print(f"[shell] {cmds}")
    assert len(cmds) == 2
    assert cmds[0].argv == ["cat", "input.txt"]
    assert cmds[1].argv == ["grep", "hello"] and cmds[1].output == "out.txt"

    cmds = parse("echo 'hello world' >> log.txt")
    print(f"[shell] {cmds}")
    assert cmds[0].argv == ["echo", "hello world"]
    assert cmds[0].output == "log.txt" and cmds[0].append

    cmds = parse("sort < data.txt")
    assert cmds[0].input == "data.txt"
    print(f"[shell] {cmds}")

    cmds = parse("echo $HOME", {"HOME": "/home/user"})
    assert cmds[0].argv == ["echo", "/home/user"]
    print(f"[shell] {cmds}")

    cmds = parse("wc -l < a.txt | sort | uniq > result.txt")
    print(f"[shell] pipeline of {len(cmds)} commands: {[c.argv for c in cmds]}")
    assert len(cmds) == 3 and cmds[-1].output == "result.txt"

    print("--- PASS: test_shell")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
