
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import os
# os.environ['SDL_VIDEO_WINDOW_POS'] = str(4) + "," + str(32)
os.environ['SDL_VIDEO_WINDOW_POS'] = "4, 32"

import math
import pygame
# pygame.init()

import random

import time #.time

totalCols = 6
totalRows = 8
gridLength = (totalCols * totalRows)

displayWidth, displayHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

screenW = displayHeight * 0.9
screenH = displayHeight * 0.9

if totalCols != totalRows:
    screenW *= (totalCols / totalRows)

screen = pygame.display.set_mode((int(screenW), int(screenH)))

cellW = (screenW / float(totalCols))
cellH = (screenH / float(totalRows))

def index(c_, r_):
    return c_ + (r_ * totalCols)
def indexToColRow(ind_):
    col = ind_ % totalCols
    row = int(ind_ / totalCols)
    return col, row

class Cell:
    def __init__(self, i_):
        self.col = i_ % totalCols
        self.row = math.floor(i_ / totalCols)
        self.index = i_

        self.walls = [True for _ in range(4)]
        self.visited = False
        
        x = cellW * self.col
        y = cellH * self.row
        cornerAddition = 0
        self.corners = [
            Luke.Vector(x + cornerAddition,         y + cornerAddition),
            Luke.Vector(x + cellW - cornerAddition, y + cornerAddition),
            Luke.Vector(x + cellW - cornerAddition, y + cellH - cornerAddition),
            Luke.Vector(x + cornerAddition,         y + cellH - cornerAddition)
        ]
    def wallsToVal(self):
        return int( sum([(int(self.walls[i])*math.pow(2, i)) for i in range(4)]) )

    def display(self):
        for c in range(4):
            if self.walls[c] == False: continue

            n = (c + 1) % 4
            pygame.draw.line(
                screen, (0, 0, 0),
                (self.corners[c].x, self.corners[c].y),
                (self.corners[n].x, self.corners[n].y),
                1
            )
        
        # visitedColour = (0, 255, 0) if self.visited else (255, 0, 0)
        # pygame.draw.line(
        #     screen, visitedColour,
        #     (self.corners[0].x, self.corners[0].y),
        #     (self.corners[2].x, self.corners[2].y),
        #     1
        # )
        # pygame.draw.line(
        #     screen, visitedColour,
        #     (self.corners[1].x, self.corners[1].y),
        #     (self.corners[3].x, self.corners[3].y),
        #     1
        # )

Grid = [Cell(i) for i in range(gridLength)]

def drawGrid():
    screen.fill((255, 255, 255))
    for cell in Grid:
        cell.display()
    pygame.display.flip()

midRow = int(totalRows / 2) - 1
midCol = int(totalCols / 2) - 1
goalIndices = [
    index(midCol, midRow),
    index(midCol+1, midRow),
    index(midCol+1, midRow+1),
    index(midCol, midRow+1)
]

for i in range(4):
    Grid[goalIndices[i]].visited = True
    Grid[goalIndices[i]].walls[(i+1)%4] = False
    Grid[goalIndices[i]].walls[(i+2)%4] = False

Grid[index(totalCols-1, 0)].visited = True
Grid[index(totalCols-1, 0)].walls[2] = False
Grid[index(totalCols-1, 1)].walls[0] = False

currentIndex = goalIndices[random.randint(0, 3)]
pathingStack = [currentIndex]
pathingStack.extend([-1 for _ in range(gridLength-2)])
def pushToStack(index_):
    i = pathingStack.index(-1)
    pathingStack[i] = index_
def popStack():
    i = pathingStack.index(-1) - 1
    ret = pathingStack[i]
    pathingStack[i] = -1
    return ret

print(pathingStack)

def getMoveableNeighbours(index_):
    col = index_ % totalCols
    row = int(index_ / totalCols)
    
    # Remove neighbours outside of edges:
    # global index
    neighbours = [
        index(col, row - 1) if (row > 0) else -1,
        index(col + 1, row) if (col < totalCols - 1) else -1,
        index(col, row + 1) if (row < totalRows - 1) else -1,
        index(col - 1, row) if (col > 0) else -1
    ]

    for n in range(4):
        if neighbours[n] == -1: continue

        if Grid[neighbours[n]].visited == True:
            neighbours[n] = -1
    
    return neighbours

def removeSeparatingWalls(previousIndex, nextIndex):
    diffIndex = previousIndex - nextIndex
    if diffIndex == totalCols:
        # next is above of previous
        Grid[previousIndex].walls[0] = False
        Grid[nextIndex].walls[2] = False
    elif diffIndex == -1:
        # next is right of previous
        Grid[previousIndex].walls[1] = False
        Grid[nextIndex].walls[3] = False
    elif diffIndex == -totalCols:
        # next is below of previous
        Grid[previousIndex].walls[2] = False
        Grid[nextIndex].walls[0] = False
    elif diffIndex == 1:
        # next is left of previous
        Grid[previousIndex].walls[3] = False
        Grid[nextIndex].walls[1] = False

startTime = time.time()

frameCount = 0
visitedCount = 0
while (visitedCount < gridLength):
    # drawGrid()

    currentCol, currentRow = indexToColRow(currentIndex)
    currentNeighbours = getMoveableNeighbours(currentIndex)
    
    nextIndex = -1
    nextNeighbour = random.randint(0, 3)
    for i in range(4):
        if currentNeighbours[(nextNeighbour + i) % 4] != -1:
            nextIndex = currentNeighbours[(nextNeighbour + i) % 4]
    
    if nextIndex == -1:
        currentIndex = popStack()
        continue
    
    pushToStack(nextIndex)
    # print(pathingStack)

    removeSeparatingWalls(currentIndex, nextIndex)
    Grid[nextIndex].visited = True
    currentIndex = nextIndex
    
    visitedCount = sum([Grid[i].visited for i in range(gridLength)] )
    print("Maze Completion: %.2F%%" %(visitedCount * 100 / gridLength))

print("Maze created successfully \n\n")

for r in range(totalRows):
    rowString = ""
    for c in range(totalCols):
        i = index(c, r)
        rowString += str(Grid[i].wallsToVal()) + " "
    print(rowString)

drawGrid()
input()