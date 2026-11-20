"""Gitlet 教学实现的测试（固定中性临时目录，真实文件操作）。"""

import sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from gitlet import Gitlet


def main():
    # 使用固定的中性路径，不依赖 TMPDIR（避免输出里出现工具缓存路径）
    root = Path("/tmp/CS61B-workspace")
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    try:
        g = Gitlet(root)

        print("[test_gitlet]", g.init())
        assert (root / ".gitlet" / "objects").is_dir()

        (root / "hello.txt").write_text("hello world\n")
        print("[test_gitlet] add ->", repr(g.add("hello.txt")))
        print("[test_gitlet]", g.commit("first commit"))

        (root / "hello.txt").write_text("hello gitlet\n")
        g.add("hello.txt")
        print("[test_gitlet]", g.commit("second commit"))

        log = g.log()
        print("[test_gitlet] log:\n" + log)
        assert "second commit" in log and "first commit" in log and "initial commit" in log

        status = g.status()
        print("[test_gitlet] status:\n" + status)

        (root / "hello.txt").write_text("broken content\n")
        print("[test_gitlet]", g.checkout("hello.txt"))
        restored = (root / "hello.txt").read_text()
        print(f"[test_gitlet] restored content={restored!r}")
        assert restored == "hello gitlet\n"

        print("--- PASS: test_gitlet")
        print("ALL 1 TEST SUITE PASSED")
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
