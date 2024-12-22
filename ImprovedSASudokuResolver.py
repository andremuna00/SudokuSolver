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
    return Energy(sudoku) == 0

def get_block_index(num):
    if num == 0:
        return 0,0
    elif num == 1:
        return 0,3
    elif num == 2:
        return 0,6
    elif num == 3:
        return 3,0
    elif num == 4:
        return 3,3
    elif num == 5:
        return 3,6
    elif num == 6:
        return 6,0
    elif num == 7:
        return 6,3
    elif num == 8:
        return 6,6

#how to random select a number from a list
def random_select (list):
    if(len(list)==0) : return None
    elif (len(list)==1) : return list[0]
    return list[random.randint(0,len(list)-1)]
    
def fill_initial_sudoku(sudoku):
    for num in range(9):
            i,j = get_block_index(num)
            zeros = []
            for k in range(i, i+3):
                for l in range(j, j+3):
                    if sudoku[k][l] == 0:
                        zeros.append((k,l))
            possible_values=[1,2,3,4,5,6,7,8,9]
            for k in range(i, i+3):
                for l in range(j, j+3):
                    if sudoku[k][l] != 0:
                        possible_values.remove(sudoku[k][l])

            for k, l in zeros:
                value = random_select(possible_values)
                sudoku[k][l] = value
                possible_values.remove(value)

#----------------------------TEMPERATURE FUNCTIONS--------------------------------#
#define a list of decreasing temperatures to 0 of length n
def schedule(n):
    initial_temperature = 0.5
    T = initial_temperature
    L = []
    for i in range(n):
        L.append(T)
        T = T - initial_temperature/n
        if T < 0.0:
            T = 0.0
    return L
    
#----------------------------SIMULATED ANNEALING--------------------------------#  
def Energy(sudoku):
    score = 162
    seen = set()
    for row in range(9):
        for col in range(9):
                seen.add(sudoku[row][col])
        score -= len(seen)
        seen.clear()
    for col in range(9):
        for row in range(9):
                seen.add(sudoku[row][col])
        score -= len(seen)
        seen.clear()
    return score

def neighbor(sudoku, initial):
    neighbors = []
    
    current = copy.deepcopy(sudoku)
    block = random.randint(0,8)
    i,j = get_block_index(block)
    zeros = []
    for k in range(i, i+3):
        for l in range(j, j+3):
            if initial[k][l] == 0:
                zeros.append((k,l))

    zero1 = random_select(zeros)
    if zero1 == None:
        neighbors.append(current)
        return neighbors
    zeros.remove(zero1)
    zero2 = random_select(zeros)
    if zero2 == None:
        neighbors.append(current)
        return neighbors
    zeros.remove(zero2)

    current[zero1[0]][zero1[1]], current[zero2[0]][zero2[1]] = current[zero2[0]][zero2[1]], current[zero1[0]][zero1[1]]
    neighbors.append(current)
    return neighbors
    

def simulated_annealing(f , sudoku, n, initial):
    current = sudoku
    for T in schedule(n):
        if(isSolved(current)):
            return current
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
        filled = copy.deepcopy(sudoku)
        fill_initial_sudoku(filled)
        print()
        
        sudokuSolved = simulated_annealing(Energy, filled, DecreasingRate, sudoku)
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
            filled = copy.deepcopy(sudoku)
            fill_initial_sudoku(filled)
            sudokuSolved = simulated_annealing(Energy, filled, DecreasingRate, sudoku)
            end = time.time()
            if isSolved(sudokuSolved):
                print("iteration:",i, "time:", end - start)
                L_perf.append(end - start)
                L_sol.append(1)
            else:
                print("Simulated annealing failed")

        print("Average time = ", sum(L_perf)/len(L_perf),"ms")
        print("Solution found:", 100*sum(L_sol)/N_test, "%")
