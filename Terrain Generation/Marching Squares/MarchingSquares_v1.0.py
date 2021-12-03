
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from random import randint

import pygame
canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

gridSize = (5, 5)
cellW, cellH = (canvasW/gridSize[0]), (canvasH/gridSize[1])

class Cell:
    def __init__(self, column_, row_, value_=None):
        self.col, self.row = column_, row_

        if value_ != None: self.corners = LL.intToBinaryList(value_)
        else: self.corners = []

        self.cornerLocations = [
            (self.col * cellW, self.row * cellH),
            ((self.col+1) * cellW, self.row * cellH),
            ((self.col+1) * cellW, (self.row+1) * cellH),
            (self.col * cellW, (self.row+1) * cellH)
        ]
    
    def render(self):
        # startLocations = self.cornerLocations
        # endLocations = self.cornerLocations[1:] + [self.cornerLocations[0]]
        # for (x1, y1), (x2, y2) in zip(startLocations, endLocations):
        
        for (x1, y1), (x2, y2) in zip(self.cornerLocations, self.cornerLocations[1:] + [self.cornerLocations[0]]):
            pygame.draw.line(
                canvas, (0, 0, 0),
                (x1, y1), (x2, y2),
                1
            )
        
        for corner in self.corners:


grid = []
for r in range(gridSize[1]):
    for c in range(gridSize[0]):
        cornerValue = randint(0, 15)
        grid.append(Cell(c, r, cornerValue))


# Each cell can have 0-4 of its corners holding either a 0 or a value, meaning there are 
# 2^4 combinations (16). To represent this, I am using this lookup table as reference: 
# http://users.polytech.unice.fr/~lingrand/MarchingCubes/resources/marchingS.gif,
# and storing those values in the following list. 
# 
# Because the states of each corner can be represented in binary (ie having a value or not), blah blah blah

corners = [
    LL.intToBinaryList(i, 4)
    for i in range(16)
]

x1_0 = int(canvasW * 0.1)
y1_0 = int(canvasH * 0.1)
x1_5 = int(canvasW * 0.5)
y1_5 = int(canvasH * 0.5)
x2_0 = int(canvasW * 0.9)
y2_0 = int(canvasH * 0.9)

displayCorners = [
    (x1_0, y2_0),
    (x2_0, y2_0),
    (x2_0, y1_0),
    (x1_0, y1_0)
]

cornerLinePoints = [
    [],
    [(x1_0, y1_5, x1_5, y2_0)],
    [(x1_5, y2_0, x2_0, y1_5)],
    [(x1_0, y1_5, x2_0, y1_5)],
    [(x2_0, y1_5, x1_5, y1_0)],
    [(x1_5, y2_0, x2_0, y1_5), (x1_5, y1_0, x1_0, y1_5)],
    [(x1_5, y1_0, x1_5, y2_0)],
    [(x1_5, y1_0, x1_0, y1_5)],
    [(x1_5, y1_0, x1_0, y1_5)],
    [(x1_5, y1_0, x1_5, y2_0)],
    [(x1_0, y1_5, x1_5, y2_0), (x2_0, y1_5, x1_5, y1_0)],
    [(x2_0, y1_5, x1_5, y1_0)],
    [(x1_0, y1_5, x2_0, y1_5)],
    [(x1_5, y2_0, x2_0, y1_5)],
    [(x1_0, y1_5, x1_5, y2_0)],
    []
]



cornerCounter = 0
while True:
    canvas.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            cornerCounter = (cornerCounter + 1) % 16
    
    # pygame.draw.polygon(
    #     canvas,
    #     (0, 0, 0),
    #     displayCorners, 
    #     1
    # )

    # for i in range(4):
    #     if corners[cornerCounter][i] == 1:
    #         pygame.draw.circle(
    #             canvas,
    #             (0, 0, 0),
    #             displayCorners[i],
    #             8, 0
    #         )
    
    # for x1, y1, x2, y2 in cornerLinePoints[cornerCounter]:
    #     pygame.draw.line(
    #         canvas, 
    #         (255, 0, 0), 
    #         (x1, y1), 
    #         (x2, y2), 
    #         1
    #     )

    for C in grid:
        C.render()


    pygame.display.flip()