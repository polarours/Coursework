// Autograder for ScopedHandle
#include "scoped_handle.h"
#include <cassert>
#include <iostream>
#include <type_traits>

struct Tracker {
    static int alive;
    int value;
    explicit Tracker(int v) : value(v) { ++alive; }
    ~Tracker() { --alive; }
};
int Tracker::alive = 0;

int main() {
    // 1. 构造与析构计数 / construction and destruction counting
    {
        ScopedHandle<Tracker> h(new Tracker(10));
        assert(Tracker::alive == 1);
        assert(h->value == 10);
    }
    assert(Tracker::alive == 0);
    std::cout << "[PASS] construction/destruction\n";

    // 2. 移动构造：源为空 / move constructor leaves source empty
    {
        ScopedHandle<Tracker> a(new Tracker(20));
        ScopedHandle<Tracker> b(std::move(a));
        assert(a.get() == nullptr);
        assert(b->value == 20);
        assert(Tracker::alive == 1);
    }
    assert(Tracker::alive == 0);
    std::cout << "[PASS] move construction\n";

    // 3. 移动赋值：释放原资源 / move assignment frees old resource
    {
        ScopedHandle<Tracker> a(new Tracker(1));
        ScopedHandle<Tracker> b(new Tracker(2));
        assert(Tracker::alive == 2);
        b = std::move(a);
        assert(a.get() == nullptr);
        assert(Tracker::alive == 1);
        assert(b->value == 1);
    }
    assert(Tracker::alive == 0);
    std::cout << "[PASS] move assignment\n";

    // 4. 拷贝被禁用 / copy disabled（编译期检查）
    static_assert(!std::is_copy_constructible_v<ScopedHandle<int>>);
    static_assert(!std::is_copy_assignable_v<ScopedHandle<int>>);
    static_assert(std::is_move_constructible_v<ScopedHandle<int>>);
    std::cout << "[PASS] copy disabled / move enabled\n";

    // 5. reset 与 release / reset and release
    {
        ScopedHandle<Tracker> h(new Tracker(30));
        h.reset(new Tracker(40));
        assert(Tracker::alive == 1);
        assert(h->value == 40);
        Tracker* raw = h.release();
        assert(h.get() == nullptr);
        assert(raw->value == 40);
        delete raw;
        assert(Tracker::alive == 0);
    }
    std::cout << "[PASS] reset/release\n";

    // 6. 空句柄 / empty handle
    {
        ScopedHandle<int> h;
        assert(h.get() == nullptr);
    }
    std::cout << "[PASS] empty handle\n";

    std::cout << "ALL TESTS PASSED\n";
    return 0;
}
