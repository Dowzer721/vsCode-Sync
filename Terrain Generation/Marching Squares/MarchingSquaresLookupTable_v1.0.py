
# This is correctly drawing the squares and their contour lines on screen, but I need to figure out two things;
#
# 1. Linear Interpolation for the lines. 
# At the moment, the lines are all straight, and starting halfway along the edges of the containing cells. 
# With linear interpolation, this will allow the lines to be curved, and make for a much smoother transition between cells. 
# What I mean is instead of the grid looking like this:
#    __ __ __
#   |        |
#   |        |
#   |__ __ __|
#
# it will instead look like a circle, by rounding off the corners. This theory then extends to any shape that the initial marching 
# cubes creates, so that any blocky, pointy shape can be transformed into a smooth surface.
#
#
# 2. Different weights for the corners.
# Currently the corners are either a 1 or a 0, but in the future I want to extend this so that the corners can be any decimal value. 
# The "Marching Squares" algorithm states that once the corner values have been set, a passover filter is applied, with a threshold value, 
# and anything below that is set to a 0, which is simple enough to implement. 
# But then after that, the values of the corners corresponds to how much influence they each have on the end positions of the lines. 
# For example:
# 
# If the corner values for a cell are as follows (after filter):
# 
# +------+------+------+
# |0                  0|
# |                    |
# |                    |
# |                    |
# |                    |
# |                    |
# +------+------+------+
# 
# Okay, I don't understand this at all. I am going to watch some content on YouTube about it to try and better understand it.


from random import randint

import pygame
canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

gridSize = (4, 4)
cellW, cellH = (canvasW / gridSize[0]), (canvasH / gridSize[1])

# Starting from the bottom left and working counter-clockwise:
contourLinesVertexPositions = [
    (0.5, 1),
    (1, 0.5),
    (0.5, 0),
    (0, 0.5)
]

tableIndexes = [
    [], #               0
    [(0, 3)], #         1
    [(0, 1)], #         2
    [(1, 3)], #         3
    [(1, 2)], #         4
    [(0, 1), (2, 3)], # 5
    [(0, 2)], #         6
    [(2, 3)], #         7
    [(2, 3)], #         8
    [(0, 2)], #         9
    [(1, 2), (3, 0)], # 10
    [(1, 2)], #         11
    [(1, 3)], #         12
    [(0, 1)], #         13
    [(3, 0)], #         14
    [] #                15
]

class Cell:
    def __init__(self, col_, row_, tableIndex_):
        self.col, self.row = col_, row_
        self.tableIndex = tableIndex_

        self.left = self.col * cellW
        self.right = (self.col + 1) * cellW

        self.top = self.row * cellH
        self.bottom = (self.row + 1) * cellH
    
    def render(self):

        pygame.draw.polygon(
            canvas, (150, 150, 150),
            [
                (self.left, self.top),
                (self.right, self.top),
                (self.right, self.bottom),
                (self.left, self.bottom)
            ], 1
        )

        for line in tableIndexes[self.tableIndex]:
            startPosition = contourLinesVertexPositions[ line[0] ]
            endPosition = contourLinesVertexPositions[ line[1] ]
            startX = self.left + (startPosition[0] * cellW)
            startY = self.top + (startPosition[1] * cellH)
            endX = self.left + (endPosition[0] * cellW)
            endY = self.top + (endPosition[1] * cellH)
            pygame.draw.line(
                canvas, (0, 0, 0),
                (startX, startY),
                (endX, endY),
                1
            )

ind = [
    13, 12, 12, 14, 
    4, 1, 0, 6, 
    2, 8, 0, 6, 
    11, 3, 3, 7
]

grid = []
for r in range(gridSize[1]):
    for c in range(gridSize[0]):
        grid.append(Cell(c, r, ind[c + (r * gridSize[0])]))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # if event.type == pygame.MOUSEBUTTONUP:
        #     index = (index + 1) % 16
            # print(index)
    
    canvas.fill((255, 255, 255))

    for C in grid:
        C.render()

    pygame.display.flip()