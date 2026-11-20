#include "n_queens.h"

// 参考实现 / reference implementation
// starter 中 solve_rec 为空壳，is_valid_row 已由上游提供

NQueens::NQueens(){
    this->board_size = 0;
    this->board = nullptr;
}

NQueens::~NQueens(){
    delete this->board;
}

NQueens::NQueens(unsigned int n){
    this->board_size = n;
    board = new std::vector<std::vector<unsigned int >>(n, std::vector<unsigned int>(n));
}

bool NQueens::solve_rec(int col){
    // 所有皇后已放置 / all queens placed
    if (col >= (int)this->board_size) return true;

    // 尝试当前列的每一行 / try each row in this column
    for (unsigned int row = 0; row < this->board_size; ++row) {
        if (is_valid_row(row, col)) {
            (*this->board)[row][col] = 1;          // 放置
            if (solve_rec(col + 1)) return true;   // 递归下一列
            (*this->board)[row][col] = 0;          // 回溯 / backtrack
        }
    }
    return false;
}

bool NQueens::is_valid_row(unsigned int row, unsigned int col){
    int i, j;
    /* Check this row on left side */
    for (i = 0; i < (int)col; i++)
        if ((*this->board)[row][i]) { return false; }

    /* Check upper diagonal on left side */
    for (i = (int)row, j = (int)col; i >= 0 && j >= 0; i--, j--)
        if ((*this->board)[i][j]) { return false; }

    /* Check lower diagonal on left side */
    for (i = (int)row, j = (int)col; j >= 0 && i < (int)this->board_size; i++, j--)
        if ((*this->board)[i][j]) { return false; }

    return true;
}

void NQueens::display_board(){
    for (unsigned int i = 0; i < this->board_size; i++) {
        for (unsigned int j = 0; j < this->board_size; j++){
            std::cout << (*this->board)[i][j] << " ";
        }
        std::cout << std::endl;
    }
}
