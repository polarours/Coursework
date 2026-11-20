// 028 边界测试（官方样例之外的补充）
#include "List.h"
#include "ListStack.h"
#include "ListQueue.h"
#include <iostream>
using namespace std;

int main()
{
    // 空表边界 —— upstream 实现在这些场景会崩溃，修复版应安全返回 T()
    List<char> empty_list;
    if (empty_list.getFirst() != char()) { cout << "FAIL getFirst on empty\n"; return 1; }
    if (empty_list.getLast() != char())  { cout << "FAIL getLast on empty\n"; return 1; }
    if (empty_list.getAt(0) != char())   { cout << "FAIL getAt on empty\n"; return 1; }
    empty_list.removeStart();   // 不应崩溃
    empty_list.removeEnd();     // 不应崩溃
    cout << "Passed empty-list edges" << endl;

    ListStack<int> st;
    if (st.size() != 0) { cout << "FAIL stack size on empty (upstream 缺 return 的 UB)\n"; return 1; }
    if (st.pop() != int()) { cout << "FAIL pop empty\n"; return 1; }
    cout << "Passed empty-stack edges" << endl;

    ListQueue<int> q;
    if (q.dequeue() != int()) { cout << "FAIL dequeue empty\n"; return 1; }
    cout << "Passed empty-queue edges" << endl;

    // LIFO / FIFO 语义
    ListStack<int> s2;
    for (int v : {1,2,3}) s2.push(v);
    if (s2.size() != 3 || s2.pop() != 3 || s2.pop() != 2 || s2.pop() != 1) {
        cout << "FAIL stack LIFO\n"; return 1;
    }
    ListQueue<int> q2;
    for (int v : {1,2,3}) q2.enqueue(v);
    if (q2.dequeue() != 1 || q2.dequeue() != 2 || q2.dequeue() != 3) {
        cout << "FAIL queue FIFO\n"; return 1;
    }
    cout << "Passed LIFO/FIFO semantics" << endl;

    // List 基本操作
    List<int> l;
    for (int v : {10,20,30}) l.insertEnd(v);
    l.insertStart(5);
    l.insertAt(99, 2);
    if (l.size() != 5) { cout << "FAIL size\n"; return 1; }
    if (l.getAt(2) != 99) { cout << "FAIL insertAt/getAt\n"; return 1; }
    l.removeAt(2);
    if (l.find(99) != -1) { cout << "FAIL removeAt/find\n"; return 1; }
    if (l.find(30) != 3) { cout << "FAIL find\n"; return 1; }
    cout << "Passed List operations" << endl;

    cout << "ALL EDGE TESTS PASSED" << endl;
    return 0;
}
