#include "sudoku.h"
#include <sstream>
#include <fstream>
#include <iostream>

// 参考实现 / reference implementation

Sudoku::Sudoku() {
}

Sudoku::~Sudoku() {
}

Sudoku::Sudoku(std::string f_name) {
    // Generate a board from the give file
    std::ifstream in(f_name);
    if (!in) { std::cerr << "cannot open " << f_name << "\n"; return; }
    for (unsigned int i = 0; i < BOARD_SIZE; ++i)
        for (unsigned int j = 0; j < BOARD_SIZE; ++j)
            in >> this->board[i][j];
}

bool Sudoku::solve() {
    // 找第一个空格 / find the first empty cell
    for (unsigned int row = 0; row < BOARD_SIZE; ++row) {
        for (unsigned int col = 0; col < BOARD_SIZE; ++col) {
            if (this->board[row][col] == EMPTY) {
                for (int num = 1; num <= 9; ++num) {
                    if (is_valid(row, col, num)) {
                        this->board[row][col] = num;         // 放置
                        if (solve()) return true;            // 递归
                        this->board[row][col] = EMPTY;       // 回溯 / backtrack
                    }
                }
                return false;   // 本格无解 → 整体回溯
            }
        }
    }
    return true;   // 没有空格了 → 完成
}

bool Sudoku::is_valid(unsigned int row, unsigned int col, int num){
    return (this->board)[row][col] == 0
            && !check_row(row, num)
            && !check_col(col, num)
            && !check_box(row - row % 3, col - col % 3, num);
}

bool Sudoku::check_row(unsigned int row, unsigned int num){
    for (unsigned int j = 0; j < BOARD_SIZE; ++j)
        if (this->board[row][j] == num) return true;
    return false;
}

bool Sudoku::check_col(unsigned int col, unsigned int num){
    for (unsigned int i = 0; i < BOARD_SIZE; ++i)
        if (this->board[i][col] == num) return true;
    return false;
}

bool Sudoku::check_box(unsigned int boxStartRow, unsigned int boxStartCol, unsigned int num){
    for (unsigned int i = 0; i < 3; ++i)
        for (unsigned int j = 0; j < 3; ++j)
            if (this->board[boxStartRow + i][boxStartCol + j] == num) return true;
    return false;
}

void Sudoku::display_board(){
    for (unsigned int i = 0; i < this->BOARD_SIZE; i++) {
        for (unsigned int j = 0; j < this->BOARD_SIZE; j++){
            std::cout << (this->board)[i][j] << " ";
        }
        std::cout << std::endl;
    }
}
