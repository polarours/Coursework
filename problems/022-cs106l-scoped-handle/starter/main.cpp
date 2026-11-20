#include <scoped_handle.h>
#include <iostream>

int main() {
    ScopedHandle<int> h(new int(42));
    std::cout << "value = " << *h << "\n";

    ScopedHandle<int> h2(std::move(h));
    std::cout << "after move: h.get() = " << h.get()
              << ", h2 value = " << *h2 << "\n";

    h2.reset(new int(7));
    std::cout << "after reset: " << *h2 << "\n";
    return 0;
}
