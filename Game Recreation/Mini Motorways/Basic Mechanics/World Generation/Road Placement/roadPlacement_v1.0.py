
from math import cos, sin, pi, atan2
import pygame

cellSize = 175
columnCount, rowCount = 4, 3

canvasW, canvasH = columnCount * cellSize, rowCount * cellSize
canvas = pygame.display.set_mode((canvasW, canvasH))

roadThickness = int(cellSize / 16)


class Vector:
    def __init__(self, x_, y_):
        self.x, self.y = x_, y_
    
    @staticmethod
    def fromAngle(angle_, mag_ = 1.0):
        return Vector(cos(angle_) * mag_, sin(angle_) * mag_)
    
    def toInt(self):
        return int(self.x), int(self.y)

class Cell:
    def __init__(self, c_, r_, startingEdge_=0, roadLayout_='d'):
        self.col, self.row = c_, r_
        self.index = c_ + (r_ * columnCount)
        self.topLeft = Vector(c_ * cellSize, r_ * cellSize)
        self.bottomRight = Vector((c_+1) * cellSize, (r_+1) * cellSize)

        # self.roadLayout = roadLayout_

        self.startingEdge = startingEdge_
        self.endingEdge = startingEdge_
        
        if roadLayout_ == 'l': # Left Turn
            self.endingEdge = (self.startingEdge + 1) % 4
        elif roadLayout_ == 'r': # Right Turn
            self.endingEdge = (self.startingEdge - 1) % 4
        elif roadLayout_ == 's': # Straight Over
            self.endingEdge = (self.startingEdge + 2) % 4
            

        # How much offset from the centre line is the road:
        self.middleOffsetMultiplier = 0.0
        # How much offset from the edge of the cell. This is just used to discern between each cell:
        self.edgeOffsetMultiplier = 0.0 # Set to 0.0 for final
        self.roadStartPoints = [
            Vector((c_ + 0.5 + self.middleOffsetMultiplier) * cellSize, (r_ + self.edgeOffsetMultiplier) * cellSize),
            Vector((c_ + (1.0 - self.edgeOffsetMultiplier)) * cellSize, (r_ + 0.5 + self.middleOffsetMultiplier) * cellSize),
            Vector((c_ + 0.5 - self.middleOffsetMultiplier) * cellSize, (r_ + (1.0 - self.edgeOffsetMultiplier)) * cellSize),
            Vector((c_ + self.edgeOffsetMultiplier) * cellSize, (r_ + 0.5 - self.middleOffsetMultiplier) * cellSize)
        ]
        self.roadEndPoints = [
            Vector((c_ + 0.5 - self.middleOffsetMultiplier) * cellSize, (r_ + self.edgeOffsetMultiplier) * cellSize),
            Vector((c_ + (1.0 - self.edgeOffsetMultiplier)) * cellSize, (r_ + 0.5 - self.middleOffsetMultiplier) * cellSize),
            Vector((c_ + 0.5 + self.middleOffsetMultiplier) * cellSize, (r_ + (1.0 - self.edgeOffsetMultiplier)) * cellSize),
            Vector((c_ + self.edgeOffsetMultiplier) * cellSize, (r_ + 0.5 + self.middleOffsetMultiplier) * cellSize)
        ]

        dx = self.roadStartPoints[0].x - self.bottomRight.x
        dy = self.roadStartPoints[0].y - self.topLeft.y
        self.roadArcRadius = ((dx**2) + (dy**2)) ** 0.5

        
    
    def render(self, roadColour=(50, 50, 50), showBounds=True, showRoadEnds=True):
        x1, y1 = self.topLeft.toInt()
        x2, y2 = self.bottomRight.toInt()
        
        cellRect = pygame.Rect(x1, y1, cellSize, cellSize)

        # Draw the bounding box of the cell:
        if showBounds: pygame.draw.rect(canvas, (0,0,0), cellRect, 2) #pygame.draw.polygon(canvas, (150, 150, 150), [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 1)

        if showRoadEnds:
            for s_pt in self.roadStartPoints:
                pygame.draw.circle(canvas, (0, 200, 0), s_pt.toInt(), 4, 0)
            for e_pt in self.roadEndPoints:
                pygame.draw.circle(canvas, (200, 0, 0), e_pt.toInt(), 4, 0)
        
        
        # If the "startingEdge" and "endingEdge" are the same, it is a dead-end (no road):
        if self.startingEdge - self.endingEdge == 0: return        

        roadStartPoint = self.roadStartPoints[self.startingEdge]
        if showRoadEnds: pygame.draw.circle(canvas, roadColour, roadStartPoint.toInt(), roadThickness, 1)

        roadEndPoint = self.roadEndPoints[self.endingEdge]
        if showRoadEnds: pygame.draw.circle(canvas, roadColour, roadEndPoint.toInt(), roadThickness, 2)

        dx = roadEndPoint.x - roadStartPoint.x
        dy = roadEndPoint.y - roadStartPoint.y
        angle = atan2(dy, dx)

        pygame.draw.polygon(
            canvas, 
            roadColour, 
            [
                (
                    roadStartPoint.x + (cos(angle - pi/2) * roadThickness * 0.5),
                    roadStartPoint.y + (sin(angle - pi/2) * roadThickness * 0.5)
                ),
                (
                    roadEndPoint.x + (cos(angle - pi/2) * roadThickness * 0.5),
                    roadEndPoint.y + (sin(angle - pi/2) * roadThickness * 0.5)
                ),
                (
                    roadEndPoint.x + (cos(angle + pi/2) * roadThickness * 0.5),
                    roadEndPoint.y + (sin(angle + pi/2) * roadThickness * 0.5)
                ),
                (
                    roadStartPoint.x + (cos(angle + pi/2) * roadThickness * 0.5),
                    roadStartPoint.y + (sin(angle + pi/2) * roadThickness * 0.5)
                )
            ], 
            0
        )

        # pygame.draw.line(canvas, (0, 200, 0), roadStartPoint.toInt(), 
        # (
        #     roadStartPoint.toInt()[0] + int(cos(angle) * 50),
        #     roadStartPoint.toInt()[1] + int(sin(angle) * 50)
        # ), 
        # 1)

        if showBounds:
            pygame.draw.line(canvas, (150,150,150), (x1+int(cellSize/2), y1), (x1+int(cellSize/2), y1+cellSize), 1)
            pygame.draw.line(canvas, (150,150,150), (x1, y1+int(cellSize/2)), (x1+cellSize, y1+int(cellSize/2)), 1)
        
        return
        # --->
        # This return statement is just here because I wanted to make sure the basic, straight lines were 
        # drawing correctly. 
        # On my next session, I want to remove this return statement and get some nice arcs drawn etc. 
        # <---

        # if self.roadLayout == "": 
        
        
        # The radius of the road arc:
        # self.roadArcRadius = cellSize * (0.5 - self.middleOffsetMultiplier)
        
        arcLeft = (x1 + cellSize) - self.roadArcRadius
        arcTop = y1 - self.roadArcRadius
        arcRect = pygame.Rect(arcLeft, arcTop, self.roadArcRadius*2, self.roadArcRadius*2)

        # Draw the mid-lines of the cell:
        # pygame.draw.line(canvas, (150,150,150), (x1+int(cellSize/2), y1), (x1+int(cellSize/2), y1+cellSize), 1)
        # pygame.draw.line(canvas, (150,150,150), (x1, y1+int(cellSize/2)), (x1+cellSize, y1+int(cellSize/2)), 1)

        # Start and end angle:
        startAngle = pi
        endAngle = pi * -0.5
        
        # Draw the arc:
        pygame.draw.arc(canvas, (50, 50, 50), arcRect, startAngle, endAngle, self.roadThickness)



gameGrid = []
for r in range(rowCount):
    row = []
    for c in range(columnCount):
        row.append(Cell(c, r))
    gameGrid.append(row)

gameGrid[0][0] = Cell(0, 0, 2, 'r')
gameGrid[0][1] = Cell(1, 0, 3, 's')
gameGrid[0][2] = Cell(2, 0, 3, 's')
gameGrid[0][3] = Cell(3, 0, 3, 'r')

gameGrid[1][3] = Cell(3, 1, 0, 'r')
gameGrid[1][2] = Cell(2, 1, 1, 'l')

gameGrid[2][2] = Cell(2, 2, 0, 'r')
gameGrid[2][1] = Cell(1, 2, 1, 's')
gameGrid[2][0] = Cell(0, 2, 1, 'r')

gameGrid[1][0] = Cell(0, 1, 2, 's')


showGrid = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            showGrid ^= True
        
    canvas.fill((255, 255, 255))

    for row in gameGrid:
        for C in row:
            C.render(showBounds=showGrid, showRoadEnds=False)
    
    pygame.display.flip()
