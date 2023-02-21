
grid = [
    list("XXXXX"),
    list("XTXTX"),
    list("XXXXX"),
    list("TTXXX"),
    list("XXXXT")
]

columnCounts = [2, 0, 1, 1, 1]
numberOfColumns = len(columnCounts)
rowCounts = [1, 1, 0, 2, 1]
numberOfRows = len(rowCounts)

def getNeighbours(r, c, adjacentOnly=True):
    neighbours = [
        (r-1, c-1),
        (r-1, c),
        (r-1, c+1),
        (r, c+1),
        (r+1, c+1),
        (r+1, c),
        (r+1, c-1),
        (r, c-1)
    ]

    if adjacentOnly:
        # neighbours = [neighbours[i] for i in range(1, 8, 2)]
        neighbours = [
            neighbours[1],
            neighbours[3],
            neighbours[5],
            neighbours[7]
        ]
    
    return neighbours

def printGrid(gridToPrint):
    printString = "\\ " + ''.join([str(count) for count in columnCounts]) + '\n'
    for row in range(numberOfRows):
        printString += str(rowCounts[row]) + ' '
        printString += ''.join(gridToPrint[row]) + '\n'
    print(printString)

def placeInitialGrass(grid_):
    for r in range(numberOfRows):
        if rowCounts[r] == 0:
            grid_[r] = ['G' if val=='X' else val for val in grid_[r]]
        for c in range(numberOfColumns):
            if columnCounts[c] == 0:
                for r_ in range(numberOfRows):
                    if grid_[r_][c] == 'X':
                        grid_[r_][c] = 'G'
            
            if grid_[r][c] != 'X': continue

            neighbourValues = []
            for nR, nC in getNeighbours(r, c):
                if (nR<0) or (nR==numberOfRows) or (nC<0) or (nC==numberOfColumns): continue
                neighbourValues.append(grid_[nR][nC])
            
            if neighbourValues.count('T') == 0:
                grid_[r][c] = 'G'
    
    return grid_

printGrid(grid)
grid = placeInitialGrass(grid)
printGrid(grid)