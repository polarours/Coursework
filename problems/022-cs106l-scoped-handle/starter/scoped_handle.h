#pragma once
// ScopedHandle: 教学版独占资源句柄 / teaching version of an owning handle
// === 这是 starter code：TODO 处由学生填写 ===

template <typename T>
class ScopedHandle {
public:
    // Part 1: 构造函数，接管 ptr 的所有权
    explicit ScopedHandle(T* ptr = nullptr) /* TODO */ {}

    // Part 1: 析构函数，释放资源
    ~ScopedHandle() /* TODO */ {}

    // Part 1: 禁止拷贝（Rule of Five）
    ScopedHandle(const ScopedHandle&) = delete;
    ScopedHandle& operator=(const ScopedHandle&) = delete;

    // Part 1: 移动构造与移动赋值
    ScopedHandle(ScopedHandle&& other) noexcept /* TODO */ {}
    ScopedHandle& operator=(ScopedHandle&& other) noexcept /* TODO */ { return *this; }

    // Part 2: 访问接口
    T& operator*() const /* TODO */ {}
    T* operator->() const /* TODO */ {}
    T* get() const /* TODO */ {}
    void reset(T* new_ptr = nullptr) /* TODO */ {}
    T* release() /* TODO */ {}

private:
    T* ptr_ = nullptr;
};
