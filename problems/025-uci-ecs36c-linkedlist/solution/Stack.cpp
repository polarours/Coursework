#ifndef STACK_CPP
#define STACK_CPP
// 参考实现 / reference implementation

#include "Stack.hpp"

template <typename T>
Stack<T>::Stack() {}

template <typename T>
Stack<T>::Stack(const std::vector<T> &items)
{
    // "end of items is the top"：链表头是栈顶，所以逆序插入
    for (auto it = items.rbegin(); it != items.rend(); ++it)
        _llist.append(*it);
}

template <typename T>
size_t Stack<T>::size() const { return _llist.size(); }

template <typename T>
std::optional<T> Stack<T>::top() const
{
    if (_llist.head() == nullptr) return std::nullopt;
    return _llist.head()->value;   // 链表头即栈顶
}

template <typename T>
void Stack<T>::push(T value) { _llist.prepend(value); }

template <typename T>
std::optional<T> Stack<T>::pop() { return _llist.removeHead(); }

#endif
