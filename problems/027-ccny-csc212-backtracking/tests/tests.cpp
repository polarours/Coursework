// 027 自写测试：N-Queens / Sudoku / Sujiko 回溯求解
// upstream scaffolding 无测试文件（评分在课堂 autograder），本文件按题面语义编写。
#include <cassert>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include "n_queens.h"
#include "sudoku.h"
#include "sujiko.h"

static int failures = 0;
#define CHECK(cond) do { \
    if (!(cond)) { std::cerr << "FAIL line " << __LINE__ << ": " #cond "\n"; ++failures; } \
    else { std::cout << "[PASS] " #cond "\n"; } \
} while (0)

// 验证皇后互不攻击 / verify no two queens attack each other
static bool queens_ok(std::vector<std::vector<unsigned int>> &b) {
    unsigned n = b.size();
    for (unsigned c = 0; c < n; ++c) {
        int rows = 0;
        for (unsigned r = 0; r < n; ++r) rows += b[r][c];
        if (rows != 1) return false;   // 每列恰好一个
    }
    for (unsigned r1 = 0; r1 < n; ++r1)
        for (unsigned c1 = 0; c1 < n; ++c1) {
            if (!b[r1][c1]) continue;
            for (unsigned r2 = 0; r2 < n; ++r2)
                for (unsigned c2 = 0; c2 < n; ++c2) {
                    if ((r2 == r1 && c2 == c1) || !b[r2][c2]) continue;
                    if (r2 == r1) return false;                       // 同行
                    if (abs((int)r1 - (int)r2) == abs((int)c1 - (int)c2)) return false; // 对角
                }
        }
    return true;
}

int main()
{
    // === N-Queens ===
    {
        NQueens q(8);
        CHECK(q.solve_rec(0));
        std::cout << "8-Queens 解:\n"; q.display_board();
        std::vector<std::vector<unsigned int>> b(8, std::vector<unsigned int>(8));
        // 通过 display 无法直接取板，用类外重算验证解存在性即可：
        // 我们再解一次并检查内部状态的方式受限（private），改为验证 n=4 的已知解数语义
    }
    {
        // n=4 已知有解；n=2/3 无解 —— 边界验证
        NQueens q4(4);
        CHECK(q4.solve_rec(0));
        NQueens q2(2);
        CHECK(!q2.solve_rec(0));
        NQueens q3(3);
        CHECK(!q3.solve_rec(0));
    }
    // N-Queens display 输出验证：捕获 stdout 检查每列恰好一个 1
    {
        NQueens q(6);
        assert(q.solve_rec(0));
        std::ostringstream oss;
        auto old = std::cout.rdbuf(oss.rdbuf());
        q.display_board();
        std::cout.rdbuf(old);
        std::istringstream iss(oss.str());
        std::vector<std::vector<unsigned int>> b(6, std::vector<unsigned int>(6));
        for (auto &row : b) for (auto &v : row) iss >> v;
        CHECK(queens_ok(b));
    }

    // === Sudoku ===
    {
        Sudoku s("upstream/Labs/Lab 07 Backtracking/scaffolding/Sudoku/puzzle_easy.txt");
        CHECK(s.solve());
        std::cout << "Sudoku(easy) 解:\n"; s.display_board();
    }
    {
        Sudoku s("upstream/Labs/Lab 07 Backtracking/scaffolding/Sudoku/puzzle_medium.txt");
        CHECK(s.solve());
    }
    {
        Sudoku s("upstream/Labs/Lab 07 Backtracking/scaffolding/Sudoku/puzzle_hard.txt");
        CHECK(s.solve());
    }

    // === Sujiko ===
    {
        Sujiko sj("upstream/Labs/Lab 07 Backtracking/scaffolding/Sujiko/sujiko_1.txt");
        CHECK(sj.solve(0));
        std::cout << "Sujiko 解:\n"; sj.display_board();
    }

    std::cout << (failures == 0 ? "ALL TESTS PASSED\n" : "SOME TESTS FAILED\n");
    return failures == 0 ? 0 : 1;
}
