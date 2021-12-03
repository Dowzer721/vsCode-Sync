
import pygame
# pygame.init()

# +---+---+---+---+---+---+---+
# |                       | S |
# +   +---+---+   +---+---+   +
# |               |       |   |
# +   +---+---+   +   +---+   +
# |   |   |     G |   |   |   |
# +   +---+---+   +   +   +   +
# |                           |
# +   +   +---+---+---+---+---+
# |                           |
# +---+---+---+---+---+---+---+
#
#     1
#   +---+
# 8 |   | 2
#   +---+
#     4

grid = [
    [9, 5, 5, 1, 5, 7, 11],
    [8, 5, 5, 2, 9, 7, 10],
    [10, 15, 13, 2, 10, 11, 10],
    [8, 1, 5, 4, 4, 4, 6],
    [12, 4, 5, 5, 5, 5, 7]
]

rowCount, colCount = len(grid), len(grid[0])
# print(f"Rows: {rowCount}, Columns: {colCount}")

canvasW = 500
canvasH = int(canvasW * (rowCount / colCount))
canvas = pygame.display.set_mode((canvasW, canvasH))
cellW, cellH = int(canvasW / colCount), int(canvasH / rowCount)

def valToBinary(val):
    bin = [0, 0, 0, 0]
    for i in range(3, -1, -1): 
        # i -> 3, 2, 1, 0
        if val >= (2 ** i):
            val -= (2 ** i)
            bin[i] = 1
    return bin

gridCells = []
class Cell:
    def __init__(self, col_, row_, walls_):
        self.col = col_
        self.row = row_
        self.walls = walls_

        self.floodFillValue = 0

        x1 = cellW * self.col
        y1 = cellH * self.row
        x2 = cellW * (self.col + 1)
        y2 = cellH * (self.row + 1)

        self.corners = [
            (x1, y1), (x2, y1),
            (x2, y2), (x1, y2)
        ]
    
    def getNeighbours(self):
        neighbours = [
            (self.row - 1, self.col),
            (self.row, self.col + 1),
            (self.row + 1, self.col),
            (self.row, self.col - 1)
        ]

        # Remove neighbours outside of borders:
        if self.row == 0: neighbours[0] = None
        if self.col == colCount - 1: neighbours[1] = None
        if self.row == rowCount - 1: neighbours[2] = None
        if self.col == 0: neighbours[3] = None

        # Remove neighbours blocked by walls:
        for w in range(4):
            if self.walls[w]: neighbours[w] = None
        
        # Remove neighbours which already have a flood fill value:
        for n in range(4):
            if neighbours[n] == None: continue
            r, c = neighbours[n]
            if gridCells[r][c].floodFillValue > 0: neighbours[n] = None
        

        return neighbours

    
    def render(self):
        
        for i in range(4):
            if not self.walls[i]: continue

            x1, y1 = self.corners[i]
            x2, y2 = self.corners[(i+1) % 4]

            pygame.draw.line(
                canvas, (0, 0, 0),
                (x1, y1), (x2, y2),
                1
            )


for row in range(rowCount):
    rowList = []
    for col in range(colCount):
        rowList.append( Cell(col, row, valToBinary(grid[row][col]) ) )
    gridCells.append(rowList)

# print(gridCells[0][colCount-1].getNeighbours())

# Flood Fill:
for i in range(0, colCount * rowCount):
    

running = True
while running:
    canvas.fill((200, 200, 200))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    for row in gridCells:
        for c in row:
            c.render()

    pygame.display.flip()


# print("PROGRAM COMPLETE")