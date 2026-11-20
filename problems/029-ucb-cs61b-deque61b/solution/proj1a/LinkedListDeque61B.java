import java.util.List;
import java.util.ArrayList;

/**
 * 参考实现 / reference implementation。
 * 按 CS61B proj1a 规格：环形双向链表 + 一个哨兵节点（sentinel），
 * getRecursive 必须用递归实现。
 *
 * Circular doubly-linked list with a single sentinel node, per the proj1a spec.
 */
public class LinkedListDeque61B<T> implements Deque61B<T> {

    /** 内部节点类（PreconditionTest 要求恰好一个 inner class）。 */
    private class Node {
        T item;
        Node prev;
        Node next;

        Node(T item, Node prev, Node next) {
            this.item = item;
            this.prev = prev;
            this.next = next;
        }
    }

    /** 哨兵：sentinel.next 指向首元素，sentinel.prev 指向末元素。 */
    private Node sentinel;
    private int size;

    public LinkedListDeque61B() {
        sentinel = new Node(null, null, null);
        sentinel.prev = sentinel;
        sentinel.next = sentinel;
        size = 0;
    }

    @Override
    public void addFirst(T x) {
        Node n = new Node(x, sentinel, sentinel.next);
        sentinel.next.prev = n;
        sentinel.next = n;
        size += 1;
    }

    @Override
    public void addLast(T x) {
        Node n = new Node(x, sentinel.prev, sentinel);
        sentinel.prev.next = n;
        sentinel.prev = n;
        size += 1;
    }

    @Override
    public List<T> toList() {
        List<T> out = new ArrayList<>(size);
        Node cur = sentinel.next;
        while (cur != sentinel) {
            out.add(cur.item);
            cur = cur.next;
        }
        return out;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public T removeFirst() {
        if (isEmpty()) return null;
        Node first = sentinel.next;
        first.next.prev = sentinel;
        sentinel.next = first.next;
        size -= 1;
        return first.item;
    }

    @Override
    public T removeLast() {
        if (isEmpty()) return null;
        Node last = sentinel.prev;
        last.prev.next = sentinel;
        sentinel.prev = last.prev;
        size -= 1;
        return last.item;
    }

    @Override
    public T get(int index) {
        if (index < 0 || index >= size) return null;
        Node cur = sentinel.next;
        for (int i = 0; i < index; i++) cur = cur.next;
        return cur.item;
    }

    @Override
    public T getRecursive(int index) {
        if (index < 0 || index >= size) return null;
        return getRecursiveHelper(sentinel.next, index);
    }

    private T getRecursiveHelper(Node start, int index) {
        if (index == 0) return start.item;
        return getRecursiveHelper(start.next, index - 1);
    }
}
