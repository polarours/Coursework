#include "sujiko.h"

// 参考实现 / reference implementation
// Sujiko：3x3 棋盘放 1-9 各一次，四个 2x2 宫的中心目标和由 nums 给出

Sujiko::Sujiko() {
}

Sujiko::Sujiko(std::string fname) {
    // Read 4 sum values from file & create board
    std::ifstream in(fname);
    if (!in) { std::cerr << "cannot open " << fname << "\n"; return; }
    for (unsigned int i = 0; i < 2; ++i)
        for (unsigned int j = 0; j < 2; ++j)
            in >> this->nums[i][j];
    for (unsigned int i = 0; i < BOARD_SIZE; ++i)
        for (unsigned int j = 0; j < BOARD_SIZE; ++j)
            in >> this->board[i][j];
}

Sujiko::~Sujiko() {
}

bool Sujiko::solve(unsigned int cell){
    // 所有格子已放好 / all cells placed
    if (cell >= BOARD_SIZE * BOARD_SIZE) return true;

    unsigned int row = cell / BOARD_SIZE;
    unsigned int col = cell % BOARD_SIZE;

    if (this->board[row][col] != EMPTY)
        return solve(cell + 1);   // 预填格直接跳过

    for (unsigned int num = 1; num <= 9; ++num) {
        // 唯一性：每个数字只用一次 / each digit used once
        bool used = false;
        for (unsigned int i = 0; i < BOARD_SIZE && !used; ++i)
            for (unsigned int j = 0; j < BOARD_SIZE; ++j)
                if (this->board[i][j] == num) { used = true; break; }
        if (used) continue;

        this->board[row][col] = num;

        // 已完成的宫必须满足目标和 / completed boxes must match targets
        bool ok = true;
        for (unsigned int bi = 0; bi < 2 && ok; ++bi) {
            for (unsigned int bj = 0; bj < 2 && ok; ++bj) {
                unsigned int r0 = bi, c0 = bj;
                int sum = 0, filled = 0;
                for (unsigned int di = 0; di < 2; ++di)
                    for (unsigned int dj = 0; dj < 2; ++dj) {
                        unsigned int v = this->board[r0 + di][c0 + dj];
                        if (v != EMPTY) { sum += v; ++filled; }
                    }
                if (filled == 4) {
                    // 与该 2x2 宫相关的目标和在 nums[bi][bj]
                    // 宫的行号范围 [bi, bi+1]，列号 [bj, bj+1]
                    if ((unsigned)sum != this->nums[bi][bj]) ok = false;
                } else if (filled == 3 && sum >= (int)this->nums[bi][bj]) {
                    ok = false;   // 剪枝：三个数已超目标和
                }
            }
        }

        if (ok && solve(cell + 1)) return true;
        this->board[row][col] = EMPTY;   // 回溯 / backtrack
    }
    return false;
}

void Sujiko::display_board(){
    for (unsigned int i = 0; i < this->BOARD_SIZE; i++) {
        for (unsigned int j = 0; j < this->BOARD_SIZE; j++){
            std::cout << this->board[i][j] << " ";
        }
        std::cout << std::endl;
    }
}
