
from math import pi, cos, sin
import pygame 

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

shapeCornerCount = 6

minX, minY, maxX, maxY = 1, 1, 0, 0
for i in range(shapeCornerCount):
    angle = -(pi/shapeCornerCount) + (i * 2*pi / shapeCornerCount)
    x = cos(angle)
    y = sin(angle)
    minX = min(minX, x)
    maxX = max(maxX, x)
    minY = min(minY, y)
    maxY = max(maxY, y)
# print(f"minX:{minX}, maxX:{maxX}, \nminY:{minY}, maxY:{maxY}")

mx, my = canvasW / 2, canvasH / 2
gameEdgeSize = max((maxX - minX), (maxY - minY)) * min(canvasW, canvasH) * 0.45
gameEdgeCorners = [
    (mx - (gameEdgeSize/2), my - (gameEdgeSize/2)),
    (mx + (gameEdgeSize/2), my - (gameEdgeSize/2)),
    (mx + (gameEdgeSize/2), my + (gameEdgeSize/2)),
    (mx - (gameEdgeSize/2), my + (gameEdgeSize/2))
]
# print(gameEdgeSize)
gameEdgeShapeCount = 10
# shapeEdgeLength = 2 * pi * (gameEdgeSize * 0.4) / (shapeCornerCount * gameEdgeShapeCount)
shapeEdgeLength = int(.45 * gameEdgeSize / gameEdgeShapeCount)  #30

class Shape:
    def __init__(self, position_):
        self.position = position_
        self.visited = False
        self.corners = []
        self.edgesVisible = [True for _ in range(shapeCornerCount)]
        for i in range(shapeCornerCount):
            angle = -(pi/shapeCornerCount) + (i * 2*pi / shapeCornerCount)
            x = self.position[0] + (cos(angle) * shapeEdgeLength)
            y = self.position[1] + (sin(angle) * shapeEdgeLength)
            self.corners.append((x,y))
    def pointInside(self, point):
        xInside = (point[0] > (self.position[0] + minX)) and (point[0] < (self.position[0] + maxX))
        yInside = (point[1] > (self.position[1] + minY)) and (point[1] < (self.position[1] + maxY))
        return xInside and yInside

    def render(self):
        for c in range(shapeCornerCount):
            if self.edgesVisible[c] == False: continue

            n = (c + 1) % shapeCornerCount
            pygame.draw.line(canvas, (0,0,0), self.corners[c], self.corners[n], 1)
shapes = [Shape((mx-13, my-19))]


def placeShapesAround(shapePosition_, shapeCorners_):
    newShapePositions = []
    for c in range(shapeCornerCount):
        n = (c + 1) % shapeCornerCount
        x1, y1 = shapeCorners_[c]
        x2, y2 = shapeCorners_[n]
        midX = (x1 + x2) / 2
        midY = (y1 + y2) / 2
        dx = shapePosition_[0] - midX
        dy = shapePosition_[1] - midY
        newShapePositions.append( (shapePosition_[0] + (dx * 2),shapePosition_[1] + (dy * 2)) )
    return newShapePositions


spacingMultiplier = 0.0

# for j in range(1, 20):
j = 1
while True:

    if (j-1) >= len(shapes): break
    
    newShapePositions = placeShapesAround(shapes[j-1].position, shapes[j-1].corners)
    for pos in newShapePositions:
        validPlacementPosition = True
        
        #self.position[0] + (cos(angle) * shapeEdgeLength)
        left  = pos[0] + (minX * shapeEdgeLength)
        right = pos[0] + (maxX * shapeEdgeLength)
        top   = pos[1] + (minY * shapeEdgeLength)
        bottom= pos[1] + (maxY * shapeEdgeLength)

        # xInsideGameArea = (pos[0] > gameEdgeCorners[0][0]) and (pos[0] < gameEdgeCorners[1][0])
        # yInsideGameArea = (pos[1] > gameEdgeCorners[0][1]) and (pos[1] < gameEdgeCorners[3][1])
        xInsideGameArea = (left > gameEdgeCorners[0][0]) and (right < gameEdgeCorners[1][0])
        yInsideGameArea = (top  > gameEdgeCorners[0][1]) and (bottom< gameEdgeCorners[3][1])

        if not (xInsideGameArea and yInsideGameArea): continue#validPlacementPosition = False

        for S in shapes:
            if S.pointInside(pos): 
                validPlacementPosition = False
            
            if validPlacementPosition == False: break
        
        if validPlacementPosition:
            shapes.append(Shape((pos)))
    j += 1

print(len(shapes))

# for c in range(shapeCornerCount):
#     n = (c + 1) % shapeCornerCount
#     x1, y1 = shapes[0].corners[c]
#     x2, y2 = shapes[0].corners[n]
#     midX = (x1 + x2) / 2
#     midY = (y1 + y2) / 2

#     dx = shapes[0].position[0] - midX
#     dy = shapes[0].position[1] - midY

#     for j in range(1, shapeCornerCount + 1):
#         x = shapes[0].position[0] + (dx * 2 * j) #+ int(dx * 2 * j * spacingMultiplier)
#         y = shapes[0].position[1] + (dy * 2 * j) #+ int(dy * 2 * j * spacingMultiplier)
#         shapes.append( Shape((x,y)) )


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    canvas.fill((255,255,255))

    pygame.draw.polygon(canvas, (0,0,0), gameEdgeCorners, 1)

    for S in shapes:
        S.render()

    pygame.display.update()