
from time import time

"""
Steps for human-solve of Standard Puzzle:
    [When placing Tent:
        Fill surrounding 8 neighbours with Grass;
        Recheck row/col counts and fill with Grass if needed;
    ]

    1: Fill all non-tent-adjacent cells with Grass
    2: Check row/col counts and fill with Grass if needed
    3: If row/col count == (spaces + Tents), fill spaces with Tents
    4: For each Tree:
        Get number of adjacent Tents
        Get number of adjacent Empties
        If (Tents==0) and (Empties==1):
            Set Empty to Tent
    5: If a Tree has 3 Empties around a corner, set the middle to Grass, to prevent the other two being blocked
    6: TODO: When a Tree has opposite spaces, a Tent must go in one or the other. Check then if (future placed Tent + placed Tents + spaces) == row/col count.
    Repeat: Go to 2
"""

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

# Classic 15x15 A1
columnCounts = [4,2,1,5,2,2,5,1,4,2,1,5,1,3,4]
numberOfColumns = len(columnCounts)
rowCounts = [6,0,2,4,1,3,3,4,2,4,1,3,3,2,4]
numberOfRows = len(rowCounts)
grid = [
    list("XXXXXXXTTXXXXXT"),
    list("TXXTXXXXXXXTXXX"),
    list("XXXXTTXXXXXTXXX"),
    list("XXXTXXXXXXXXXTX"),
    list("TXXXXXXXTXXXXXX"),
    list("TXXXTXXXTTXXTXX"),
    list("XXXXTXXXXXXXXXX"),
    list("XXXXXXXTXXTTXXX"),
    list("XXTTXXTTXXXXXTX"),
    list("XXXXXXXXXXXTXXX"),
    list("XTXXXXXXXXXTXXT"),
    list("XXXXXTXTXXXXXXX"),
    list("TXXXXXXXTXXXXTX"),
    list("XXXXTXXXXXXXTXT"),
    list("TXTXTXXXXXXXXXX")
]

def printGrid(treeSymbol='T', tentSymbol='A', grassSymbol='G'):
    print('\\ ' + ' '.join([str(cC) for cC in columnCounts]))
    for r in range(numberOfRows):
        rowString = ""
        for c in range(numberOfColumns):
            if grid[r][c] == 'T': rowString += treeSymbol
            if grid[r][c] == 'A': rowString += tentSymbol
            if grid[r][c] == 'G': rowString += grassSymbol
            if grid[r][c] == 'X': rowString += 'X'
            rowString += ' '
        print(str(rowCounts[r]) + ' ' + rowString )

def getCellNeighbours(row, col, adjacentOnly=False, returnCoordinates=False):
    neighbours = [
        [row-1, col-1], 
        [row-1, col], 
        [row-1, col+1],
        [row,   col+1],
        [row+1, col+1],
        [row+1, col],
        [row+1, col-1],
        [row,   col-1]
    ]

    if adjacentOnly:
        neighbours = [
            neighbours[1],
            neighbours[3],
            neighbours[5],
            neighbours[7]
        ]
    
    for i in range(len(neighbours)):
        nR, nC = neighbours[i]
        if (nR==-1) or (nC==-1) or (nR==numberOfRows) or (nC==numberOfColumns):
            neighbours[i] = 'G'
        else:
            if returnCoordinates == False:
                neighbours[i] = grid[nR][nC]
    
    return neighbours

def placeTent(row, col):
    grid[row][col] = 'A'
    surroundingNeighbours = getCellNeighbours(row, col, returnCoordinates=True)
    for n in range(8):
        if surroundingNeighbours[n] == 'G': continue
        nR, nC = surroundingNeighbours[n]
        if grid[nR][nC] == 'X': grid[nR][nC] = 'G'

# 1:
def setInvalidPositionsAsGrass(): # Working
    for row in range(numberOfRows):
        for col in range(numberOfColumns):
            if grid[row][col] != 'X': continue

            adjacentNeighbours = getCellNeighbours(row, col, True)
            if adjacentNeighbours.count('T') == 0:
                grid[row][col] = 'G'

# 2:
def checkForCompletedRowCol(): # Working
    for r in range(numberOfRows):
        if grid[r].count('A') == rowCounts[r]:
            grid[r] = ['G' if val=='X' else val for val in grid[r]]
    
    for c in range(numberOfColumns):
        if [grid[r][c] for r in range(numberOfRows)].count('A') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X': grid[r][c] = 'G'

