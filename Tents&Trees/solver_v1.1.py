
# Classic 5x5 A1
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

# Classic 10x10 A1
# columnCounts = [4,1,2,1,3,1,3,0,2,3]
# numberOfColumns = len(columnCounts)
# rowCounts = [3,0,2,2,0,5,0,4,0,4]
# numberOfRows = len(rowCounts)
# grid = [
#     list("XTXXXXXXTX"),
#     list("TXXXXTXXXX"),
#     list("XXXXXXXXTX"),
#     list("XTTXXXXXXX"),
#     list("XXXXXXXXXX"),
#     list("XTXXXTXXXX"),
#     list("TTXXTXTXXT"),
#     list("XXXXXTXXXX"),
#     list("TXXXXXXXTX"),
#     list("XXXTXXXTXT")
# ]

# Large 20x20 A1
columnCounts = [5,4,3,4,4,3,6,1,6,2,4,3,5,4,4,2,7,2,5,4]
numberOfColumns = len(columnCounts)
rowCounts = [6,2,6,1,8,0,8,1,9,0,7,1,7,1,3,3,4,3,5,3]
numberOfRows = len(rowCounts)
grid = [
    list("XTTXXXXXXXXXXXXXXTTX"),
    list("XXXXXXTXXXXTXTXXXXTX"),
    list("XXXXXXXXTXXXXTXXXTXX"),
    list("XTXXXXTXXXXXTXTXTXTX"),
    list("XTXXTXXTXTXTXXXTXXXX"),
    list("XXXXXXXXXXXXXXXXXTXX"),
    list("XTXXXXXXTXXXXTTXXXXX"),
    list("XXTXTXTXTXTXXXTXTXXT"),
    list("TXXTXXXXXXXXXTXXXTXX"),
    list("XXXXXXTXTXXXXXXXXXXX"),
    list("XXXXXXTXXXXXXTXXXXXX"),
    list("TTTXXXXXXXXTTXXXTXXX"),
    list("XXXTXXXXXXTXXXTXXXXT"),
    list("XXXXXXXTXXXXXXXXTTXX"),
    list("XXXXXXXTXXXXXTXTXXXX"),
    list("XXTXXXXXXXTXXXXXXXXX"),
    list("XTXTXXXXXXXXXTXXXXXT"),
    list("XXXXXTXXTXXTXXXXXXXX"),
    list("TXXXXTXXXXTXXXTXXXTX"),
    list("XXTXTXXXTXXXXXXXXTXX")
]

"""
The solver is stuck on this 20x20 puzzle. Either there is a bug, or I need to implement more logic into the solver, because currently 
it is being too generous with placing grass. 
I am not entirely sure why this is, because it appears to me that the logic in place should not be allowing such placement, 
but nonetheless, here we are. :P

"""

def printGrid(pause=False):
    for r in range(numberOfRows):
        print(' '.join(grid[r]))
    print()
    if pause: input()
# printGrid()

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
        neighbours = [
            neighbours[1],
            neighbours[3],
            neighbours[5],
            neighbours[7]
        ]
        return neighbours

    # print(neighbours)
    
    return neighbours
    

def setTent(r_, c_):
    
    try:
        grid[r_][c_] = 'A'
    except: 
        raise Exception(f"r:{r_}, c:{c_}")
    
    # For each placed Tent, set the surrounding 8 cells as Grass:
    neighbours = getCellNeighbours(r_, c_)
    for nR, nC in neighbours:
        if (nR == -1) or (nC == -1) or (nR == numberOfRows) or (nC == numberOfColumns): continue
        if grid[nR][nC] == 'X': grid[nR][nC] = 'G'



