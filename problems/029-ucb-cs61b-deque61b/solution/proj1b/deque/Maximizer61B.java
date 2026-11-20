package deque;

import java.util.Comparator;
import java.util.Iterator;

/**
 * 参考实现 / reference implementation（proj1b）。
 * 泛型 max：自然序 + 指定 Comparator 两个版本。
 */
public class Maximizer61B {

    /** 自然序最大元素 / max by natural ordering。 */
    public static <T extends Comparable<T>> T max(Iterable<T> iterable) {
        Iterator<T> it = iterable.iterator();
        if (!it.hasNext()) return null;

        T best = it.next();
        while (it.hasNext()) {
            T cur = it.next();
            if (cur.compareTo(best) > 0) best = cur;
        }
        return best;
    }

    /** 按 comp 比较的最大元素 / max by the given comparator。 */
    public static <T> T max(Iterable<T> iterable, Comparator<T> comp) {
        Iterator<T> it = iterable.iterator();
        if (!it.hasNext()) return null;

        T best = it.next();
        while (it.hasNext()) {
            T cur = it.next();
            if (comp.compare(cur, best) > 0) best = cur;
        }
        return best;
    }
}
