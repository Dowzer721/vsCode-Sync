
from math import pi, atan2
import pygame
from random import randint

canvasW, canvasH = 680, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

minX = int(canvasW * 0.1)
maxX = int(canvasW * 0.9)

minY = int(canvasH * 0.1)
maxY = int(canvasH * 0.9)

numberOfPoints = 16
points = [ (randint(minX, maxX), randint(minY, maxY)) for _ in range(numberOfPoints) ]
connected = [True] + [False for _ in range(numberOfPoints-1)]

pointRadius = 6


def findHull(currentPoint, currentAngle):

    connectionOrder = [currentPoint]

    smallest_dAngle = pi * 2
    smallest_dAngle_Index = currentPoint
    closestAngleToOtherPoint = currentAngle

    for otherPointIndex in range(numberOfPoints):
        # Don't check current against itself
        if currentPoint == otherPointIndex: continue

        # Skip already connected points
        if connected[otherPointIndex]: continue

        otherX, otherY = points[otherPointIndex]
        dx = otherX - points[currentPoint][0]
        dy = otherY - points[currentPoint][1]
        angleToOtherPoint = atan2(dy, dx)

        # Difference between currentAngle and angleToOtherPoint
        # NOTE: may need to add 2pi and mod 2pi
        dAngle = abs(angleToOtherPoint - currentAngle)

        # If dAngle is less than smallest dAngle, 
        if dAngle <= smallest_dAngle:
            smallest_dAngle = dAngle
            smallest_dAngle_Index = otherPointIndex
            closestAngleToOtherPoint = angleToOtherPoint

    if smallest_dAngle_Index == connectionOrder[0]: return False
    
    connectionOrder.append(smallest_dAngle_Index)
    connected[smallest_dAngle_Index] = True

    returnValue = findHull(smallest_dAngle_Index, 0.0)

    if returnValue == False:
        return connectionOrder
    
    if isinstance(returnValue, list):
        return returnValue
    
    



    # closestAngle, smallestDifAngle, closestAngleIndex = currentAngle + pi, 2 * pi, currentPoint

    # for otherPointIndex in range(numberOfPoints):
    #     if currentPoint == otherPointIndex: continue

    #     otherPoint = points[otherPointIndex]
    #     dx = otherPoint[0] - points[currentPoint][0]
    #     dy = otherPoint[1] - points[currentPoint][1]
    #     angleToOtherPoint = atan2(dy, dx)

    #     dAngle = closestAngle - angleToOtherPoint
    #     if dAngle <= smallestDifAngle:
    #         smallestDifAngle = dAngle

# Finding the point closest to the top, so that the starting angle can begin at 0.0
minY, pointWithMinY = canvasH, 0
for i in range(numberOfPoints):
    if points[i][1] <= minY:
        minY = points[i][1]
        pointWithMinY = i


connectionOrder = findHull(pointWithMinY, 0.0)



while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
            
    canvas.fill((255, 255, 255))

    for pt in points:
        pygame.draw.circle(canvas, (100,100,100), pt, pointRadius, 1)
    
    # pygame.draw.line(canvas, (0,0,0), points[0], points[1], int(pointRadius/2))

    start = connectionOrder
    end = connectionOrder[1:] + [connectionOrder[0]]

    for s, e in zip(start, end):
        pygame.draw.line(canvas, (0,0,0), points[s], points[e], int(pointRadius/2))
    
    # for c in range(len(connectionOrder)):
    #     n = (c + 1) % len(connectionOrder)

    #     start = points[connectionOrder[c]]
    #     end = points[connectionOrder[n]]

    #     pygame.draw.line(canvas, (0,0,0), start, end, int(pointRadius/2))

        

    pygame.display.flip()