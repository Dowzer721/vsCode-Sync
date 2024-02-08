
import pygame
from random import randint

canvasW, canvasH = 600, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

def rf(min_=0.0, max_=1.0, dp_=3):
    _rng = max_ - min_
    _pct = randint(0, 10 ** dp_) / (10 ** dp_)
    return round(min_ + (_rng * _pct), dp_)

def calculatePathPoints(PathAnchors, PathPointCount):
    def interp(start, end, T):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        x = start[0] + (T * dx / PathPointCount)
        y = start[1] + (T * dy / PathPointCount)
        return (x, y)
    
    def calculatePointAt_T(Anchors, T):
        AnchorCount = len(Anchors)
        if AnchorCount == 1: return Anchors
        newAnchors = []
        for c in range(AnchorCount-1):
            n = c + 1
            newAnchors.append(interp(Anchors[c], Anchors[n], T))
        return calculatePointAt_T(newAnchors, T)

    
    pathMidPoints = []
    for T in range(PathPointCount):
        pathMidPoints.append(calculatePointAt_T(PathAnchors, T)[0])

    pathEdgePoints = [[], []] # [[Left Points], [Right Points]]
    for c in range(PathPointCount-1):
        n = c + 1
        (x1, y1), (x2, y2) = pathMidPoints[c], pathMidPoints[n]
        dx = x2 - x1
        dy = y2 - y1
        pathEdgePoints[0].append((x1 + dy, y1 - dx))
        pathEdgePoints[1].append((x1 - dy, y1 + dx))
    
    return pathEdgePoints

anc = [(canvasW * 0.1, canvasH * 0.1), (canvasW * 0.5, canvasH * 0.9), (canvasW * 0.9, canvasH * 0.1)]
path = calculatePathPoints(anc, 10)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    canvas.fill((255, 255, 255))

    for Ax,Ay in anc:
        pygame.draw.circle(canvas, (0,0,0), (int(Ax), int(Ay)), 8, 0)
    
    for PathLeftX, PathLeftY in path[0]:
        pygame.draw.circle(canvas, (200,200,200), (int(PathLeftX), int(PathLeftY)), 4, 0)
    for PathRightX, PathRightY in path[1]:
        pygame.draw.circle(canvas, (200,200,200), (int(PathRightX), int(PathRightY)), 4, 0)
    
    pygame.display.update()
