
import random

import os
def cls():
    os.system('cls')
cls()

N = 4

grid = [
    [int(c == 0) for c in range(N)] for _ in range(N)
]

def printGrid():
    cls()
    print("\n")
    for r in range(N):
        row = ["%d: "%r]
        for c in range(N):
            row.append(str(grid[r][c]) + " ")
        print(''.join(row))

def positionIsValid(col, row):
    # Top row takes priority:
    if row == 0: return True

    # Check the vertical spots directly above:
    for r in range(row, 0, -1):
        if grid[r][col] == 1:
            return False
    
    # Check the diagonal spots above:
    for r in range(row-1, -1, -1):
        queenColumn = grid[r].index(1)
        queenRow = r

        dx = abs(queenColumn - col)
        dy = abs(queenRow - row)
        if dx == dy:
            return False


    # Position is valid:
    return True

printGrid()
input("Enter to continue: ")

currentCheckingRow = 0
currentRowPositionValid = True
while currentCheckingRow < N:
    printGrid()
    
    queenCol = grid[currentCheckingRow].index(1)
    
    # If the current position is valid, step to the next row:
    if positionIsValid(queenCol, currentCheckingRow):
        currentCheckingRow += 1
        continue
    
    # Search for next valid position:
    newColumn = queenCol
    newPositionFound = False
    for c in range(queenCol, N):
        if positionIsValid(c, currentCheckingRow):
            newPositionFound = True
            newColumn = c
            break
    if newPositionFound:
        grid[currentCheckingRow] = [
            int(c == newColumn) for c in range(N)
        ]
        currentCheckingRow += 1
        continue
    # If no valid position is found:
    else:
        prevRowQueenColumn = grid[currentCheckingRow - 1].index(1)
        grid[currentCheckingRow - 1] = [
            int(c == prevRowQueenColumn + 1) for c in range(N)
        ]
        continue


    

print("FIN")


# for r in range(N):
#     row = []
#     for c in range(N):
#         #print("%d, %d, %d" %(c, r, int(positionIsValid(c, r))) )
#         row.append(str(int(positionIsValid(c, r))) )
#     print(''.join(row))











# Nothing I effing try has worked for this.
# This is doing my fucking head in. 
# Rosetta Code will likely have a solution which I might be able to work through to help me understand.
