package gh2;

import deque.Deque61B;
import deque.ArrayDeque61B;

/** 参考实现 / reference implementation（proj1b gh2）。Karplus-Strong 弦振动仿真。 */
public class GuitarString {
    /** 采样率 / sampling rate。 */
    private static final int SR = 44100;
    /** 能量衰减因子 / energy decay factor。 */
    private static final double DECAY = .996;

    private Deque61B<Double> buffer;

    /** 频率 frequency 的弦：buffer 容量 SR/frequency，初始全 0。 */
    public GuitarString(double frequency) {
        int capacity = (int) Math.round(SR / frequency);
        buffer = new ArrayDeque61B<>();
        for (int i = 0; i < capacity; ++i)
            buffer.addLast(0.0);
    }

    /** 拨弦：buffer 换成 [-0.5, 0.5) 白噪声。 */
    public void pluck() {
        int capacity = buffer.size();
        for (int i = 0; i < capacity; ++i) {
            buffer.removeFirst();
            buffer.addLast(Math.random() - 0.5);
        }
    }

    /** 推进一步仿真：出队首样本，压入 DECAY*(首+次)/2。 */
    public void tic() {
        double first = buffer.removeFirst();
        Double secondObj = buffer.get(0);   // removeFirst 后原第二样本已是首元素
        double second = secondObj == null ? 0.0 : secondObj;
        buffer.addLast(DECAY * 0.5 * (first + second));
    }

    /** 当前首样本 / front sample。 */
    public double sample() {
        Double s = buffer.get(0);
        return s == null ? 0.0 : s;
    }
}
