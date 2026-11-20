#include "avltree.h"
#include <algorithm>
#include <cassert>

// 参考实现 / reference implementation —— starter 中此文件为空

int AVLTree::get_height(Node * node)
{
    return node == nullptr ? 0 : node->height;
}

int AVLTree::get_balance(Node * node)
{
    return node == nullptr ? 0 : get_height(node->left) - get_height(node->right);
}

void AVLTree::set_height(Node * node)
{
    node->height = 1 + std::max(get_height(node->left), get_height(node->right));
}

Node * AVLTree::right_rotate(Node * y)
{
    Node *x = y->left;
    y->left = x->right;
    x->right = y;
    set_height(y);
    set_height(x);
    return x;
}

Node * AVLTree::left_rotate(Node * x)
{
    Node *y = x->right;
    x->right = y->left;
    y->left = x;
    set_height(x);
    set_height(y);
    return y;
}

Node * AVLTree::rebalance(Node * t)
{
    set_height(t);
    int balance = get_balance(t);
    if (balance > 1) {
        if (get_balance(t->left) < 0)          // LR
            t->left = left_rotate(t->left);
        return right_rotate(t);               // LL
    }
    if (balance < -1) {
        if (get_balance(t->right) > 0)         // RL
            t->right = right_rotate(t->right);
        return left_rotate(t);                // RR
    }
    return t;
}

Node * AVLTree::insert_node(Node * t, string key)
{
    if (t == nullptr) return new Node(key);
    if (key < t->key)      t->left  = insert_node(t->left, key);
    else if (key > t->key) t->right = insert_node(t->right, key);
    else                   return t;   // 重复不插入
    return rebalance(t);
}

Node * AVLTree::find_node(Node * t, string key)
{
    while (t != nullptr) {
        if (key == t->key) return t;
        t = (key < t->key) ? t->left : t->right;
    }
    return nullptr;
}

Node * AVLTree::delete_node(Node * t, string key)
{
    if (t == nullptr) return nullptr;
    if (key < t->key) {
        t->left = delete_node(t->left, key);
    } else if (key > t->key) {
        t->right = delete_node(t->right, key);
    } else {
        if (t->left == nullptr && t->right == nullptr) {
            delete t; return nullptr;
        }
        if (t->left == nullptr) {
            Node *r = t->right; delete t; return r;
        }
        if (t->right == nullptr) {
            Node *l = t->left;  delete t; return l;
        }
        // 双孩子：取右子树最小替换后删除 / two children: successor swap
        Node *succ = t->right;
        while (succ->left != nullptr) succ = succ->left;
        t->key = succ->key;
        t->right = delete_node(t->right, succ->key);
    }
    return rebalance(t);   // 删除后也要保持平衡 / rebalance after deletion
}

AVLTree::AVLTree() : BST("AVLTree") {}

void AVLTree::insert(const string & key)
{
    if (find_node(root, key) != nullptr) return;   // 重复键不插入不计数
    root = insert_node(root, key);
    ++count;
}

bool AVLTree::find(const string & key) const
{
    return find_node(root, key) != nullptr;
}

void AVLTree::remove(const string & key)
{
    if (find_node(root, key) == nullptr) return;
    root = delete_node(root, key);
    --count;
}

bool AVLTree::is_empty() const { return root == nullptr; }

int AVLTree::get_height() const { return get_height(root); }
