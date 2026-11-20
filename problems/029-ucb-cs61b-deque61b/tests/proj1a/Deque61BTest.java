import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * 029 自写测试。说明：upstream 官方 LinkedListDeque61BTest 的示例用例全部
 * 处于注释状态（CS61B 鼓励学生先写测试），且依赖课程私有库 jh61b/Truth（不在
 * 公开仓库）。本文件按 Deque61B.java 的接口 javadoc 语义编写。
 */
public class Deque61BTest {

    @Test
    @DisplayName("addFirst / addLast / toList 基本顺序")
    public void addFirstAndAddLast() {
        LinkedListDeque61B<String> d = new LinkedListDeque61B<>();
        d.addLast("back");
        assertEquals(List.of("back"), d.toList());
        d.addFirst("middle");
        d.addFirst("front");
        assertEquals(List.of("front", "middle", "back"), d.toList());
    }

    @Test
    @DisplayName("官方注释示例：交替 addFirst/addLast")
    public void interspersed() {
        LinkedListDeque61B<Integer> d = new LinkedListDeque61B<>();
        d.addLast(0);
        d.addLast(1);
        d.addFirst(-1);
        d.addLast(2);
        d.addFirst(-2);
        assertEquals(List.of(-2, -1, 0, 1, 2), d.toList());
    }

    @Test
    @DisplayName("isEmpty / size")
    public void emptyAndSize() {
        LinkedListDeque61B<Integer> d = new LinkedListDeque61B<>();
        assertTrue(d.isEmpty());
        assertEquals(0, d.size());
        d.addFirst(10);
        assertFalse(d.isEmpty());
        assertEquals(1, d.size());
        d.addLast(20);
        assertEquals(2, d.size());
    }

    @Test
    @DisplayName("removeFirst / removeLast")
    public void removes() {
        LinkedListDeque61B<Integer> d = new LinkedListDeque61B<>();
        assertNull(d.removeFirst());   // 空表返回 null
        assertNull(d.removeLast());
        d.addLast(1); d.addLast(2); d.addLast(3);
        assertEquals(3, d.removeLast());
        assertEquals(1, d.removeFirst());
        assertEquals(List.of(2), d.toList());
        assertEquals(1, d.size());
    }

    @Test
    @DisplayName("get 与 getRecursive 一致且越界返回 null")
    public void gets() {
        LinkedListDeque61B<String> d = new LinkedListDeque61B<>();
        d.addLast("a"); d.addLast("b"); d.addLast("c");
        assertEquals("a", d.get(0));
        assertEquals("b", d.get(1));
        assertEquals("c", d.get(2));
        assertEquals(d.get(1), d.getRecursive(1));
        assertNull(d.get(-1));
        assertNull(d.get(3));
        assertNull(d.getRecursive(-1));
        assertNull(d.getRecursive(3));
    }

    @Test
    @DisplayName("哨兵环形结构：反复增删后仍然正确")
    public void sentinelStress() {
        LinkedListDeque61B<Integer> d = new LinkedListDeque61B<>();
        for (int i = 0; i < 100; i++) d.addLast(i);
        for (int i = 0; i < 50; i++) d.removeFirst();
        assertEquals(50, d.size());
        assertEquals(50, d.get(0));
        assertEquals(99, d.get(49));
        assertEquals(50, d.getRecursive(0));
        for (int i = 0; i < 49; i++) d.removeLast();
        assertEquals(1, d.size());
        assertEquals(50, d.get(0));
    }
}
