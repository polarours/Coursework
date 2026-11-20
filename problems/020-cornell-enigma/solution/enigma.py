"""Cornell CS3110 A1 Enigma 风格转子密码机教学版（独立编写）。

实现转子旋转、替换映射与加解密（Enigma 是对称的：加密函数同样用于解密）。
"""

from __future__ import annotations
from string import ascii_uppercase as ALPHA


class Rotor:
    def __init__(self, mapping: str, notch: int):
        assert len(mapping) == 26 and set(mapping) == set(ALPHA)
        self.wiring = [ALPHA.index(c) for c in mapping]
        self.pos = 0
        self.notch = notch

    def forward(self, ch: str) -> str:
        idx = (ALPHA.index(ch) + self.pos) % 26
        out = self.wiring[idx]
        return ALPHA[(out - self.pos) % 26]

    def rotate(self) -> bool:
        """转一格；返回是否到达 notch（触发下一个转子）。"""
        self.pos = (self.pos + 1) % 26
        return self.pos == self.notch


class Enigma:
    def __init__(self, rotors, reflector: str):
        self.rotors = rotors
        self.reflector = [ALPHA.index(c) for c in reflector]

    def _step(self):
        # 最右转子每次转；到 notch 时级联（简化：全部级联）
        for i in reversed(range(len(self.rotors))):
            if not self.rotors[i].rotate():
                break

    def encode_char(self, ch: str) -> str:
        self._step()
        x = ch.upper()
        for r in self.rotors:
            x = r.forward(x)
        idx = ALPHA.index(x)
        x = ALPHA[self.reflector[idx]]
        for r in reversed(self.rotors):
            # 反向穿过转子：找 wiring 中等于 (index+pos)%26 的位置
            target = (ALPHA.index(x) + r.pos) % 26
            orig = r.wiring.index(target)
            x = ALPHA[(orig - r.pos) % 26]
        return x

    def encode(self, text: str) -> str:
        return "".join(self.encode_char(c) if c.isalpha() else c for c in text)
