"""两层神经网络测试：前向、反向、训练收敛。"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "solution"))
from nn import TwoLayerNet, make_spiral


def main():
    X, y = make_spiral(60, 3)
    print(f"[nn] dataset: {len(X)} samples, {len(set(y))} classes")
    net = TwoLayerNet(D=2, H=32, C=3, seed=42)
    probs, _ = net.forward(X)
    init_loss = net.loss(probs, y)
    print(f"[nn] initial loss={init_loss:.4f} acc={net.accuracy(probs, y):.3f}")
    assert abs(sum(probs[0]) - 1.0) < 1e-9, "softmax 概率和应为 1"

    losses = net.train(X, y, epochs=600, lr=1.0, verbose=True)
    probs, _ = net.forward(X)
    final_loss = losses[-1]
    final_acc = net.accuracy(probs, y)
    print(f"[nn] final loss={final_loss:.4f} acc={final_acc:.3f}")
    print(f"[nn] loss reduced: {final_loss < init_loss * 0.5}")
    assert final_loss < init_loss * 0.5, "训练后 loss 应显著下降"
    assert final_acc > 0.85, "训练后准确率应超过 85%"

    print("--- PASS: test_nn")
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
