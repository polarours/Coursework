// 026 自写测试（说明：upstream 的 student_gtests.cpp 只有占位用例
// TEST(Replace, Me) 永远失败——真实评测在 Gradescope。本文件按 bst.h
// 接口语义编写，验证参考实现的正确性）。
#include <gtest/gtest.h>
#include "timer.h"
#include "bst.h"
#include "bstree.h"
#include "avltree.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <cstdio>

static int count_lines(const std::string &path) {
    std::ifstream in(path);
    std::string w; int n = 0;
    while (in >> w) ++n;
    return n;
}

TEST(BSTree, InsertFindRemove)
{
    BSTree tree;
    EXPECT_TRUE(tree.is_empty());
    tree.insert("mango");
    tree.insert("apple");
    tree.insert("pear");
    tree.insert("banana");
    EXPECT_FALSE(tree.is_empty());
    EXPECT_TRUE(tree.find("apple"));
    EXPECT_TRUE(tree.find("mango"));
    EXPECT_FALSE(tree.find("cherry"));

    tree.remove("apple");
    EXPECT_FALSE(tree.find("apple"));
    EXPECT_TRUE(tree.find("pear"));

    // 中序输出应有序 / in-order output is sorted
    std::ostringstream out;
    out << tree;
    std::string s = out.str();
    EXPECT_NE(s.find("banana"), std::string::npos);
    EXPECT_NE(s.find("mango"), std::string::npos);
    EXPECT_EQ(s.find("apple"), std::string::npos);
}

TEST(BSTree, SortedInputDegradesToChain)
{
    // 顺序插入使普通 BST 退化成链 / sorted input degrades a plain BST
    BSTree tree;
    const int N = 1024;
    // 零填充保证字典序 = 数值序，严格递增 → 完美退化链
    for (int i = 0; i < N; ++i) {
        char buf[16];
        std::snprintf(buf, sizeof buf, "w%04d", i);
        tree.insert(buf);
    }
    EXPECT_EQ(tree.get_height(), N);   // 链的高度 = N
}

TEST(AVLTree, SortedInputStaysBalanced)
{
    // 同样的顺序插入，AVL 高度应为对数 / same input, AVL height is logarithmic
    AVLTree tree;
    const int N = 1024;
    for (int i = 0; i < N; ++i) {
        char buf[16];
        std::snprintf(buf, sizeof buf, "w%04d", i);
        tree.insert(buf);
    }
    // AVL 高度上界 ≈ 1.44*log2(N+2)；N=1024 时界限约 14.3
    EXPECT_LE(tree.get_height(), 14);
    EXPECT_GE(tree.get_height(), 10);   // 完全平衡是 11（1024 节点）
}

TEST(AVLTree, FindAndRemoveRebalanced)
{
    AVLTree tree;
    for (int i = 0; i < 500; ++i)
        tree.insert("k" + std::to_string(i));
    EXPECT_TRUE(tree.find("k0"));
    EXPECT_TRUE(tree.find("k499"));
    EXPECT_FALSE(tree.find("k500"));

    for (int i = 0; i < 250; ++i)
        tree.remove("k" + std::to_string(i));
    EXPECT_FALSE(tree.find("k42"));
    EXPECT_TRUE(tree.find("k250"));
    EXPECT_TRUE(tree.find("k499"));
    // 删除一半后仍是 AVL 平衡 / still balanced after mass deletion
    EXPECT_LE(tree.get_height(), 13);
}

TEST(BothTrees, SameDataSameInOrderOutput)
{
    // 两棵树插入同一批数据，中序输出必须一致 / identical in-order content
    std::ifstream in("upstream/src/shortrandom.txt");
    ASSERT_TRUE(in.good());
    std::vector<std::string> words;
    std::string w;
    while (in >> w) words.push_back(w);
    ASSERT_GT(words.size(), 5u);

    BSTree b;
    AVLTree a;
    for (const std::string &x : words) { b.insert(x); a.insert(x); }

    std::ostringstream ob, oa;
    ob << b; oa << a;
    EXPECT_EQ(ob.str(), oa.str());
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
