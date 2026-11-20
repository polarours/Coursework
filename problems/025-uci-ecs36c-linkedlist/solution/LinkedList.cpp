#ifndef LINKED_LIST_CPP
#define LINKED_LIST_CPP
// 参考实现 / reference implementation

#include "LinkedList.hpp"

template <typename T>
LinkedList<T>::LinkedList() : _size(0), _head(nullptr), _tail(nullptr) {}

template <typename T>
LinkedList<T>::LinkedList(LinkedList<T> &&other) : _size(other._size),
                                                   _head(other._head),
                                                   _tail(other._tail)
{
    other._size = 0;
    other._head = nullptr;
    other._tail = nullptr;
}

template <typename T>
LinkedList<T>::LinkedList(const std::vector<T> &items)
    : _size(0), _head(nullptr), _tail(nullptr)
{
    for (const T &v : items) append(v);
}

template <typename T>
size_t LinkedList<T>::size() const { return _size; }

template <typename T>
LinkedListNode<T> *LinkedList<T>::head() const { return _head; }

template <typename T>
LinkedListNode<T> *LinkedList<T>::tail() const { return _tail; }

template <typename T>
LinkedListNode<T> *LinkedList<T>::find(T value) const
{
    for (LinkedListNode<T> *cur = _head; cur != nullptr; cur = cur->next())
        if (cur->value == value) return cur;
    return nullptr;
}

template <typename T>
LinkedListNode<T> *LinkedList<T>::prepend(T value)
{
    _head = new LinkedListNode<T>(value, _head);
    if (_tail == nullptr) _tail = _head;
    ++_size;
    return _head;
}

template <typename T>
LinkedListNode<T> *LinkedList<T>::append(T value)
{
    LinkedListNode<T> *node = new LinkedListNode<T>(value);
    if (_tail == nullptr) {
        _head = _tail = node;
    } else {
        _tail->_next = node;   // friend 类可访问私有构造与 _next
        _tail = node;
    }
    ++_size;
    return node;
}

template <typename T>
LinkedListNode<T> *LinkedList<T>::insertAfter(LinkedListNode<T> *node, T value)
{
    LinkedListNode<T> *fresh = new LinkedListNode<T>(value, node->next());
    node->_next = fresh;
    if (_tail == node) _tail = fresh;
    ++_size;
    return fresh;
}

template <typename T>
std::optional<T> LinkedList<T>::removeHead()
{
    if (_head == nullptr) return std::nullopt;
    LinkedListNode<T> *old = _head;
    _head = old->_next;
    if (_head == nullptr) _tail = nullptr;
    --_size;
    T value = old->value;
    delete old;
    return value;
}

template <typename T>
LinkedList<T>::~LinkedList() { clear(); }

template <typename T>
void LinkedList<T>::clear()
{
    while (_head != nullptr) {
        LinkedListNode<T> *next = _head->_next;
        delete _head;
        _head = next;
    }
    _tail = nullptr;
    _size = 0;
}

#endif
