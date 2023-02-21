
from copy import deepcopy
from random import randint

RES = 4
grid = [
    [0 for _ in range(RES)]
    for _ in range(RES)
]

def recursivelyFill(previousGrid, recursionLevel):
    if recursionLevel == 0: 
        return previousGrid

    newGrid = deepcopy(previousGrid)

    randomRow = randint(0, RES-1)
    randomCol = randint(0, RES-1)

    newGrid[randomRow][randomCol] = 1

    return recursivelyFill(newGrid, recursionLevel - 1)

print(f"Grid before recursion: {grid}")
print(f"Grid after recursion: {recursivelyFill(grid, RES**2)}")
