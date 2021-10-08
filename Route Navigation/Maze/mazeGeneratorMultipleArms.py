
import pygame
from random import randint

def generate(
    colCount, rowCount, mazeStart, mazeEnd, armCount = 2, 
    renderLocation = -1, debugPrint = False, progressPrint = False, saveToFile = True):
    """
    colCount:       The number of columns for the maze (c >= 6)

    rowCount:       The number of rows for the maze (r >= 8)

    mazeStart:      List [x, y] of maze starting point (defaults to [0, 0])
    
    mazeEnd:        List [x, y] of maze ending point (defaults to [c-1, r-1])
    
    armCount:       The number of arms to spread when generating the maze (defaults to 2)
    
    renderLocation: If drawing with pygame, the canvas you want to draw to

    debugPrint:     Whether or not to print to the console during execution (helpful for larger mazes)

    progressPrint:  Whether or not to print to the console the progression of the generation

    saveToFile:     Whether or not to save to the "mazeData.txt" file in the folder
    """

    colCount = max(colCount, 6)
    rowCount = max(rowCount, 8)
    
    mazeStart[0] = max(0, min(mazeStart[0], colCount-1))
    mazeStart[1] = max(0, min(mazeStart[1], rowCount-1))

    mazeEnd[0] = max(0, min(mazeEnd[0], colCount-1))
    mazeEnd[1] = max(0, min(mazeEnd[1], rowCount-1))

    # mazeEnd[0] = min(mazeEnd[0], colCount)
    # mazeEnd[1] = min(mazeEnd[1], rowCount)

    armCount = max(armCount, 1)
    
    def index(col, row):
        return col + (row * colCount)
    
    if renderLocation != -1:
        canvasW, canvasH = renderLocation.get_size()

        gridW = canvasW / colCount
        gridH = canvasH / rowCount
    
    mazeSize = colCount * rowCount

    Grid = []
    class Cell:
        def __init__(self, col_, row_):
            self.col = col_
            self.row = row_
            self.index = index(col_, row_)

            self.walls = [1, 1, 1, 1]
            self.visited = False

            if renderLocation != -1:
                x1 = self.col * gridW
                y1 = self.row * gridH
                x2 = (self.col + 1) * gridW
                y2 = (self.row + 1) * gridH

                cornerAdd = 0#int(gridW * 0.1)

                self.corners = [
                    (x1 + cornerAdd, y1 + cornerAdd),
                    (x2 - cornerAdd, y1 + cornerAdd),
                    (x2 - cornerAdd, y2 - cornerAdd),
                    (x1 + cornerAdd, y2 - cornerAdd)
                ]
        
        def getNeighbours(self, removeBorders=True, removeVisited=True):
            # Neighbours ignoring borders and visitations:
            neighbours = [
                index(self.col, self.row - 1),
                index(self.col + 1, self.row),
                index(self.col, self.row + 1),
                index(self.col - 1, self.row)
            ]

            if removeBorders:
                # Remove neighbours outside borders:
                if self.row == 0: neighbours[0] = -1
                if self.col == colCount-1: neighbours[1] = -1
                if self.row == rowCount-1: neighbours[2] = -1
                if self.col == 0: neighbours[3] = -1

            if removeVisited:
                # Remove neighbours which have been visited:
                for n in range(4):
                    if neighbours[n] == -1: continue
                    
                    if Grid[neighbours[n]].visited == True:
                        neighbours[n] = -1
            
            return neighbours


        
        def render(self):
            """
            This method should only be called if a renderLocation was provided to the "generate()" function. 
            """
            
            for w in range(4):
                # If wall isn't there, skip:
                if self.walls[w] == 0: continue

                n = (w + 1) % 4
                
                start = ( int(self.corners[w][0]), int(self.corners[w][1]) )
                end = ( int(self.corners[n][0]), int(self.corners[n][1]) )
                
                pygame.draw.line(
                    renderLocation, (0, 0, 0),
                    start, end, 1
                )
            
            isStart = (self.col == mazeStart[0] and self.row == mazeStart[1])
            isEnd = (self.col == mazeEnd[0] and self.row == mazeEnd[1])

            if isStart or isEnd:

                x = int((self.col + 0.5) * gridW)
                y = int((self.row + 0.5) * gridH)
                r = int( min(gridW * 0.2, gridH * 0.2) )
                col = (0, 200, 0) if isStart else (200, 0, 0)
                pygame.draw.circle(
                    renderLocation, col,
                    (x, y), r, 0
                )
    
    for row in range(rowCount):
        for col in range(colCount):
            Grid.append(Cell(col, row))
    

    armIndexes = [
        index(mazeStart[0], mazeStart[1])
    ]

    for _ in range(armCount-2):
        armIndexes.append(randint(4, mazeSize-5))
    
    if armCount > 1:
        armIndexes.append(index(colCount-1, rowCount-1))

    if debugPrint:
        print(
            f"c:{colCount}, r:{rowCount}, sz:{mazeSize} \n",
            f"start:{mazeStart}, end:{mazeEnd} \n",
            f"armCount:{armCount}, arms:{armIndexes}"
        )

    for armInd in armIndexes:
        Grid[armInd].visited = True
    
    armStacks = []
    armStacksNoPop = []
    for arm in armIndexes:
        armStacks.append([arm])
        armStacksNoPop.append([arm])


    # print(armStacks)

    permissionToMove = False

    visitedCount = 0
    while visitedCount != mazeSize-1:
        visitedCount = sum([int(Grid[i].visited) for i in range(mazeSize)])
        # if visitedCount == (mazeSize-1):
        #     break

        # permissionToMoveCount = 0

        # # Gather permission to move from all arms
        # for arm in range(armCount):
        #     currentIndex = armStacks[arm][-1]
        #     currentNeighbours = Grid[currentIndex].getNeighbours()
        #     if currentNeighbours.count(-1) == 4:
        #         permissionToMoveCount += 1
        
        # permissionToMove = (permissionToMoveCount == 4)
        
        for arm in range(armCount):
            if len(armStacks[arm]) == 0: continue

            currentIndex = armStacks[arm][-1]

            currentNeighbours = Grid[currentIndex].getNeighbours()

            # # If there are no neighbours, remove walls to adjoining neighbours, 
            # # then move back one position in the arm stack:
            if currentNeighbours.count(-1) == 4:
                neighboursIgnoringVisited = Grid[currentIndex].getNeighbours(removeVisited=False)
                for neighbourDirection in range(4):
                    for otherArm in range(armCount):
                        if otherArm == arm: continue

                        neighbourIndex = neighboursIgnoringVisited[neighbourDirection]
                        if neighbourIndex in armStacksNoPop[otherArm]:
                            Grid[currentIndex].walls[neighbourDirection] = 0
                            Grid[neighbourIndex].walls[(neighbourDirection+2)%4] = 0
                
                currentIndex = armStacks[arm].pop(-1)

                continue

            # # If there are no neighbours, step backwards one position in the stack:
            # if currentNeighbours.count(-1) == 4:
            #     currentIndex = armStacks[arm].pop(-1)
            #     continue

            # If there are no neighbours:
            #   Check if any of the neighbours are within another arm stack. 
            #   If so, remove the walls between them.
            # Then step back one position in the arm stack:
            
            # if currentNeighbours.count(-1) == 4:
                # neighboursIgnoringVisited = Grid[currentIndex].getNeighbours(removeVisited=False)
                # for neighbourDirection in range(4):
                # # for neighbourIndex in neighboursIgnoringVisited:
                #     for otherArm in range(armCount):
                #         if otherArm == arm: continue

                #         neighbourIndex = neighboursIgnoringVisited[neighbourDirection]
                #         if neighbourIndex in armStacks[otherArm]:
                #             Grid[currentIndex].walls[neighbourDirection] = 0
                #             Grid[neighbourIndex].walls[(neighbourDirection+2)%4] = 0
                
                # if permissionToMove:
                #     currentIndex = armStacks[arm].pop(-1)
                    
                # continue
                            

                
            # Choose a random valid direction:
            randomDirection = randint(0, 3)
            for i in range(4):
                if currentNeighbours[(randomDirection + i) % 4] != -1:
                    randomDirection = (randomDirection + i) % 4
                    break
            
            # Remove the walls between the current and the neighbour. 
            # This requires removing both the current cell wall and the neighbour adjoining wall too:
            Grid[currentIndex].walls[randomDirection] = 0
            neighbourInDirection = currentNeighbours[randomDirection]
            Grid[neighbourInDirection].walls[(randomDirection + 2) % 4] = 0


            # Move current index to neighbour index:
            currentIndex = neighbourInDirection

            # Set current index to visited:
            Grid[currentIndex].visited = True

            # Push the current index to the arm stack:
            armStacks[arm].append(currentIndex)
            armStacksNoPop[arm].append(currentIndex)

        if debugPrint:
            pct = (visitedCount * 100) / mazeSize
            print(f"{round(pct, 2)}%")
    
    if debugPrint:
        print(armStacksNoPop)
    
    if saveToFile:
        gridStorageFile = open("C:/Users/Luke/Documents/Learning Python/Route Navigation/Maze/mazeData.txt", 'w')
        for cell in Grid:
            wallsInteger = sum([
                (2 ** i) * int(cell.walls[i])
                for i in range(4)
            ])
            if cell.index < mazeSize-1:
                gridStorageFile.write(str(wallsInteger) + ', ')
            else:
                gridStorageFile.write(str(wallsInteger) + '.')
        
        gridStorageFile.write(
            f"{colCount}x{rowCount}" +
            f"[{mazeStart[0]},{mazeStart[1]}][{mazeEnd[0]},{mazeEnd[1]}]"
        )
        gridStorageFile.close()

    return Grid



# col, row = 6, 8
# canvasW = 500
# canvasH = int(canvasW * (row/col))
# canvas = pygame.display.set_mode((canvasW, canvasH))

# # maze = generate(col, row, [10, 0], [0, 13], 2, 
# #     debugPrint=False, 
# #     returnMaze=True, 
# #     saveToFile=True
# # )

# maze = generate(col, row, [0, 0], [col//2, row//2], 
#     armCount=int((col*row)*0.005), 
#     renderLocation=canvas,
#     debugPrint=False, 
#     progressPrint=True, 
#     saveToFile=True
# )

# while True:
#     canvas.fill((255, 255, 255))

#     for cell in maze:
#         cell.render()
    
#     pygame.display.flip()
