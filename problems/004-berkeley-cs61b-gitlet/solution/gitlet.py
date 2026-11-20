"""CS61B Gitlet 的教学版简化实现（独立于官方框架编写）。

实现内容寻址存储、暂存区、提交图、init/add/commit/log/status/checkout。
所有数据存放在 .gitlet 目录，用 SHA-1 对内容取哈希。
"""

from __future__ import annotations
import hashlib
import os
import pickle
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Commit:
    message: str
    timestamp: float
    parent: str | None
    tree: dict[str, str]  # 文件名 -> blob hash
    uid: str = ""

    def __post_init__(self):
        if not self.uid:
            # uid 必须与 _save_commit 写入的内容哈希一致，否则读不回来
            self.uid = hashlib.sha1(self._serialize()).hexdigest()

    def _serialize(self) -> bytes:
        return pickle.dumps(("commit", self.message, self.timestamp, self.parent, self.tree))


class Gitlet:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.gitdir = self.root / ".gitlet"
        self.objects = self.gitdir / "objects"
        self.refs = self.gitdir / "refs"

    # ---------- 存储原语 / storage primitives ----------
    def _write_object(self, data: bytes) -> str:
        uid = hashlib.sha1(data).hexdigest()
        path = self.objects / uid
        if not path.exists():
            path.write_bytes(data)
        return uid

    def _read_object(self, uid: str) -> bytes:
        return (self.objects / uid).read_bytes()

    def _save_commit(self, c: Commit) -> None:
        data = c._serialize()
        uid = hashlib.sha1(data).hexdigest()
        assert uid == c.uid, "commit uid 必须与内容哈希一致"
        if not (self.objects / uid).exists():
            (self.objects / uid).write_bytes(data)

    def _load_commit(self, uid: str) -> Commit:
        data = pickle.loads(self._read_object(uid))
        assert data[0] == "commit"
        return Commit(data[1], data[2], data[3], data[4], uid)

    def _head(self) -> str:
        return (self.refs / "HEAD").read_text().strip()

    def _set_head(self, uid: str) -> None:
        (self.refs / "HEAD").write_text(uid)

    def _branch(self, name: str) -> str:
        return (self.refs / "heads" / name).read_text().strip()

    def _set_branch(self, name: str, uid: str) -> None:
        (self.refs / "heads" / name).write_text(uid)

    def _current_commit(self) -> Commit:
        return self._load_commit(self._head())

    # ---------- 命令 / commands ----------
    def init(self) -> str:
        self.objects.mkdir(parents=True, exist_ok=True)
        (self.refs / "heads").mkdir(parents=True, exist_ok=True)
        if (self.refs / "HEAD").exists():
            return "A Gitlet version-control system already exists."
        c = Commit("initial commit", 0.0, None, {})
        self._save_commit(c)
        self._set_branch("master", c.uid)
        self._set_head(c.uid)
        return f"Initialized empty Gitlet in {self.gitdir}"

    def add(self, filename: str) -> str:
        path = self.root / filename
        if not path.exists():
            return f"File does not exist: {filename}"
        data = path.read_bytes()
        blob_uid = self._write_object(b"blob:" + data)
        stage = self._load_stage()
        stage[filename] = blob_uid
        self._save_stage(stage)
        return ""

    def _stage_path(self) -> Path:
        return self.gitdir / "stage"

    def _load_stage(self) -> dict[str, str]:
        p = self._stage_path()
        if not p.exists():
            return {}
        return pickle.loads(p.read_bytes())

    def _save_stage(self, stage: dict[str, str]) -> None:
        self._stage_path().write_bytes(pickle.dumps(stage))

    def commit(self, message: str) -> str:
        if not message:
            return "Please enter a commit message."
        stage = self._load_stage()
        if not stage:
            return "No changes added to the commit."
        parent = self._current_commit()
        tree = dict(parent.tree)
        tree.update(stage)
        c = Commit(message, float(len(self._log_uids())), parent.uid, tree)
        self._save_commit(c)
        self._set_head(c.uid)
        self._set_branch(self._current_branch(), c.uid)
        self._save_stage({})
        return f"Committed as {c.uid[:7]}"

    def _current_branch(self) -> str:
        # HEAD 存储的是分支名或 commit uid；本简化版用 refs/heads/master
        return "master"

    def _log_uids(self) -> list[str]:
        out, cur = [], self._head()
        while cur:
            out.append(cur)
            c = self._load_commit(cur)
            cur = c.parent
        return out

    def log(self) -> str:
        lines = []
        for uid in self._log_uids():
            c = self._load_commit(uid)
            lines.append(f"===\ncommit {uid}\nDate: {c.timestamp}\n{c.message}\n")
        return "\n".join(lines)

    def status(self) -> str:
        stage = self._load_stage()
        staged = "Staged files:\n" + "".join(f"  {f}\n" for f in sorted(stage)) if stage else "Staged files: (none)"
        head = self._current_commit()
        return f"=== Current branch: {self._current_branch()}\nHead: {head.uid[:7]}\n{staged}"

    def checkout(self, filename: str) -> str:
        """用当前 HEAD 提交的版本覆盖工作区文件。"""
        c = self._current_commit()
        if filename not in c.tree:
            return f"File {filename} does not exist in the current commit."
        blob = c.tree[filename]
        data = self._read_object(blob)
        (self.root / filename).write_bytes(data.replace(b"blob:", b"", 1))
        return f"Restored {filename} from commit {c.uid[:7]}"
