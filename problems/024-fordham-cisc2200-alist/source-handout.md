# 原始作业说明 / Original Assignment Handout

> 提取自 upstream 原仓库 `README.md`（保持原文）；中文导读见 `01-题目解读.md`。
> Extracted verbatim from the upstream repo; Chinese walkthrough in `01-题目解读.md`.

---

# CISC2200 Spring 2024 Lab3

In this lab assignment, we practice **working with dynamic array**, **working with class template**,
and **understanding testcases**.

## Download starter code

From your terminal (mac or WSL/Ubunto) window, you can use the following command to download it:

```bash
git clone https://github.com/CISC2200-Fall-24-Fordham/Lab3
```

## Programming Environment Setup

If you haven't done so already, please set up programming environment our our own computer, by following [Setup Tutorial](https://eecs280staff.github.io/tutorials/).

- The _Commannd Line Tools_ are required.

- The _C++ Dev Environment_ (VSCode) is highly recommened.

**Please follow these tutorials closely and carefully.**

## Requirements

Please implement the following member functions in the **AList.h**.

1. Implement  **addFirst** member function
2. Implement **getFirst()** member function
3. Implement **removeFirst()**  member function
4. Implement the copy constructor, note that you need to perform deep-copy
5. Implement the assignment operator. Note that you need to resize the array as needed, and perform deep-copy

## Hints

The **main.cpp** provided in this repository uses **doctests.h** framework to write testcases for the above five member functions.

You can modify the file **main.cpp** to add more testcases.

If you type **main.out**, all testcases are tested.

To run a particular subcase, specify the testcase (AList), and the subcase name in the command line:

```
./main.out -tc="AList" -sc="addFirst and getFirst"
```

## Submission

Submit your **AList.h** file at the following link by March 5th, Tuesday, midnight (11:59pm).

[lab3 submission link](https://storm.cis.fordham.edu:8443/web/project/1948)

The autograder compiles and tests your programs using
some testcases that are different from those in **main.cpp**. If your program fails some testcases, go back to review your code, and test your member functions
with different inputs.
