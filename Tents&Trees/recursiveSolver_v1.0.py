
# Classic 5x5 A1
columnCounts = [2, 0, 1, 1, 1]
numberOfColumns = len(columnCounts)
rowCounts = [1, 1, 0, 2, 1]
numberOfRows = len(rowCounts)
rowsWhichCanIncrement = [(count>0) for count in rowCounts]

def gridIsValid(grid):

    def getNeighbours(row, col, adjacentOnly=False, returnValues=False):
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

        if adjacentOnly:
            neighbours = [neighbours[(i*2)+1] for i in range(4)]
        
        for n in range(len(neighbours)):
            nR, nC = neighbours[n]
            if (-1 in neighbours[n]) or (nR==numberOfRows) or (nC==numberOfColumns):
                neighbours[n] = 'G'
            else:
                if returnValues:
                    neighbours[n] = grid[nR][nC]
        
        return neighbours
            
    # Check col/row counts against placed Tents:
    for c in range(numberOfColumns):
        col = []
        for r in range(numberOfRows):
            if grid[r].count('A') != rowCounts[r]: return False # f"rowCounts wrong ({grid[r].count('A')}/{rowCounts[r]})"
            col.append(grid[r][c])

            # Check for touching Tents:
            if grid[r][c] == 'A':
                if 'A' in getNeighbours(r, c, returnValues=True): return False # f"tents touching @({r},{c})"
            
            # Check each Tree has at least 1 Tent:
            if grid[r][c] == 'T':
                if 'A' not in getNeighbours(r, c, True, True): return False

        if col.count('A') != columnCounts[c]: return False # f"colCounts wrong ({col.count('A')}/{columnCounts[c]})"
    

    # If all checks have passed, then it can be assumed that the grid is valid:
    return True
    
# print(gridIsValid([ # Should print False
#     list("XXXXX"),
#     list("XTXTX"),
#     list("XXXXX"),
#     list("TTXXX"),
#     list("XXXXT")
# ]))

# print(gridIsValid([ # Should print True
#     list("GGGAG"),
#     list("ATGTG"),
#     list("GGGGG"),
#     list("TTAGA"),
#     list("AGGGT")
# ]))

"""
TODO: Need to come back to this with a clearer mind:

    TODO: JUST SEEN A GLARING ISSUE:
    The current method of stepping each row forward once will only work out if each row requires maximum 1 Tent. Because I am only placing 1 Tent to move. 
    In order to place more than one tent, I am wondering if I can do something with Binary. 
    As in if a row needs 1 Tent, with 4 spaces, the binary numbers the row could be are: 1000(8), 0100(4), 0010(2), 0001(1).
    
    The number of possible permutations of 2 Tents in 4 Spaces is (Tents:T, Spaces:S):
    ((T+S)!) / (T! * S!)

    Need to do some further testing to see how I might produce these permutations, and how I might do so in a meaningful way, 
    or at least in a fashion which allows me to calculate the next permutation from any given starting permutation.
    View File: recursiveFactorial.py for some calculations I have started

    -----------

    1. Starting at the final row: 

    2. Increment the Tent position once, then check the Grid's validity.
    3. If the Tent reaches the end, and the Grid isn't valid, reset the Tent.
    4. Increment the previous row's Tent once, then return to 2.


"""

def recursiveSolve(grid, rowToIncrement):
    if gridIsValid(grid): return grid

    if rowToIncrement == 0: return grid

    if rowCounts[rowToIncrement] == 0:
        return recursiveSolve(grid, rowToIncrement-1)

    # try:
    tentPosition = grid[rowToIncrement].index('A')
    # except:
    #     raise Exception(f"{rowToIncrement}")
    
    # If the Tent can be shifted right one space:
    if 'X' in grid[rowToIncrement][tentPosition:]:
        grid[rowToIncrement][tentPosition] = 'X'
        nextTentPosition = grid[rowToIncrement].index('X', tentPosition+1)
        grid[rowToIncrement][nextTentPosition] = 'A'
        recursiveSolve(grid, rowToIncrement)
    else:
        grid[rowToIncrement][tentPosition] = 'X'
        firstTentPosition = grid[rowToIncrement].index('X')
        grid[rowToIncrement][firstTentPosition] = 'A'

        nextPreviousRowToIncrement = [r for r in reversed(rowsWhichCanIncrement)].index(True, numberOfRows-rowToIncrement)
        recursiveSolve(grid, nextPreviousRowToIncrement)
        

startingGrid = [
    list("XXXXX"),
    list("XTXTX"),
    list("XXXXX"),
    list("TTXXX"),
    list("XXXXT")
]
for r in range(numberOfRows):
    if rowCounts[r] > 0:
        startingTentPosition = startingGrid[r].index('X')
        startingGrid[r][startingTentPosition] = 'A'

# print(''.join(startingGrid))

solvedGrid = recursiveSolve(startingGrid, numberOfRows-1)
print(solvedGrid)