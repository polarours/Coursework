package gh2;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 029 proj1b gh2：GuitarString 数值仿真验证（不播放音频）。
 * 用固定 buffer 手工注入：构造 440Hz → 容量 44100/440 = 100（round 后）。
 */
public class GuitarStringTest {

    @Test
    @DisplayName("构造：440Hz 容量 100，初始全 0")
    public void construction() {
        GuitarString gs = new GuitarString(440.0);
        // 未拨弦时 sample 应为 0（初始 buffer 全 0）
        assertEquals(0.0, gs.sample(), 1e-12);
        // tic 不应崩溃；首两样本均 0 → 新样本 0
        gs.tic();
        assertEquals(0.0, gs.sample(), 1e-12);
    }

    @Test
    @DisplayName("拨弦：白噪声范围 [-0.5, 0.5)")
    public void pluckRange() {
        GuitarString gs = new GuitarString(440.0);
        gs.pluck();
        // 多次采样（用 tic 轮转 buffer）都在 [-0.5, 0.5)
        for (int i = 0; i < 100; ++i) {
            double s = gs.sample();
            assertTrue(s >= -0.5 && s < 0.5, "sample out of range: " + s);
            gs.tic();
        }
    }

    @Test
    @DisplayName("tic 的 Karplus-Strong 更新：能量衰减")
    public void decay() {
        GuitarString gs = new GuitarString(440.0);
        gs.pluck();
        // 500 步后能量应明显衰减（DECAY=0.996 每步）
        double e0 = energy(gs);
        for (int i = 0; i < 500; ++i) gs.tic();
        double e1 = energy(gs);
        assertTrue(e1 < e0, "能量应衰减: e0=" + e0 + " e1=" + e1);
        assertTrue(e1 > 0, "但不应立刻归零");
    }

    /** 粗略能量：连续 100 个 sample 的平方和。 */
    private double energy(GuitarString gs) {
        double sum = 0;
        for (int i = 0; i < 100; ++i) {
            double s = gs.sample();
            sum += s * s;
            gs.tic();
        }
        return sum;
    }
}