# 3:
def onlySpaceForTents(): # Working
    for r in range(numberOfRows):
        row = grid[r]
        if row.count('X') + row.count('A') == rowCounts[r]:
            for c in range(numberOfColumns):
                if grid[r][c] == 'X': placeTent(r, c)
    
    for c in range(numberOfColumns):
        col = [grid[r][c] for r in range(numberOfRows)]
        if col.count('X') + col.count('A') == columnCounts[c]:
            for r in range(numberOfRows):
                if grid[r][c] == 'X': placeTent(r, c) # grid[r][c] = 'A'

# 4:
def treeHasOneTentPosition(): # Working
    for r in range(numberOfRows):
        for c in range(numberOfColumns):
            if grid[r][c] != 'T': continue

            adjacentNeighbourPositions = getCellNeighbours(r, c, True, True)
            adjacentTentCount = 0
            adjacentEmptyCount = 0
            for n in range(4):
                if adjacentNeighbourPositions[n] == 'G': continue
                
                nR, nC = adjacentNeighbourPositions[n]
                adjacentTentCount  += int(grid[nR][nC] == 'A')
                adjacentEmptyCount += int(grid[nR][nC] == 'X')
            
            if (adjacentTentCount==0) and (adjacentEmptyCount==1):
                for n in range(4):
                    if adjacentNeighbourPositions[n] == 'G': continue
                
                    nR, nC = adjacentNeighbourPositions[n]
                    if grid[nR][nC] == 'X': 
                        placeTent(nR, nC)
                        #break

# 5:
def treeCouldBeCornerBlocked():
    for r in range(numberOfRows):
        for c in range(numberOfColumns):
            if grid[r][c] != 'T': continue

            surroundingNeighbourPositions = getCellNeighbours(r, c, returnCoordinates=True)
            surroundingNeighbourValues = []
            for n in range(8):
                if surroundingNeighbourPositions[n] == 'G': 
                    surroundingNeighbourValues.append('G')
                    continue
                
                nR, nC = surroundingNeighbourPositions[n]
                surroundingNeighbourValues.append(grid[nR][nC])
            if surroundingNeighbourValues.count('X') != 3: continue

            # At this point, there are only 3 neighbours surrounding the Tree
            
            # I'm sure this could be mathematically calculated, but this works for now:
            cornerIndexes = [
                [1,2,3],
                [3,4,5],
                [5,6,7],
                [7,0,1]
            ]
            neighbourIndexes = []
            for corner in range(4):
                cornerIndex = corner * 2        # 0, 2, 4, 6
                prevIndex = (cornerIndex+7)%8   # 7, 1, 3, 5
                nextIndex = (cornerIndex+1)%8   # 1, 3, 5, 7
                
                sNV_prev = surroundingNeighbourValues[prevIndex]
                sNV_curr = surroundingNeighbourValues[cornerIndex]
                sNV_next = surroundingNeighbourValues[nextIndex]

                if (sNV_prev=='X') and (sNV_curr=='X') and (sNV_next=='X'):
                    cornerRow, cornerColumn = surroundingNeighbourPositions[cornerIndex]
                    grid[cornerRow][cornerColumn] = 'G'
                
            # if neighbourIndexes in cornerIndexes:
            #     input(f"Corner found @ ({r},{c}), indexes {neighbourIndexes}")
            #     middleIndexR, middleIndexC = surroundingNeighbourPositions[neighbourIndexes[1]]
            #     grid[middleIndexR][middleIndexC] = 'G'
            #     return



# Complete Check:
def puzzleSolved():
    rowsComplete = columnsComplete = True
    for r in range(numberOfRows):
        if grid[r].count('A') != rowCounts[r]:
            rowsComplete = False
            break
    
    for c in range(numberOfColumns):
        if [grid[r][c] for r in range(numberOfRows)].count('A') != columnCounts[c]:
            columnsComplete = False
            break
    
    return rowsComplete and columnsComplete

giveUpTime = 10 # Seconds
startTime = time()

setInvalidPositionsAsGrass()
while not puzzleSolved():
    checkForCompletedRowCol()
    onlySpaceForTents()
    treeHasOneTentPosition()
    treeCouldBeCornerBlocked()
    
    currentTime = time()
    if (currentTime - startTime) > giveUpTime:
        print(f"Couldn't solve in {giveUpTime} seconds.")
        print(f"Placed {sum([row.count('A') for row in grid])} / {sum(rowCounts)} Tents:")
        break
checkForCompletedRowCol()

endTime = time()
if puzzleSolved(): print(f"Puzzle solved in {round(endTime - startTime, 3)} seconds: ")
printGrid(treeSymbol='T', tentSymbol='Δ', grassSymbol='v')