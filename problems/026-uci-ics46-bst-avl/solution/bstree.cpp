#include "bstree.h"
#include <cassert>
#include <algorithm>

// 参考实现 / reference implementation —— starter 中此文件为空

Node * BSTree::insert_node(Node * t, string key)
{
    if (t == nullptr) return new Node(key);
    if (key < t->key)      t->left  = insert_node(t->left, key);
    else if (key > t->key) t->right = insert_node(t->right, key);
    // 相等则不重复插入 / duplicate: no-op
    return t;
}

Node * BSTree::find_node(Node * t, string key)
{
    while (t != nullptr) {
        if (key == t->key) return t;
        t = (key < t->key) ? t->left : t->right;
    }
    return nullptr;
}

Node * BSTree::left_most(Node * t)
{
    while (t != nullptr && t->left != nullptr) t = t->left;
    return t;
}

Node * BSTree::delete_node(Node * t, string key)
{
    if (t == nullptr) return nullptr;
    if (key < t->key) {
        t->left = delete_node(t->left, key);
    } else if (key > t->key) {
        t->right = delete_node(t->right, key);
    } else {
        // 找到要删除的节点 / found
        if (t->left == nullptr && t->right == nullptr) {
            delete t;
            return nullptr;
        }
        if (t->left == nullptr) {
            Node *r = t->right; delete t; return r;
        }
        if (t->right == nullptr) {
            Node *l = t->left;  delete t; return l;
        }
        // 双孩子：用右子树最小节点替换 / two children: replace with successor
        Node *succ = left_most(t->right);
        t->key = succ->key;
        t->right = delete_node(t->right, succ->key);
    }
    return t;
}

int BSTree::compute_height(Node * t)
{
    if (t == nullptr) return 0;
    return 1 + std::max(compute_height(t->left), compute_height(t->right));
}

BSTree::BSTree() : BST("BSTree") {}

void BSTree::insert(const string & key)
{
    if (find_node(root, key) != nullptr) return;   // 重复键不插入不计数
    root = insert_node(root, key);
    ++count;
}

bool BSTree::find(const string & key) const
{
    return find_node(root, key) != nullptr;
}

void BSTree::remove(const string & key)
{
    if (find_node(root, key) == nullptr) return;  // 不存在直接返回
    root = delete_node(root, key);
    --count;
}

bool BSTree::is_empty() const { return root == nullptr; }

int BSTree::get_height() const { return compute_height(root); }
