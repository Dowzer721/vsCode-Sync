
from random import randint#, seed
# seed(0)

import pygame

from math import pi, cos, sin


def generate(colCount, rowCount, startingLocation = -1, renderScreen=-1, renderOffset=1.0):
    mazeSize = colCount * rowCount
    # print(f"c:{colCount}, r:{rowCount}, s:{mazeSize}")

    def index(c, r):
        return c + (r * colCount)

    if renderScreen != -1:
        screen = renderScreen

        screenW, screenH = screen.get_size()

        gridW = screenW / colCount
        gridH = screenH / rowCount

    Grid = []
    class Cell:
        def __init__(self, col, row):
            self.col = col
            self.row = row
            self.index = index(col, row)

            self.walls = [1,1,1,1]
            self.visited = False

            if renderScreen != -1:

                # self.corners = []
                # mx = self.col * (gridW + 0.5)
                # my = self.row * (gridH + 0.5)
                # for i in range(4):
                #     angle = (pi * 1.25) + ((pi / 2) * i)
                #     x = mx + (cos(angle) * gridW * 0.5 * renderOffset)
                #     y = my + (sin(angle) * gridH * 0.5 * renderOffset)
                #     self.corners.append((x, y))

                c = self.col
                cn = self.col + 1
                r = self.row
                rn = self.row + 1
                self.corners = [
                    (c * gridW, r * gridH),
                    (cn* gridW, r * gridH),
                    (cn* gridW, rn* gridH),
                    (c * gridW, rn* gridH)
                ]
        
        def getNeighbours(self):
            neighbours = [
                index(self.col, self.row-1),
                index(self.col+1, self.row),
                index(self.col, self.row+1),
                index(self.col-1, self.row)
            ]

            # Remove neighbours outside edges:
            if self.row == 0:
                neighbours[0] = -1
            if self.col == colCount-1:
                neighbours[1] = -1
            if self.row == rowCount-1:
                neighbours[2] = -1
            if self.col == 0:
                neighbours[3] = -1
            
            # Remove neighbours which have been visited:
            for n in range(4):
                # Skip 'n' if the neighbour is already invalid:
                if neighbours[n] == -1: continue

                if Grid[neighbours[n]].visited:
                    neighbours[n] = -1
            
            return neighbours
        
        def render(self, screen):
            for w in range(4):
                if self.walls[w] == 0: continue

                x1 = int(self.corners[w][0]) 
                y1 = int(self.corners[w][1])
                x2 = int(self.corners[(w+1)%4][0]) 
                y2 = int(self.corners[(w+1)%4][1])
                pygame.draw.line(
                    screen, (0, 0, 0),
                    (x1, y1), (x2, y2),
                    1
                )




    for row in range(rowCount):
        for col in range(colCount):
            Grid.append(Cell(col, row))
    
    currentIndex = randint(0, mazeSize - 1)
    if startingLocation != -1:
        currentIndex = index(startingLocation[0], startingLocation[1])
    # print(f"currentIndex: {currentIndex}")
    
    Grid[currentIndex].visited = True
    
    stack = [currentIndex]

    visitedCount = 1
    while(visitedCount != mazeSize-1):
        visitedCount = sum([int(Grid[i].visited) for i in range(mazeSize)])
        # print(f"vC:{visitedCount}")

        currentNeighbours = Grid[currentIndex].getNeighbours()
        
        # If there are no neighbours, step back one cell from the stack:
        if currentNeighbours.count(-1) == 4:
            currentIndex = stack.pop(-1)
            continue

        # Choose a random valid direction:
        randomDirection = randint(0, 3)
        for i in range(4):
            if currentNeighbours[(randomDirection + i) % 4] != -1:
                randomDirection = (randomDirection + i) % 4
                break
        
        # Remove the wall between the current cell and the neighbour. 
        # This requires removing both the current cell's wall and the neighbour's wall:
        Grid[currentIndex].walls[randomDirection] = 0
        neighbourInDirection = currentNeighbours[randomDirection]
        Grid[neighbourInDirection].walls[(randomDirection + 2) % 4] = 0

        # Move the current index to the neighbour cell:
        currentIndex = neighbourInDirection

        # Set current cell visited to True:
        Grid[currentIndex].visited = True

        # Push the current location to the stack:
        stack.append(currentIndex)
    
    # Make sure that all external walls are present:
    topRowIndexes = []
    bottomRowIndexes = []
    for c in range(colCount):
        topRowIndexes.append(index(c, 0))
        bottomRowIndexes.append(index(c, rowCount-1))
    
    leftColIndexes = []
    rightColIndexes = []
    for r in range(rowCount):
        leftColIndexes.append(index(0, r))
        rightColIndexes.append(index(colCount-1, r))
    
    for i in topRowIndexes:
        Grid[i].walls[0] = 1
    for i in rightColIndexes:
        Grid[i].walls[1] = 1
    for i in bottomRowIndexes:
        Grid[i].walls[2] = 1
    for i in leftColIndexes:
        Grid[i].walls[3] = 1
    
    return Grid

# col,row = 50,50

# screenW = 500
# screenH = int(screenW * (row/col))
# screen = pygame.display.set_mode((screenW, screenH))

# generate(colCount, rowCount, startingLocation = -1, renderScreen=-1)
# maze = generate(col, row, (0,0))

# screen.fill((255, 255, 255))

# for cell in maze:
#     cell.render()

# pygame.display.flip()

# input()