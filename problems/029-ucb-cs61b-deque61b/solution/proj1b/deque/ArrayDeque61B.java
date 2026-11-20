package deque;

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

/**
 * 参考实现 / reference implementation（proj1b）。
 * 环形数组：nextFirst 指向首元素前一格，nextLast 指向末元素后一格。
 * 扩容：满时翻倍；缩容：元素数 < 容量/4 且容量足够大时减半。
 * 官方 Maximizer61BTest 直接把 ArrayDeque61B 传入 max(Iterable,...)，
 * 因此需实现 Iterable——这是 starter 故意留下的缺口。
 */
public class ArrayDeque61B<T> implements Deque61B<T>, Iterable<T> {

    private T[] items;
    private int size;
    private int nextFirst;   // 首元素前一格
    private int nextLast;    // 末元素后一格

    private static final int START_CAPACITY = 8;

    @SuppressWarnings("unchecked")
    public ArrayDeque61B() {
        items = (T[]) new Object[START_CAPACITY];
        size = 0;
        nextFirst = START_CAPACITY - 1;
        nextLast = 0;
    }

    /** 环形下标前进/后退一步。 */
    private int plusOne(int i) { return (i + 1) % items.length; }
    private int minusOne(int i) { return (i - 1 + items.length) % items.length; }

    /** 调整容量并把元素按逻辑顺序搬回 [0, size)。 */
    @SuppressWarnings("unchecked")
    private void resize(int capacity) {
        T[] fresh = (T[]) new Object[capacity];
        int idx = plusOne(nextFirst);
        for (int i = 0; i < size; ++i) {
            fresh[i] = items[idx];
            idx = plusOne(idx);
        }
        items = fresh;
        nextFirst = items.length - 1;
        nextLast = size;
    }

    @Override
    public void addFirst(T x) {
        if (size == items.length) resize(items.length * 2);
        items[nextFirst] = x;
        nextFirst = minusOne(nextFirst);
        size += 1;
    }

    @Override
    public void addLast(T x) {
        if (size == items.length) resize(items.length * 2);
        items[nextLast] = x;
        nextLast = plusOne(nextLast);
        size += 1;
    }

    @Override
    public List<T> toList() {
        List<T> out = new ArrayList<>(size);
        int idx = plusOne(nextFirst);
        for (int i = 0; i < size; ++i) {
            out.add(items[idx]);
            idx = plusOne(idx);
        }
        return out;
    }

    @Override
    public boolean isEmpty() { return size == 0; }

    @Override
    public int size() { return size; }

    @Override
    public T removeFirst() {
        if (isEmpty()) return null;
        int first = plusOne(nextFirst);
        T val = items[first];
        items[first] = null;          // 释放引用，避免 loitering
        nextFirst = first;
        size -= 1;
        shrinkIfNeeded();
        return val;
    }

    @Override
    public T removeLast() {
        if (isEmpty()) return null;
        int last = minusOne(nextLast);
        T val = items[last];
        items[last] = null;
        nextLast = last;
        size -= 1;
        shrinkIfNeeded();
        return val;
    }

    /** 元素数 < 容量 1/4 且容量足够大时减半。 */
    private void shrinkIfNeeded() {
        if (items.length > START_CAPACITY * 2 && size * 4 < items.length)
            resize(items.length / 2);
    }

    @Override
    public T get(int index) {
        if (index < 0 || index >= size) return null;
        int idx = plusOne(nextFirst);
        for (int i = 0; i < index; ++i) idx = plusOne(idx);
        return items[idx];
    }

    /**
     * 数组版用迭代实现（规格未要求递归——数组 O(1) 索引正是它的优势）。
     * Implemented iteratively: O(1) indexing is the array deque's strength.
     */
    @Override
    public T getRecursive(int index) {
        return get(index);
    }

    /** 按逻辑顺序遍历（Maximizer61B 依赖此接口）。 */
    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {
            private int seen = 0;
            private int idx = plusOne(nextFirst);

            @Override
            public boolean hasNext() { return seen < size; }

            @Override
            public T next() {
                T val = items[idx];
                idx = plusOne(idx);
                seen += 1;
                return val;
            }
        };
    }
}
