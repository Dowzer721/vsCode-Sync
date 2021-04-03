
import math
import pygame
import random

pygame.display.init()

def generateMaze(cols = 6, rows = 8):
    
    def index(c, r):
        return c + (r * cols)
    def colRowFromIndex(i):
        col = i % cols
        row = math.floor(i / cols)
        return (col, row)

    goalIndices = [
        index(math.floor(cols/2) - 1,   math.floor(rows/2) - 1),
        index(math.floor(cols/2),       math.floor(rows/2) - 1),
        index(math.floor(cols/2),       math.floor(rows/2)    ),
        index(math.floor(cols/2) - 1,   math.floor(rows/2)    )
    ]

    class Cell:
        def __init__(self, c_, r_):
            self.col = c_
            self.row = r_
            self.index = index(c_, r_)

            self.walls = [1 for _ in range(4)]
            x = (1 / cols) * c_
            y = (1 / rows) * r_
            w = (1 / cols)
            h = (1 / rows)
            self.corners = [
                (x, y),
                (x + w, y),
                (x + w, y + h),
                (x, y + h)
            ]
            
            self.isGoal = self.index in goalIndices
            self.visited = self.isGoal # (self.isGoal == 1)
        
        def displayCell(self, pyGameScreen, screenW, screenH, colour=(0, 0, 0), thickness=1): #, isCurrent=False):
            
            visitedColour = (0, 200, 0)
            x = int(self.corners[0][0] * screenW) + 5
            y = int(self.corners[0][1] * screenH) + 5
            if (self.visited):
                visitedColour = (200, 0, 0)
            pygame.draw.circle(
                pyGameScreen, visitedColour,
                (x, y),
                5, 0
            )

            if self.isGoal:
                x = int(self.corners[1][0] * screenW) - 5
                pygame.draw.circle(
                    pyGameScreen, (0, 0, 200),
                    (x, y),
                    5, 0
                )
            
            # if isCurrent:
            #     x = int( (self.corners[0][0] + self.corners[1][0] /2) )
            #     y = int( (self.corners[0][1] + self.corners[2][1] /2) )
            #     pygame.draw.circle(
            #         screen, (100, 100, 100),
            #         (x, y), 5, 0
            #     )
            
            for w in range(4):
                n = (w + 1) % 4
                start = (
                    int(self.corners[w][0] * screenW),
                    int(self.corners[w][1] * screenH)
                )
                end = (
                    int(self.corners[n][0] * screenW),
                    int(self.corners[n][1] * screenH)
                )
                if (self.walls[w]):
                    pygame.draw.line(
                        pyGameScreen, colour,
                        start, end,
                        thickness
                    )

    Grid = [
        [
            Cell(c, r) for c in range(cols)
        ] for r in range(rows)
    ]

    def getNeighbours(col, row):
        neighbours = [
            Grid[row-1][col] if row > 0 else -1,
            Grid[row][col+1] if col < cols - 1 else -1,
            Grid[row+1][col] if row < rows - 1 else -1,
            Grid[row][col-1] if col > 0 else -1
        ]
        return neighbours
    
    
    mazeGenerationStack = []
    # Push val to stack: mazeGenerationStack.append(val)
    # Peak end of stack: mazeGenerationStack[-1]
    # Pop end of stack:  mazeGenerationStack.pop(-1)
        
    
    # Add the starting index to the stack:
    mazeGenerationStack.append( goalIndices[random.randint(0, 3)] )

    mazeGenerated = True
    while (mazeGenerated == False):
        
        # Find current neighbours:
        currentLocation = colRowFromIndex(mazeGenerationStack[-1])
        currentNeighbours = getNeighbours(currentLocation[0], currentLocation[1])

        # Remove neighbours which have been visited:
        for n in range(4):
            if currentNeighbours[n].visited == True:
                currentNeighbours[n] = -1
        
        # Choose a random neighbour to move to:
        start_i = random.randint(0, 3)
        end_i = start_i + 4
        #next = currentNeighbours[0] # <----------- FINISHED HERE (THIS NEEDS TO BE OPTIMISED).
        for i in range(start_i, end_i):
            j = i % 4
            if currentNeighbours[j] != -1:
                next = currentNeighbours[j]
                break
    
    


    return Grid

# screenW = 500
# screenH = 500
# screen = pygame.display.set_mode((screenW, screenH))

# cols = 6
# rows = 8
# # gridW = (screenW / cols)
# # gridH = (screenH / rows)

# Grid = generateMaze() # cols, rows)
# # print(maze)
# # input()

# cols = len(Grid[0])
# rows = len(Grid)

# while(True):
#     screen.fill((255, 255, 255))

#     # for C in Grid:
#         # displayCell(self, scaleW, scaleH, colour=(0, 0, 0), thickness=1.0)
#         # C.displayCell(screenW, screenH, (255, 0, 0), 1)

#     for r in range(rows):
#         for c in range(cols):
#             Grid[r][c].displayCell(screenW, screenH)

#     pygame.display.flip()