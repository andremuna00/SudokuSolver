# 🧩 Sudoku Solver Project

## 🔍 Overview

This project involves creating a solver for Sudoku puzzles, using methods such as constraint propagation and optimization algorithms. The Sudoku puzzle is formalized as a constraint satisfaction problem (CSP) with specific rules and constraints. The solver is implemented using simulated annealing, a probabilistic optimization technique.
![image](https://github.com/user-attachments/assets/205e5d88-de2e-473f-bc0e-1651440990ef)

## 📐 Problem Formalization

A Sudoku puzzle consists of a 9×9 board divided into 3×3 sub-grids. The objective is to fill the grid with digits 1 to 9 such that:

🔹 Each number appears only once in every row, column, and 3×3 sub-grid.

🔹 All rows, columns, and sub-grids contain all 9 digits.

The puzzle includes pre-filled numbers, and the task is to complete the board while respecting these constraints.

## 🔢 Constraint Satisfaction Problem (CSP)

The Sudoku puzzle can be defined as:

- Variables: Each cell in the 9×9 grid.
- Domains: The set of integers from 1 to 9.
- Constraints:
    - Each digit appears only once per row, column, and sub-grid.
    - All rows, columns, and sub-grids contain all digits from 1 to 9.

## ⚙️ Implementation Details

### Input

The solver takes a 9×9 matrix as input:

- Empty cells are represented by 0.
- Pre-filled cells contain digits 1 to 9.

## Algorithm

1. Constraint Propagation:
    - Simplifies the puzzle by eliminating impossible values for each cell.

2. Simulated Annealing:
    - A probabilistic method used to find a solution by exploring the search space and gradually reducing randomness.

## 🚀 Usage Instructions

### Requirements

Install the following Python packages:

```bash
pip install numpy
dokusan
```
Note: Use Python 3.8 to ensure compatibility with the dokusan library.

### Running the Solver

Edit the boolean variables in the main function to choose the execution mode:

- TestPerformance: Set to True to evaluate the algorithm with multiple randomly generated Sudoku puzzles.
- SudokuExample: Set to True to solve the example Sudoku puzzle provided in the assignment.

### Commands

```python
# Example usage in Python
TestPerformance = False  # Run example puzzle
SudokuExample = True  # Run with generated Sudoku puzzles
```
## 📊 Results

The solver's performance can be evaluated using metrics such as:

- Accuracy in solving puzzles.
- Time taken to find a solution.

## ⚠️ Warnings

Use Python 3.8, as some functions in the dokusan library are deprecated in later versions.

## 🛠 Future Enhancements

Explore additional optimization techniques like genetic algorithms and gradient projection.

Develop a GUI for interactive solving.
