#pragma once
// 参考实现 / reference implementation
#include <utility>

template <typename T>
class ScopedHandle {
public:
    explicit ScopedHandle(T* ptr = nullptr) noexcept : ptr_(ptr) {}

    ~ScopedHandle() { delete ptr_; }

    ScopedHandle(const ScopedHandle&) = delete;
    ScopedHandle& operator=(const ScopedHandle&) = delete;

    ScopedHandle(ScopedHandle&& other) noexcept : ptr_(other.ptr_) {
        other.ptr_ = nullptr;   // 移动后源对象置空 / leave source empty
    }

    ScopedHandle& operator=(ScopedHandle&& other) noexcept {
        if (this != &other) {
            delete ptr_;             // 先释放自己的资源
            ptr_ = other.ptr_;
            other.ptr_ = nullptr;
        }
        return *this;
    }

    T& operator*() const { return *ptr_; }
    T* operator->() const { return ptr_; }
    T* get() const { return ptr_; }

    void reset(T* new_ptr = nullptr) noexcept {
        if (new_ptr != ptr_) {
            delete ptr_;
            ptr_ = new_ptr;
        }
    }

    T* release() noexcept {
        T* old = ptr_;
        ptr_ = nullptr;
        return old;
    }

private:
    T* ptr_ = nullptr;
};
