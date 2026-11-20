"""Stanford CS231n 两层神经网络教学版（纯 Python 矩阵运算；独立编写）。

结构：输入 -> 全连接(W1,b1) -> ReLU -> 全连接(W2,b2) -> Softmax + 交叉熵。
手动实现前向/反向传播，在合成数据上训练。
"""

from __future__ import annotations
import math
import random


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    rows, k, cols = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(cols)]
            for i in range(rows)]


def rowsum(A: list[list[float]]) -> list[float]:
    return [sum(row) for row in A]


def softmax(scores: list[list[float]]) -> list[list[float]]:
    out = []
    for row in scores:
        m = max(row)
        exps = [math.exp(x - m) for x in row]
        s = sum(exps)
        out.append([e / s for e in exps])
    return out


class TwoLayerNet:
    def __init__(self, D: int, H: int, C: int, seed: int = 42):
        rng = random.Random(seed)
        self.W1 = [[rng.gauss(0, 0.1) for _ in range(H)] for _ in range(D)]
        self.b1 = [0.0] * H
        self.W2 = [[rng.gauss(0, 0.1) for _ in range(C)] for _ in range(H)]
        self.b2 = [0.0] * C

    def forward(self, X: list[list[float]]) -> tuple[list[list[float]], tuple]:
        Z1 = [[sum(X[i][d] * self.W1[d][h] for d in range(len(X[0]))) + self.b1[h]
               for h in range(len(self.W1[0]))] for i in range(len(X))]
        A1 = [[max(0, z) for z in row] for row in Z1]
        scores = [[sum(A1[i][h] * self.W2[h][c] for h in range(len(A1[0]))) + self.b2[c]
                   for c in range(len(self.W2[0]))] for i in range(len(A1))]
        probs = softmax(scores)
        return probs, (X, Z1, A1, scores)

    def loss(self, probs: list[list[float]], y: list[int]) -> float:
        n = len(y)
        return -sum(math.log(max(probs[i][y[i]], 1e-12)) for i in range(n)) / n

    def accuracy(self, probs: list[list[float]], y: list[int]) -> float:
        return sum(1 for i in range(len(y)) if max(range(len(probs[i])), key=lambda c: probs[i][c]) == y[i]) / len(y)

    def backward(self, probs: list[list[float]], y: list[int], cache: tuple, lr: float) -> None:
        X, Z1, A1, _ = cache
        n = len(y)
        # dScores
        dS = [row[:] for row in probs]
        for i in range(n):
            dS[i][y[i]] -= 1
        dS = [[v / n for v in row] for row in dS]
        # W2 梯度：dW2[h][c] = sum_i A1[i][h] * dS[i][c]
        H, C = len(self.W2), len(self.W2[0])
        dW2 = [[sum(A1[i][h] * dS[i][c] for i in range(n)) for c in range(C)] for h in range(H)]
        db2 = rowsum(dS)
        # 反向过全连接层：dA1 = dS @ W2^T，W2^T 形状为 C×H
        W2_T = [[self.W2[h][c] for h in range(H)] for c in range(C)]
        dA1 = matmul(dS, W2_T)  # n×C @ C×H -> n×H
        # 反向过 ReLU：Z1<=0 处梯度置零
        dZ1 = [[dA1[i][h] if Z1[i][h] > 0 else 0.0 for h in range(H)] for i in range(n)]
        D, _ = len(self.W1), len(self.W1[0])
        dW1 = [[sum(X[i][d] * dZ1[i][h] for i in range(n)) for h in range(H)] for d in range(D)]
        db1 = rowsum(dZ1)
        # SGD 更新
        for d in range(D):
            for h in range(H):
                self.W1[d][h] -= lr * dW1[d][h]
        for h in range(H):
            self.b1[h] -= lr * db1[h]
        for h in range(H):
            for c in range(C):
                self.W2[h][c] -= lr * dW2[h][c]
        for c in range(C):
            self.b2[c] -= lr * db2[c]

    def train(self, X: list[list[float]], y: list[int], epochs: int, lr: float,
              verbose: bool = False) -> list[float]:
        losses = []
        for ep in range(epochs):
            probs, cache = self.forward(X)
            loss = self.loss(probs, y)
            losses.append(loss)
            self.backward(probs, y, cache, lr)
            if verbose and (ep % 100 == 0 or ep == epochs - 1):
                print(f"  epoch {ep:4d} loss={loss:.4f} acc={self.accuracy(probs, y):.3f}")
        return losses


def make_spiral(n_per_class: int = 60, classes: int = 3, seed: int = 1):
    """生成螺旋形合成数据（CS231n 经典 toy dataset 的平缓版）。

    圈数 2π、半径范围较小——保证纯 Python 实现在数百轮内能收敛，
    同时仍是非线性可分问题，能体现隐藏层与 ReLU 的作用。
    """
    rng = random.Random(seed)
    X, y = [], []
    for c in range(classes):
        for i in range(n_per_class):
            r = 0.3 + i / n_per_class * 2.5
            t = i / n_per_class * 2 * math.pi + c * 2 * math.pi / classes
            X.append([r * math.sin(t) + rng.gauss(0, 0.08),
                      r * math.cos(t) + rng.gauss(0, 0.08)])
            y.append(c)
    return X, y
