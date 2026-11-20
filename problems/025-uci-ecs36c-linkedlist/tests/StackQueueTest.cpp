// Stack/Queue 激活测试
// 第一个用例来自 upstream tests/StackTest.cpp 中被注释的官方示例（原样启用）
// 其余基于 Stack.hpp / Queue.hpp 的接口语义编写
#include <gtest/gtest.h>
#include "LinkedList.cpp"   // 必须先引入 solution 版实现（-I solution 优先）
#include "Stack.cpp"       // Stack.hpp 内部再 include LinkedList.cpp 时已被 guard 挡住
#include "Queue.cpp"

// === 来自 upstream 的官方示例（解除注释）===
TEST(StackTest, InstantiateEmptyStack)
{
    Stack<int> stack;
    ASSERT_EQ(stack.size(), 0);
    ASSERT_EQ(stack.top(), std::nullopt);
}

// 来自 upstream tests/QueueTest.cpp 的官方示例
TEST(QueueTest, InstantiateEmptyQueue)
{
    Queue<int> queue;
    ASSERT_EQ(queue.size(), 0);
}

// === 语义测试 ===
TEST(StackTest, PushPopLIFO)
{
    Stack<int> stack;
    stack.push(1);
    stack.push(2);
    stack.push(3);
    ASSERT_EQ(stack.size(), 3);
    ASSERT_EQ(stack.top(), 3);
    ASSERT_EQ(stack.pop(), 3);
    ASSERT_EQ(stack.pop(), 2);
    ASSERT_EQ(stack.pop(), 1);
    ASSERT_EQ(stack.pop(), std::nullopt);   // 空栈弹出
    ASSERT_EQ(stack.size(), 0);
}

TEST(StackTest, VectorCtorTopIsEnd)
{
    // "end of items is the top"
    Stack<int> stack(std::vector<int>{1, 2, 3});
    ASSERT_EQ(stack.top(), 3);
    ASSERT_EQ(stack.pop(), 3);
    ASSERT_EQ(stack.pop(), 2);
}

TEST(QueueTest, EnqueueDequeueFIFO)
{
    Queue<int> queue;
    queue.enqueue(1);
    queue.enqueue(2);
    queue.enqueue(3);
    ASSERT_EQ(queue.size(), 3);
    ASSERT_EQ(queue.dequeue(), 1);   // 先进先出
    ASSERT_EQ(queue.dequeue(), 2);
    ASSERT_EQ(queue.dequeue(), 3);
    ASSERT_EQ(queue.dequeue(), std::nullopt);
}
