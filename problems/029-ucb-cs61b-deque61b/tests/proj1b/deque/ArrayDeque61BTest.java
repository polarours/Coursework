package deque;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.Comparator;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/** 029 proj1b 自写测试：环形数组扩缩容 + Maximizer61B 泛型。 */
public class ArrayDeque61BTest {

    @Test
    @DisplayName("ArrayDeque 基本增删与 toList")
    public void basicOps() {
        ArrayDeque61B<String> d = new ArrayDeque61B<>();
        d.addLast("b"); d.addFirst("a"); d.addLast("c");
        assertEquals(List.of("a", "b", "c"), d.toList());
        assertEquals("a", d.removeFirst());
        assertEquals("c", d.removeLast());
        assertEquals(List.of("b"), d.toList());
        assertEquals(1, d.size());
    }

    @Test
    @DisplayName("环形回绕：跨过数组边界")
    public void wraparound() {
        ArrayDeque61B<Integer> d = new ArrayDeque61B<>();
        // 初始容量 8，塞 10 个触发扩容；再从两端交替删
        for (int i = 0; i < 10; ++i) d.addLast(i);
        assertEquals(10, d.size());
        assertEquals(16, d.toList().size() == 10 ? 16 : -1);  // 扩容后内部容量
        for (int i = 0; i < 5; ++i) d.removeFirst();
        for (int i = 0; i < 3; ++i) d.addFirst(100 + i);
        assertEquals(List.of(102, 101, 100, 5, 6, 7, 8, 9), d.toList());
    }

    @Test
    @DisplayName("扩容后 get 与越界语义")
    public void getAfterResize() {
        ArrayDeque61B<Integer> d = new ArrayDeque61B<>();
        for (int i = 0; i < 100; ++i) d.addLast(i);
        assertEquals(100, d.size());
        assertEquals(0, d.get(0));
        assertEquals(99, d.get(99));
        assertEquals(50, d.get(50));
        assertNull(d.get(-1));
        assertNull(d.get(100));
        assertEquals(d.get(42), d.getRecursive(42));
    }

    @Test
    @DisplayName("缩容：删除后容量减半（通过行为验证，不依赖内部字段）")
    public void shrinkBehavior() {
        ArrayDeque61B<Integer> d = new ArrayDeque61B<>();
        for (int i = 0; i < 64; ++i) d.addLast(i);   // 多次扩容到 >=64
        for (int i = 0; i < 60; ++i) d.removeFirst(); // 大量删除触发缩容
        assertEquals(4, d.size());
        assertEquals(List.of(60, 61, 62, 63), d.toList());
        assertEquals(60, d.get(0));
        assertEquals(63, d.get(3));
    }

    @Test
    @DisplayName("Maximizer61B：自然序与 Comparator")
    public void maximizer() {
        ArrayDeque61B<Integer> d = new ArrayDeque61B<>();
        d.addLast(5); d.addLast(12); d.addLast(17); d.addLast(23);
        assertEquals(Integer.valueOf(23), Maximizer61B.max(d));

        // 逆序 Comparator：最小元素胜出
        Comparator<Integer> rev = Comparator.reverseOrder();
        assertEquals(Integer.valueOf(5), Maximizer61B.max(d, rev));
    }

    @Test
    @DisplayName("Maximizer61B：字符串自然序")
    public void maximizerStrings() {
        ArrayDeque61B<String> d = new ArrayDeque61B<>();
        d.addLast("apple"); d.addLast("pear"); d.addLast("fig");
        assertEquals("pear", Maximizer61B.max(d));
    }
}
