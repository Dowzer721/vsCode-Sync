
# Classic 5x5 A1:
# 
# \ 2 0 1 1 1
# 1 X X X X X
# 1 X T X T X
# 0 X X X X X
# 2 T T X X X
# 1 X X X X T

# columnCounts = [2, 0, 1, 1, 1]
# numberOfColumns = len(columnCounts)
# rowCounts = [1, 1, 0, 2, 1]
# numberOfRows = len(rowCounts)
# grid = [
#     list("XXXXX"),
#     list("XTXTX"),
#     list("XXXXX"),
#     list("TTXXX"),
#     list("XXXXT")
# ]

columnCounts = [4,1,2,1,3,1,3,0,2,3]
numberOfColumns = len(columnCounts)
rowCounts = [3,0,2,2,0,5,0,4,0,4]
numberOfRows = len(rowCounts)
grid = [
    list("XTXXXXXXTX"),
    list("TXXXXTXXXX"),
    list("XXXXXXXXTX"),
    list("XTTXXXXXXX"),
    list("XXXXXXXXXX"),
    list("XTXXXTXXXX"),
    list("TTXXTXTXXT"),
    list("XXXXXTXXXX"),
    list("TXXXXXXXTX"),
    list("XXXTXXXTXT")
]
# input(grid)

# columnCounts = [int(pos) for pos in list(input("Enter the tent counts along the top of the grid (eg. 02201): "))]
# numberOfColumns = len(columnCounts)

# rowCounts = []

# print("Row Input format: [Tent Count][Tree Positions]")
# print("Example Input: 0023 -> There are 0 tents to place, then there are trees in positions 0, 2, 3.")
# print("If there are no trees, just enter the tent count.")
# print("To finish, leave input empty.")

# grid = []
# rowIndex = 0
# while True:
#     rowValues = [int(val) for val in list(input(f"Enter row {rowIndex}: ")) ]
#     if rowValues == []:
#         break
#     # print(rowValues)

#     # Add the first value to the rowCounts list:
#     rowCounts.append(rowValues[0])

#     # Add a list to grid to represent the row:
#     if rowValues == [0]:
#         grid.append(['G' for _ in range(numberOfColumns)])
#     else:
#         grid.append(['X' for _ in range(numberOfColumns)])

#     if len(rowValues) > 1:
#         for treePosition in rowValues[1:]:
#             grid[-1][treePosition] = 'T'

#     rowIndex += 1

# numberOfRows = rowIndex

# print(grid)

# At this point, grid should contain all the blank and tree positions.



# Step 1: Find positions which have no adjacent Trees, and set those to Grass.
# Step 2: Check col/row counts match number of Tents, and if so, set the rest to Grass.
# Step 3: Check col/row counts match number of empty cells, and if so, set them to Tents.
# Step 3.1: For each placed Tent, set the surrounding 8 cells as Grass.
# Goto 2

# Step 1:
def getCellNeighbours(row, col, onlyAdjacent=False):
    neighbours = [
        [row-1, col-1],
        [row-1, col],
        [row-1, col+1],
        [row, col+1],
        [row+1, col+1],
        [row+1, col],
        [row+1, col-1],
        [row, col-1]
    ]

    if onlyAdjacent:
        return [
            neighbours[1],
            neighbours[3],
            neighbours[5],
            neighbours[7]
        ]

    # print(neighbours)
    return neighbours

for r in range(numberOfRows):
    for c in range(numberOfColumns):
        if grid[r][c] == 'T': continue

        neighbours = getCellNeighbours(r, c, True)
        treeCount = 0 # = sum([int(grid[nr][nc]=='T') for nr, nc in neighbours])
        for nR, nC in neighbours:
            if (nR == -1) or (nC == -1) or (nR == numberOfRows) or (nC == numberOfColumns): continue
            if grid[nR][nC] == 'T': treeCount += 1
        
        if treeCount == 0:
            grid[r][c] = 'G'

# input(grid)
# End (Step 1)

def setTent(r_, c_):
    grid[r_][c_] = 'A'
    
    # For each placed Tent, set the surrounding 8 cells as Grass:
    neighbours = getCellNeighbours(r_, c_)
    for nR, nC in neighbours:
        if (nR == -1) or (nC == -1) or (nR == numberOfRows) or (nC == numberOfColumns): continue
        if grid[nR][nC] == 'X': grid[nR][nC] = 'G'

def repeatingSolveSteps():
    
    # Check col/row counts match number of Tents, and if so, set the rest to Grass:
    for r in range(numberOfRows):
        row = grid[r]
        if row.count('A') == rowCounts[r]:
            grid[r] = ['G' if val=='X' else val for val in row]
    
    for c in range(numberOfColumns):
        col = [grid[r][c] for r in range(numberOfRows)]
        if col.count('A') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X': grid[r][c] = 'G'
    

    # Check col/row counts match number of empty cells, and if so, set them to Tents.
    for r in range(numberOfRows):
        row = grid[r]
        if row.count('X') == rowCounts[r]:
            for c in range(numberOfColumns):
                if grid[r][c] == 'X': setTent(r, c)
            #grid[r] = ['A' if val=='X' else val for val in row]
    
    for c in range(numberOfColumns):
        col = [grid[r][c] for r in range(numberOfRows)]
        if col.count('X') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X': 
                    setTent(r, c)
    

def gridComplete():
    for r in range(numberOfRows):
        if grid[r].count('A') != rowCounts[r]: return False
    return True

def printGrid(pause=False):
    for r in range(numberOfRows):
        print(' '.join(grid[r]))
    if pause: input()

while (not gridComplete()):
    # input(grid)
    printGrid(True)

    repeatingSolveSteps()

print("Puzzle Solved: \n")
printGrid()