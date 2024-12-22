from dokusan import generators
import numpy as np
import time
import copy


#------------------AUX FUNCTION----------------------------
#generate the sudoku domains matrix
def FillSudokuDomains(sudoku, domains):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                for k in range(9):
                    if isValid(sudoku, i, j, k+1):
                        domains[i][j].add(k+1)
            else:
                domains[i][j].add(sudoku[i][j])

#update sudoku domains matrix
def UpdateDomains(row, col, k, sudokuDomains):
    #row
    for i in range(9):
        if k in sudokuDomains[row][i]:
            sudokuDomains[row][i].remove(k)
    #col
    for i in range(9):
        if k in sudokuDomains[i][col]:
            sudokuDomains[i][col].remove(k)
    #3x3
    for i in range(3):
        for j in range(3):
            if k in sudokuDomains[(row // 3) * 3 + i][(col // 3) * 3 + j]:
                sudokuDomains[(row // 3) * 3 + i][(col // 3) * 3 + j].remove(k)
    sudokuDomains[row][col].add(k)
    return sudokuDomains

#print sudoku
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

#get the next empty cell with smallest
def nextCell(sudoku, domains):
    minSet = 10
    row = 0
    col = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0 and len(domains[i][j]) < minSet:
                minSet = len(domains[i][j])
                row = i
                col = j
    return row, col

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
#------------------SOLVING----------------------------
#solve the sudoku
def solveSudoku(sudoku, domains):
    if isSolved(sudoku):
        return True

    row, col = nextCell(sudoku, domains)
    for i in domains[row][col]:
        sudoku[row][col] = i
        #Forward checking
        newDomains = UpdateDomains(row, col, i, copy.deepcopy(domains))
        #recursive call (descending the branch of BT three)
        if solveSudoku(sudoku, newDomains):
            return True
        #backtracking if sudoku is not solved (returning to the previous state of BT three)
        else:
            sudoku[row][col] = 0
        #if i is not a valid input for empty cell we proceed with the next number
    return False

#main function
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

    if SudokuExample:
        sudokuDomains = np.array([set() for i in range(81)]).reshape(9,9)
        print("Sudoku:")
        printSudoku(sudoku)
        print()
        FillSudokuDomains(sudoku, sudokuDomains)
        if solveSudoku(sudoku, sudokuDomains):
            print("Sudoku is solved:")
            printSudoku(sudoku)
        else:
            print("There is no solutions for this sudoku")
        
    if TestPerformance:
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
            sudokuDomains = np.array([set() for i in range(81)]).reshape(9,9)
            FillSudokuDomains(sudoku, sudokuDomains)
            if solveSudoku(sudoku, sudokuDomains):
                end = time.time()
                print("iteration:",i, "time:", end - start)
                L_perf.append(end - start)
                L_sol.append(1)
            else:
                print("There is no solutions for this sudoku")
        print("Average time = ", sum(L_perf)/len(L_perf),"ms")
        print("Solution found:", 100*sum(L_sol)/N_test, "%")

