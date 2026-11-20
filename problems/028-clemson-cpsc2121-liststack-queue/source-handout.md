# 原始作业说明 / Original Assignment Materials

> 本题 upstream 仓库没有独立的 handout 文件——课程把作业说明嵌在**接口注释**里、
> 把验收标准写进 **13 个官方样例测试**（这正是 Clemson CPSC2121 的风格）。
> 下面按原样汇集：仓库 README（课程/实验说明）、四个头文件（含接口注释合同）、
> 官方样例测试清单。中文导读见 `01-题目解读.md`。
>
> No separate handout exists upstream: the spec lives in header comments and the
> 13 official sample test cases. Original materials collected verbatim below.

---

## 仓库 README（原文）

# CPSC 2121: Data Structures and Algorithms

## Russell Welch, Clemson University

- Sophomore, BS in Computer Science
- Spring Semester, 2023

---

### Course Objective

This repository contains the lab assignments and solutions for the CPSC 2121 course at Clemson University. The objective of this course is to study data structures and algorithms fundamental to computer science, abstract data-type concepts, measures of program running time and time complexity, and algorithm analysis and design techniques. The lab portion of the course aims to reinforce the material learned during the lecture.

### Course Requisites

The prerequisite for this course is CPSC 1020 or CPSC 1070. The corequisite for this course is the corresponding lecture, CPSC 2120.

### Assignments and Class Format

Each week, the assignment is posted on Canvas, with submission through Gradescope on Monday. Students may start work in advance; however, they are still required to attend the lab. A brief lecture is given at the beginning of each lab during Monday’s lab meeting. After the lecture, students may leave after they finish the lab assignment. Lab assignments are due by the end of the following Monday (11:59 PM) unless otherwise specified.

---

### Repository Structure

This repository contains lab assignments and solutions organized by topic. Each lab folder contains source code files, sample test cases, and additional required files, such as input files or text files.

```
CPSC2121
│
├── Lab 1 - Linked List Based Stacks and Queues
│   ├── Lab 1 Sample Test Cases
│   ├── List.h
│   ├── ListQueue.h
│   ├── ListStack.h
│   ├── Node.h
│   └── main.cpp
│
├── Lab 2 - Infix to Postfix Conversion
│   ├── Lab 2 Sample Test Cases
│   ├── infixToPostfix
│   └── infixToPostfix.cpp
│
├── Lab 3 - Finding Groups Using Recursion
│   ├── Lab 3 Sample Test Cases
│   ├── output
│   ├── CMakeLists.txt
│   ├── Grouping.cpp
│   ├── Grouping.h
│   ├── input2.txt
│   ├── input3.txt
│   └── input4.txt
│
├── Lab 4 - Searching and Sorting
│   ├── Lab 4 Sample Test Cases
│   ├── Searches.h
│   └── Sorts.h
│
├── Lab 5 - Spell Checker Using a Hash Table
│   ├── Lab 5 Sample Test Cases
│   ├── main.cpp
│   ├── stringset.cpp
│   ├── stringset.h
│   ├── wordlist.txt
│   ├── wordlist02.txt
│   ├── wordlist03.txt
│   ├── wordlist04.txt
│   └── wordlist05.txt
│
├── Lab 6 - Finding the Closest Pair of Points
│   ├── closestPair
│   ├── closestPair.cpp
│   ├── points10.txt
│   ├── points100.txt
│   ├── points250k.txt
│   └── tempCodeRunnerFile.cpp
│
├── Lab 7 - Binary Search Tree
│   ├── Lab 7 Sample Test Cases
│   ├── binarySearchTree
│   ├── binarySearchTree.cpp
│   └── binarySearchTree.h
│
├── Lab 8 - Storing a Sequence in a Binary Search Tree
│   ├── Lab 8 Sample Test Cases
│   ├── bstSequence.cpp
│   └── bstSequence.h
│
├── Lab 9 - Using Recursion to Solve the N-Queens Problem
│ ├── Lab 9 Sample Test Cases
│ ├── nQueens
│ ├── nQueens.cpp
│ └── tempCodeRunnerFile.cpp
│
├── Lab 10 - Using Breadth-First Search to Solve Puzzles
│ ├── waterJugs
│ ├── waterJugs.cpp
│ ├── wolfGoatCabbage
│ └── wolfGoatCabbage.cpp
│
├── Lab 11 - Iterative Refinement and the Traveling Salesman Problem
│ ├── Lab 11 Sample Test Cases
│ ├── cities.txt
│ ├── tspPrunedExhaustiveSearch.cpp
│ ├── tspRefine
│ └── tspRefine.cpp
│
├── .DS_Store
├── .gitignore
├── CMakeLists.txt
└── README.md
```

### How to Use This Repository

To use the code in this repository, simply clone it to your local machine and navigate to the desired lab folder. Each lab folder contains the necessary source code files, sample test cases, and additional files as required.

