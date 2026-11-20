#include "bst.h"
#include "bstree.h"
#include "avltree.h"
#include "timer.h"
#include <fstream>
#include <sstream>
#include <vector>

// 参考实现 / reference implementation —— starter 中此文件为空

BST::~BST()
{
    // 递归删除所有节点 / recursively delete all nodes
    struct Cleanup {
        static void destroy(Node *t) {
            if (t == nullptr) return;
            destroy(t->left);
            destroy(t->right);
            delete t;
        }
    };
    Cleanup::destroy(root);
}

void BST::pre_order_print(ostream & out, Node * t)
{
    if (t == nullptr) return;
    out << t->key << " ";
    pre_order_print(out, t->left);
    pre_order_print(out, t->right);
}

void BST::in_order_print(ostream & out, Node * t)
{
    if (t == nullptr) return;
    in_order_print(out, t->left);
    out << t->key << " ";
    in_order_print(out, t->right);
}

void BST::post_order_print(ostream & out, Node * t)
{
    if (t == nullptr) return;
    post_order_print(out, t->left);
    post_order_print(out, t->right);
    out << t->key << " ";
}

ostream & operator << (ostream & out, BST & L)
{
    L.print(out);
    return out;
}

void error(string word, string msg)
{
    cerr << "ERROR: " << word << " " << msg << endl;
    exit(1);
}

static void load_words(const string & file_name, vector<string> & words)
{
    ifstream in(file_name);
    if (!in) error(file_name, "cannot open");
    string w;
    while (in >> w) words.push_back(w);
}

void insert_all_words(int k, string file_name, BST & L)
{
    vector<string> words;
    load_words(file_name, words);
    for (int rep = 0; rep < k; ++rep)
        for (const string & w : words)
            L.insert(w);
}

void find_all_words(int k, string file_name, BST & L)
{
    vector<string> words;
    load_words(file_name, words);
    for (int rep = 0; rep < k; ++rep)
        for (const string & w : words)
            L.find(w);
}

void remove_all_words(int k, string file_name, BST & L)
{
    vector<string> words;
    load_words(file_name, words);
    for (int rep = 0; rep < k; ++rep)
        for (const string & w : words)
            L.remove(w);
}

void measure_BST(string file_name, BST & L)
{
    double wc, ut, st;
    Timer timer;

    timer.start();
    insert_all_words(1, file_name, L);
    timer.elapsedTime(wc, ut, st);
    cout << L.name
         << " insert " << file_name << " " << wc << "s wallclock, size "
         << L.size() << ", height " << L.get_height() << "\n";

    timer.start();
    find_all_words(1, file_name, L);
    timer.elapsedTime(wc, ut, st);
    cout << L.name << " find " << file_name << " " << wc << "s\n";

    timer.start();
    remove_all_words(1, file_name, L);
    timer.elapsedTime(wc, ut, st);
    cout << L.name << " remove " << file_name << " " << wc << "s, size "
         << L.size() << "\n";
}

void measure_BSTs(string input_file)
{
    {
        BSTree tree;
        measure_BST(input_file, tree);
    }
    {
        AVLTree tree;
        measure_BST(input_file, tree);
    }
}
