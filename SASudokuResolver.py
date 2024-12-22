import random
import copy
import math
from dokusan import generators
import numpy as np
import time

#----------------------------AUX FUNCTIONS--------------------------------#
#prints the sudoku
def printSudoku(sudoku):
    def expandLine(line):
        return line[0]+line[5:9].join([line[1:5]*(2)]*3)+line[9:13]
    line0  = expandLine("╔═══╤═══╦═══╗")
    line1  = expandLine("║ . │ . ║ . ║")
    line2  = expandLine("╟───┼───╫───╢")
    line3  = expandLine("╠═══╪═══╬═══╣")
    line4  = expandLine("╚═══╧═══╩═══╝")
    symbol = " 1234567890"
    nums   = [ [""]+[symbol[n] for n in row] for row in sudoku ]
    print(line0)
    for r in range(1,10):
        print("".join(n+s for n,s in zip(nums[r-1],line1.split("."))))
        print([line2,line3,line4][(r%9==0)+(r%3==0)])

#check if the sudoku is solved
def isSolved(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return False
    return True

#find the previous empty cell
def find_previous_empty_cell(row,col,initial):
    #explore a matrix backwards
    for i in range(8, -1, -1):
        for j in range(8, -1, -1):
            if initial[i][j] == 0:
                if i < row or (i == row and j < col):
                    return i, j
    return -1, -1
    
#get the next empty cell
def nextCell(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j

#check if the value is valid
def isValid(sudoku, row, col, value):
    #row
    for i in range(9):
        if sudoku[row][i] == value:
            return False
    #col
    for i in range(9):
        if sudoku[i][col] == value:
            return False
    #3x3
    for i in range(3):
        for j in range(3):
            if sudoku[(row // 3) * 3 + i][(col // 3) * 3 + j] == value:
                return False

    return True

#----------------------------TEMPERATURE FUNCTIONS--------------------------------#
#how to random select a number from a list
def random_select (list):
    return list[random.randint(0,len(list)-1)]

#define a list of decreasing temperatures to 0 of length n
def schedule(n):
    initial_temperature = 10
    T = initial_temperature
    L = []
    for i in range(n):
        L.append(T)
        T = T - (initial_temperature/n)
        if T < 0.0:
            T = 0.0
    return L

#----------------------------SIMULATED ANNEALING--------------------------------#   
#calculate the number of empty cells
def Energy(sudoku):
    count = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                count += 1
    return count

def neighbor(current, initial):
    row, col = nextCell(current)
    L = []
    # add next state to neighbor list
    for i in range(1, 10):
        if isValid(current, row, col, i):
            sudoku_copy = copy.deepcopy(current)
            sudoku_copy[row][col] = i
            L.append(sudoku_copy)

    # add previous state to neighbor list
    row_prev, col_prev = find_previous_empty_cell(row, col, initial)
    if row_prev != -1 and col_prev != -1:
       sudoku_copy = copy.deepcopy(current)
       sudoku_copy[row_prev][col_prev] = 0
       L.append(sudoku_copy)
    return L

def simulated_annealing(f , initial, n):
    current = initial
    for T in schedule(n):
        if T == 0 or isSolved(current):
            return current
        next = random_select(neighbor(current, initial))
        de = f(next) - f(current)
        if de < 0:
            current = next
        else :
            if random.uniform(0,1) < math.exp(- de/T):
                current = next
    return current

if __name__ == "__main__":

    sudoku  = [ [3, 7, 0, 5, 0, 0, 0, 0, 6],
                [0, 0, 0, 3, 6, 0, 0, 1, 2],
                [0, 0, 0, 0, 9, 1, 7, 5, 0],
                [0, 0, 0, 1, 5, 4, 0, 7, 0],
                [0, 0, 3, 0, 7, 0, 6, 0, 0],
                [0, 5, 0, 6, 3, 8, 0, 0, 0],
                [0, 6, 4, 9, 8, 0, 0, 0, 0],
                [5, 9, 0, 0, 2, 6, 0, 0, 0],
                [2, 0, 0, 0, 0, 5, 0, 6, 4] ]

    TestPerformance = False
    SudokuExample = True

    #------------------------------SOLVE SUDOKU EXAMPLE-----------------------#
    if SudokuExample:
        DecreasingRate = 10000
        print("Sudoku:")
        printSudoku(sudoku)
        print()
        sudokuSolved = simulated_annealing(Energy, sudoku, DecreasingRate)
        print("Sudoku is solved:", isSolved(sudokuSolved))
        print("Sudoku Energy:" + str(Energy(sudokuSolved)))
        printSudoku(sudokuSolved)

    #-------------------------------TEST PERFORMANCE-------------------------------#
    if TestPerformance:
        DecreasingRate = 50000
        Avg_rank = 70
        L_perf = []
        L_sol = []
        N_test = 100
        for i in range(N_test):
            #measure time
            start = time.time()
            sudoku = np.array(list(str(generators.random_sudoku(avg_rank=Avg_rank))))
            sudoku = sudoku.reshape(9,9)
            sudoku = sudoku.astype(int)
            resolved = simulated_annealing(Energy, sudoku, DecreasingRate)
            end = time.time()
            if isSolved(resolved):
                print("iteration:",i, "time:", end - start)
                L_perf.append(end - start)
                L_sol.append(1)
            else:
                print("Simulated annealing failed")

        print("Average time = ", sum(L_perf)/len(L_perf),"ms")
        print("Solution found:", 100*sum(L_sol)/N_test, "%")

    