# Can I place a tent here?
def validTentPosition(checkRow, checkCol):
    # Needs to be an empty space:
    if grid[checkRow][checkCol] != 'X': return False

    currentNeighbours = getCellNeighbours(checkRow, checkCol, True)

    adjacentTreeCount = 0
    adjacentTentCount = 0
    for nR, nC in currentNeighbours:
        if (nR==-1) or (nC==-1) or (nR==numberOfRows) or (nC==numberOfColumns): continue
        adjacentTreeCount += int(grid[nR][nC] == 'T')
        adjacentTentCount += int(grid[nR][nC] == 'A')
    
    # Needs to be an adjacent tree:
    if adjacentTreeCount == 0: return False
    
    # Needs to be no adjacent tents:    
    if adjacentTentCount > 0: return False

    # Needs to be available space to fit into row/col count.
    row = grid[checkRow]
    col = [grid[r][checkCol] for r in range(numberOfRows)]
    if (row.count('A') == rowCounts[checkRow]) or (col.count('A') == columnCounts[checkCol]): return False

    return True

def tentCountMet_FillGrass():
    for r in range(numberOfRows):
        if grid[r].count('A') == rowCounts[r]:
            grid[r] = ['G' if val=='X' else val for val in grid[r]]
    
    for c in range(numberOfColumns):
        col = [grid[r][c] for r in range(numberOfRows)]
        if col.count('A') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X': grid[r][c] = 'G'


# for r in range(numberOfRows):
#     for c in range(numberOfColumns):
#         if validTentPosition(r, c): continue
#         if grid[r][c] != 'X': continue

#         grid[r][c] = 'G'

def tentCountEquals_RemainingSpaces():
    for r in range(numberOfRows):
        if grid[r].count('X') + grid[r].count('A') == rowCounts[r]:
            grid[r] = ['A' if val=='X' else val for val in grid[r]]
    
    for c in range(numberOfColumns):
        col = [grid[r][c] for r in range(numberOfRows)]
        if col.count('X') + col.count('A') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X' and validTentPosition(r, c): 
                    setTent(r, c)


def treeHasOneTentPosition():
    for r in range(numberOfRows):
        for c in range(numberOfColumns):
            if grid[r][c] != 'T': continue

            treeAdjacentNeighbours = getCellNeighbours(r, c, True)
            neighbourValues = []
            for nR, nC in treeAdjacentNeighbours:
                if (nR == -1) or (nC == -1) or (nR == numberOfRows) or (nC == numberOfColumns):
                    neighbourValues.append('O') # Just using a different letter as a placeholder in the list, so that indexing works in the future
                else:
                    neighbourValues.append(grid[nR][nC])
            
            # print(f"R:{r}, C:{c}")
            # print(neighbourValues)

            if neighbourValues.count('A') == 0 and neighbourValues.count('X') == 1:
                tR, tC = treeAdjacentNeighbours[neighbourValues.index('X')]
                if validTentPosition(tR, tC):
                    setTent(tR, tC)

def canOnlyBeGrass():
    for r in range(numberOfRows):
        for c in range(numberOfColumns):
            if grid[r][c] != 'X': continue

            adjacentNeighbours = getCellNeighbours(r, c, True)
            treeAdjacent = False
            for nR, nC in adjacentNeighbours:
                if (nR==-1) or (nR==numberOfRows) or (nC==-1) or (nC==numberOfColumns): continue
                if grid[nR][nC] == 'T': 
                    treeAdjacent = True
                    break
            
            if treeAdjacent == False:
                grid[r][c] = 'G'

def gridComplete():
    numberOfTents = sum([grid[r].count('A') for r in range(numberOfRows)])
    return numberOfTents == sum(rowCounts)
    
    # for r in range(numberOfRows):
    #     if grid[r].count('A') != rowCounts[r]: return False
    
    # return True


# while not gridComplete():
for _ in range(numberOfColumns * numberOfRows * 10):
    canOnlyBeGrass()
    tentCountMet_FillGrass()
    tentCountEquals_RemainingSpaces()
    treeHasOneTentPosition()

# for r in range(numberOfRows):
#     for c in range(numberOfColumns):
#         if grid[r][c] == 'X': grid[r][c] = 'G'


printGrid()


