
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from random import randint

import pygame
canvasW, canvasH = 600, 600
canvas = pygame.display.set_mode((canvasW, canvasH))

totalCols = totalRows = 8
cellW, cellH = canvasW / totalCols, canvasH / totalRows
# print(f"cellW:{cellW}, cellH:{cellH}")

#   x0           1
# y0 +-----o-----+
#    |     2     |
#    o 3       1 o
#    |     0     |
#  1 +-----o-----+

endPositions = [
    (0.5, 1),
    (1, 0.5),
    (0.5, 0),
    (0, 0.5)
]

# a,b,c,d = 0,1,2,3
cases = [
    (),
    (0, 3),
    (0, 1),
    (1, 3),
    (1, 2),
    (0, 1, 2, 3),
    (0, 2),
    (2, 3),
    (2, 3),
    (0, 2),
    (1, 2, 3, 0),
    (1, 2),
    (1, 3),
    (0, 1),
    (3, 0),
    ()
]

corners = []
for r in range(totalRows + 1):
    row = []
    for c in range(totalCols + 1):
        row.append(randint(0, 1))
    corners.append(row)

    # print(row)

class Cell:
    def __init__(self, row_, col_, *corners_):

        self.row, self.col = row_, col_
        
        # self.corner0, self.corner1, self.corner2, self.corner3 = corners_
        # self.caseIndex = LL.binaryListToInt([self.corner3, self.corner2, self.corner1, self.corner0])
        corner0, corner1, corner2, corner3 = corners_
        self.caseIndex = LL.binaryListToInt([corner3, corner2, corner1, corner0])
        # print(self.caseIndex)

        x1 = self.col * cellW
        y1 = self.row * cellH
        self.endPositions = []
        for index in cases[self.caseIndex]:
            x = x1 + (cellW * endPositions[index][0])
            y = y1 + (cellH * endPositions[index][1])
            self.endPositions.append((x, y))
    
    def render(self, drawGrid_=False):
        x1, y1 = int(self.col * cellW), int(self.row * cellH)
        x2, y2 = int((self.col+1) * cellW), int((self.row+1) * cellH)

        if drawGrid_:
            pygame.draw.polygon(
                canvas, 
                (200, 200, 200), 
                [
                    (x1, y2),
                    (x2, y2),
                    (x2, y1),
                    (x1, y1)
                ], 
                1
            )
        
        if self.caseIndex == 0 or self.caseIndex == 15: return

        if len(self.endPositions) == 2:
            pygame.draw.line(
                canvas, 
                (0, 0, 0), 
                (int(self.endPositions[0][0]), int(self.endPositions[0][1])),
                (int(self.endPositions[1][0]), int(self.endPositions[1][1])),
                1
            )
        else:
            pygame.draw.line(
                canvas, 
                (0, 0, 0), 
                (int(self.endPositions[0][0]), int(self.endPositions[0][1])),
                (int(self.endPositions[1][0]), int(self.endPositions[1][1])),
                1
            )
            pygame.draw.line(
                canvas, 
                (0, 0, 0), 
                (int(self.endPositions[2][0]), int(self.endPositions[2][1])),
                (int(self.endPositions[3][0]), int(self.endPositions[3][1])),
                1
            )


grid = []
for r in range(totalRows):
    row = []
    # rowStr = ""
    for c in range(totalCols):
        # Cell(row_, col_, *corners_)
        newCell = Cell( r, c, corners[r+1][c], corners[r+1][c+1], corners[r][c+1], corners[r][c] )
        # rowStr += str(newCell.caseIndex) + ', '
        row.append(newCell)
    grid.append(row)
    # print(rowStr)

# print(grid[0][0].endPositions)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.quit()
            exit(0)
        # if event.type == pygame.MOUSEBUTTONUP:
            

    canvas.fill((255, 255, 255))

    for r in range(totalRows):
        for c in range(totalCols):
            grid[r][c].render(drawGrid_=False)

    pygame.display.flip()