
import sys
recursionLimit = sys.getrecursionlimit()
# print(recursionLimit)
sys.setrecursionlimit(int(recursionLimit * 1.5))

N = 5

possibleRows = [format(2**i, f"#0{N+2}b")[2:] for i in range(N)]
# print(possibleRows)

def getDiagonalPositions(startingRow, startingCol):
    directionalRowAdditions = [-1, -1, 1, 1]
    directionalColAdditions = [-1, 1, 1, -1]
    diagonalPositions = []
    for direction in range(4):
        for step in range(1, N):
            nextRow = startingRow + (directionalRowAdditions[direction] * step)
            nextCol = startingCol + (directionalColAdditions[direction] * step)
            if (nextRow < 0) or (nextRow == N) or (nextCol < 0) or (nextCol == N):
                break
            diagonalPositions.append((nextRow, nextCol))
    
    return diagonalPositions

def gridIsValid(grid):
    # Check the columns of grid:
    for c in range(N):
        if [grid[r][c] for r in range(N)].count('1') > 1: return False
    
    # Check the diagonals of grid:
    for r in range(N):
        for c in range(N):
            if grid[r][c] != '1': continue
            for dR, dC in getDiagonalPositions(r, c):
                if grid[dR][dC] == '1': return False
    
    return True

def getValidGrid(initialGrid=[possibleRows[0] for _ in range(N)]):
    if gridIsValid(initialGrid): return initialGrid

    initialGrid_RowIndices = [possibleRows.index(row) for row in initialGrid]
    initialGrid_RowIndices[-1] += 1

    for row in range(N-2, -1, -1):
        initialGrid_RowIndices[row] += int(
            initialGrid_RowIndices[row + 1] == N
        )
    initialGrid_RowIndices = [(initialGrid_RowIndices[row] % N) for row in range(N)]

    newInitialGrid = [possibleRows[initialGrid_RowIndices[row]] for row in range(N)]
    
    return getValidGrid(newInitialGrid)

def printGrid(gridToPrint, queenChar='Q', notQueenChar='-'):
    printString = ""
    for row in range(N):
        for gridValue in gridToPrint[row]:
            printString += queenChar if (gridValue=='1') else notQueenChar
        printString += '\n'
    print(printString)

printGrid(getValidGrid())