Compile and run the code using an appropriate compiler and IDE (e.g., GCC, Clang, Visual Studio, etc.) or by using the command line.

Please note that some labs may have specific instructions, dependencies, or requirements for compilation and execution. Be sure to read any additional README files or comments in the source code for specific lab instructions.

### Contributing

This repository is for educational purposes and personal use only. Contributions are not accepted. However, if you find an issue or have a question, please open an issue on GitHub.

### License

This repository is for personal and educational use only. The code and content in this repository are not intended for commercial use or redistribution.

### Acknowledgments

I would like to thank the faculty and staff of Clemson University's Computer Science department for their guidance and support throughout the course.


---

## 接口定义与注释合同（原文，四个头文件）

### List.h

```cpp
/*
 * Name: Russell Welch
 * Date Submitted: 1/23/23
 * Lab Section: 001
 * Assignment Name: Linked List Based Stacks and Queues
 */

#pragma once

#include <iostream>
#include <string>
#include "Node.h"
using namespace std;

//This class represents a linked list of node objects
//Do not modify anything in the class interface
template <class T>
class List{

 private:
  Node<T> * start; //pointer to the first node in this list
  int mySize;  //size (or length) of this list

 public:
  List();
  ~List();
  int size();
  bool empty();
  void insertStart(T);
  void insertEnd(T);
  void insertAt(T, int);
  void removeStart();
  void removeEnd();
  void removeAt(int);
  T getFirst();
  T getLast();
  T getAt(int);
  int find(T);

  //Print the name and this list's size and values to stdout
  //This function is already implemented (no need to change it)
  void print(string name){
    cout << name << ": ";
    cout << "size = " << size();
    cout << ", values = ";
    Node<T> * iterator = start;
    while(iterator != nullptr){
      cout << iterator->value << ' ';
      iterator = iterator->next;
    }
    cout << endl;
  }

}; //end of class interface (you may modify the code below)

//Implement all of the functions below
//Construct an empty list by initializig this list's instance variables
template <class T>
List<T>::List(){
  start = nullptr;
  mySize = 0;
}

//Destroy all nodes in this list to prevent memory leaks
template <class T>
List<T>::~List(){
  while(size() != 0) {
    removeEnd();
  }
}

//Return the size of this list
template <class T>
int List<T>::size(){
  return mySize;
}

//Return true if this list is empty
//Otherwise, return false
template <class T>
bool List<T>::empty(){
  if(size() == 0)
    return true;
  return false;
}

//Create a new node with value, and insert that new node
//into this list at start
template <class T>
void List<T>::insertStart(T value){
  Node<T>* tempStart = new Node<T>(value);
  tempStart->next = start;
  start = tempStart;
  mySize++;
}

//Create a new node with value, and insert that new node
//into this list at end
template <class T>
void List<T>::insertEnd(T value){
  Node<T> * end = new Node<T>(value);

  Node<T> * iterator = start;
  if(iterator == nullptr){
    start = end;
    mySize++;
    return;
  }
  while(iterator->next != nullptr)
    iterator = iterator->next;

  iterator->next = end;
  mySize++;
}

//Create a new node with value <value>, and insert that new node at position j
template <class T>
void List<T>::insertAt(T value, int j){
  Node<T> * iterator = start;
  
  if (j == 0)
    insertStart(value);
  else if (j == size())
    insertEnd(value);
  else {
    for(int i = 0; i < j - 1; i++)
      iterator = iterator->next;
    Node<T> * temp = new Node<T>(value);
    temp->next = iterator->next;
    iterator->next = temp;
    mySize++;
  }
}

//Remove node at start
//Make no other changes to list
template <class T>
void List<T>::removeStart(){
  Node<T> * iterator = start;
  start = iterator->next;
  delete iterator;
  mySize--;
}

//Remove node at end
//Make no other changes to list
template <class T>
void List<T>::removeEnd(){
  Node<T> * iterator = start;
  if(iterator->next == nullptr){
    delete iterator;
    start = nullptr;
    mySize--;
    return;
  }
  while(iterator->next->next != nullptr)
    iterator = iterator->next;

  delete iterator->next;
  iterator->next = nullptr;
  mySize--;
}

//Remove node at position j
//Make no other changes to list
template <class T>
void List<T>::removeAt(int j){
  Node<T> * iterator = start;
  if(j == 0)
    removeStart();
  else if(j == size() - 1)
    removeEnd();
  else {
    for(int i = 0; i < j - 1; i++)
      iterator = iterator->next;
    Node<T> * temp = iterator->next;
    iterator->next = temp->next;
    delete temp;
    mySize--;
  }
}

//Return the value of the first node in the Linked List,
//If no first node, return the default constructed value: T()
template <class T>
T List<T>::getFirst(){
  return start->value;
}

//Return the value of the last node in the Linked List,
//If no first node, return the default constructed value: T()
template <class T>
T List<T>::getLast(){
  Node<T> * iterator = start;
  while(iterator->next != nullptr)
    iterator = iterator->next;

  return iterator->value;
}

//Return the value of the node at position j in the Linked List,
//If no first node, return the default constructed value: T()
template <class T>
T List<T>::getAt(int j){
  Node<T> * iterator = start;
  for(int i = 0; i < j; i++)
    iterator = iterator->next;

  return iterator->value;
}

//Return the position of the (first) node whose value is equal to the key
//Otherwise, return -1
template <class T>
int List<T>::find(T key){
  Node<T> * iterator = start;
  for(int i = 0; i < size(); i++) {
    if(iterator->value == key)
      return i;
    iterator = iterator->next;
  }
  return -1;
}

```

