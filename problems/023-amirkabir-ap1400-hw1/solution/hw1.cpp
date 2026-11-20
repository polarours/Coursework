#include "hw1.h"
#include <random>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <cmath>
namespace algebra {

Matrix zeros(std::size_t n, std::size_t m) { return Matrix(n, std::vector<double>(m, 0.0)); }
Matrix ones(std::size_t n, std::size_t m) { return Matrix(n, std::vector<double>(m, 1.0)); }

Matrix random(std::size_t n, std::size_t m, double mn, double mx) {
    if (mn > mx) throw std::logic_error("min cannot be greater than max");
    std::mt19937 gen(42);  // 固定种子保证可复现
    std::uniform_real_distribution<double> dist(mn, mx);
    Matrix r(n, std::vector<double>(m));
    for (auto& row : r) for (auto& x : row) x = dist(gen);
    return r;
}

void show(const Matrix& matrix) {
    for (const auto& row : matrix) {
        for (double x : row) std::cout << std::fixed << std::setprecision(3) << x << " ";
        std::cout << "\n";
    }
}

Matrix multiply(const Matrix& a, double c) {
    Matrix r = a;
    for (auto& row : r) for (auto& x : row) x *= c;
    return r;
}

Matrix multiply(const Matrix& a, const Matrix& b) {
    if (a.empty() || b.empty() || b[0].empty()) return {};       // 空矩阵相乘
    std::size_t n = a.size(), m = b[0].size(), k = b.size();
    if (a[0].size() != k) throw std::logic_error("dimension mismatch");
    Matrix r(n, std::vector<double>(m, 0.0));
    for (std::size_t i = 0; i < n; ++i)
        for (std::size_t t = 0; t < k; ++t)
            for (std::size_t j = 0; j < m; ++j)
                r[i][j] += a[i][t] * b[t][j];
    return r;
}

Matrix sum(const Matrix& a, double c) {
    Matrix r = a;
    for (auto& row : r) for (auto& x : row) x += c;
    return r;
}

Matrix sum(const Matrix& a, const Matrix& b) {
    if (a.empty() && b.empty()) return {};
    if (a.size() != b.size() || a.empty() || b.empty() || a[0].size() != b[0].size())
        throw std::logic_error("dimension mismatch");
    Matrix r = a;
    for (std::size_t i = 0; i < r.size(); ++i)
        for (std::size_t j = 0; j < r[i].size(); ++j)
            r[i][j] += b[i][j];
    return r;
}

Matrix transpose(const Matrix& a) {
    if (a.empty() || a[0].empty()) return {};
    Matrix r(a[0].size(), std::vector<double>(a.size()));
    for (std::size_t i = 0; i < a.size(); ++i)
        for (std::size_t j = 0; j < a[i].size(); ++j)
            r[j][i] = a[i][j];
    return r;
}

Matrix minor(const Matrix& a, std::size_t excl_row, std::size_t excl_col) {
    if (a.empty() || excl_row >= a.size() || excl_col >= a[0].size())
        throw std::logic_error("invalid minor indices");
    Matrix r(a.size() - 1, std::vector<double>(a[0].size() - 1));
    std::size_t ri = 0;
    for (std::size_t i = 0; i < a.size(); ++i) {
        if (i == excl_row) continue;
        std::size_t ci = 0;
        for (std::size_t j = 0; j < a[i].size(); ++j) {
            if (j == excl_col) continue;
            r[ri][ci++] = a[i][j];
        }
        ++ri;
    }
    return r;
}

double determinant(const Matrix& a) {
    if (a.empty()) return 1.0;  // 数学约定：空矩阵行列式为 1
    if (a.size() != a[0].size()) throw std::logic_error("determinant requires square matrix");
    if (a.size() == 1) return a[0][0];
    double det = 0.0;
    for (std::size_t j = 0; j < a[0].size(); ++j) {
        double sign = (j % 2 == 0) ? 1.0 : -1.0;
        det += sign * a[0][j] * determinant(minor(a, 0, j));
    }
    return det;
}

Matrix inverse(const Matrix& a) {
    if (a.empty()) return {};
    double det = determinant(a);
    if (std::abs(det) < 1e-12) throw std::logic_error("singular matrix");
    std::size_t n = a.size();
    if (n == 1) return Matrix{{1.0 / a[0][0]}};
    Matrix r(n, std::vector<double>(n));
    for (std::size_t i = 0; i < n; ++i)
        for (std::size_t j = 0; j < n; ++j) {
            double sign = ((i + j) % 2 == 0) ? 1.0 : -1.0;
            r[i][j] = sign * determinant(minor(a, j, i)) / det;  // 伴随矩阵转置
        }
    return r;
}

Matrix concatenate(const Matrix& a, const Matrix& b, int axis) {
    if (a.empty() || b.empty()) return a.empty() ? b : a;
    if (axis == 0 && a[0].size() != b[0].size()) throw std::logic_error("column mismatch");
    if (axis == 1 && a.size() != b.size()) throw std::logic_error("row mismatch");
    Matrix r;
    if (axis == 0) {  // 垂直拼接
        r = a;
        for (const auto& row : b) r.push_back(row);
    } else {          // 水平拼接
        r.resize(a.size());
        for (std::size_t i = 0; i < a.size(); ++i) {
            r[i] = a[i];
            for (double x : b[i]) r[i].push_back(x);
        }
    }
    return r;
}

Matrix ero_swap(const Matrix& a, std::size_t r1, std::size_t r2) {
    if (r1 >= a.size() || r2 >= a.size()) throw std::logic_error("row index out of range");
    Matrix r = a;
    std::swap(r[r1], r[r2]);
    return r;
}

Matrix ero_multiply(const Matrix& a, std::size_t row, double c) {
    Matrix r = a;
    for (auto& x : r[row]) x *= c;
    return r;
}

Matrix ero_sum(const Matrix& a, std::size_t r1, double c, std::size_t r2) {
    if (r1 >= a.size() || r2 >= a.size()) throw std::logic_error("row index out of range");
    Matrix r = a;
    // 语义：把 r1 行乘以 c 后加到 r2 行（handout 定义）
    for (std::size_t j = 0; j < r[r2].size(); ++j)
        r[r2][j] += c * a[r1][j];
    return r;
}

Matrix upper_triangular(const Matrix& a) {
    if (a.empty()) return {};
    if (a.size() != a[0].size()) throw std::logic_error("upper_triangular requires square matrix");
    Matrix r = a;
    std::size_t n = r.size();
    for (std::size_t col = 0; col < n; ++col) {
        // 找主元
        std::size_t pivot = col;
        for (std::size_t i = col + 1; i < n; ++i)
            if (std::abs(r[i][col]) > std::abs(r[pivot][col])) pivot = i;
        if (std::abs(r[pivot][col]) < 1e-12) continue;
        (void)pivot;  // 不使用换主元：题目 bonus 要求处理主元为 0 的情况
        if (std::abs(r[col][col]) < 1e-12) {
            // 主元为 0：找下方非零行，用 ero_sum 把其加到主元行（不做 swap）
            for (std::size_t k = col + 1; k < n; ++k) {
                if (std::abs(r[k][col]) > 1e-12) {
                    r = ero_sum(r, k, 1.0, col);  // row_col += 1*row_k
                    break;
                }
            }
        }
        for (std::size_t i = col + 1; i < n; ++i) {
            // 消元：row_i -= (r[i][col]/r[col][col]) * row_col
            // ero_sum(row_col, factor, row_i) 表示 row_i += factor*row_col
            double factor = -r[i][col] / r[col][col];
            r = ero_sum(r, col, factor, i);
        }
    }
    return r;
}
}