### ListStack.h

```cpp
/*
 * Name: Russell Welch
 * Date Submitted: 1/23/23
 * Lab Section: 001
 * Assignment Name: Linked List Based Stacks and Queues
 */

#pragma once

#include "List.h"

//This class represents a Stack implemented via Linked List
//Do not modify anything in the class interface
template <class T>
class ListStack{

 private:
  List<T> stack;

 public:
  ListStack();
  ~ListStack();
  int size();
  bool empty();
  void push(T);
  T pop();
  //Print the name and this ListStack's size and values to stdout
  //This function is already implemented (no need to change it)
  void print(string name){
    stack.print(name);
  }

}; //end of class interface (you may modify the code below)

//Implement all of the functions below

//Construct an empty ListStack by initializing this ListStack's instance variables
template <class T>
ListStack<T>::ListStack(){
}

//Destroy all nodes in this ListStack to prevent memory leaks
template <class T>
ListStack<T>::~ListStack(){
}

//Return the size of this ListStack
template <class T>
int ListStack<T>::size(){
  stack.size();
}

//Return true if this ListStack is empty
//Otherwise, return false
template <class T>
bool ListStack<T>::empty(){
  return stack.empty();
}

//Create a node with value <value> and push it onto the stack
template <class T>
void ListStack<T>::push(T value){
  stack.insertStart(value);
}

//Pop a node from the Stack.
//Note that here that includes both removing the node from the stack
//AND returning its value.
template <class T>
T ListStack<T>::pop(){
  T value = stack.getFirst();
  stack.removeStart();
  return value;
}

```

### ListQueue.h

```cpp
/*
 * Name: Russell Welch
 * Date Submitted: 1/23/23
 * Lab Section: 001
 * Assignment Name: Linked List Based Stacks and Queues
 */

#pragma once

#include "List.h"


//This class represents a Queue implemented via Linked List
//Do not modify anything in the class interface
template <class T>
class ListQueue{

 private:
  List<T> queue;

 public:
  ListQueue();
  ~ListQueue();
  int size();
  bool empty();
  void enqueue(T);
  T dequeue();
  //Print the name and this ListQueue's size and values to stdout
  //This function is already implemented (no need to change it)
  void print(string name){
    queue.print(name);
  }

}; //end of class interface (you may modify the code below)

//Implement all of the functions below

//Construct an empty ListQueue by initializing this ListQueue's instance variables
template <class T>
ListQueue<T>::ListQueue(){
}

//Destroy all nodes in this ListQueue to prevent memory leaks
template <class T>
ListQueue<T>::~ListQueue(){
}

//Return the size of this ListQueue
template <class T>
int ListQueue<T>::size(){
  return queue.size();
}

//Return true if this ListQueue is empty
//Otherwise, return false
template <class T>
bool ListQueue<T>::empty(){
  return queue.empty();
}

//Create a new node with value, and insert that new node
//into this ListQueue in its correct position
template <class T>
void ListQueue<T>::enqueue(T value){
  queue.insertEnd(value);
}

//Dequeue an element from the queue.
//Note that here that means both removing it from the list
//AND returning the value
template <class T>
T ListQueue<T>::dequeue(){
  T value = queue.getFirst();
  queue.removeStart();
  return value;
}

```

### Node.h

```cpp
#pragma once

template <class T>
class List;

//This class represents a node in a linked list
//Do not modify anything in this file
template <class T>
class Node{

 friend class List<T>;

 private:
  T value; //value stored by this node
  Node * next; //pointer to the next node in list

public:
 Node(T v){
   value = v;
   next = nullptr;
 }

};

```

---

## 官方样例测试清单（13 个，原文文件名）

- `T1.cpp`
- `T10.cpp`
- `T12.cpp`
- `T13.cpp`
- `T14.cpp`
- `T16.cpp`
- `T18.cpp`
- `T2.cpp`
- `T20.cpp`
- `T22.cpp`
- `T4.cpp`
- `T5.cpp`
- `T8.cpp`
