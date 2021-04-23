
from math import pi, atan2, cos, sin
import pygame
from random import randint

screenW, screenH = 600, 500
screen = pygame.display.set_mode((screenW, screenH))
screen.fill((0, 0, 0))

pointCount = 16
points = []
class Point:
    def __init__(self, id_, x_, y_):
        self.id = id_

        self.position = (x_, y_)

        self.connectedPoint = None
    
    def render(self, renderColour=(200, 0, 0), renderRadius=4):
        pygame.draw.circle(
            screen, renderColour,
            self.position, renderRadius,
            0
        )

        if (self.connectedPoint != None):
            pygame.draw.line(
                screen, (0, 0, 0),
                self.position, self.connectedPoint.position,
                1
            )

for i in range(pointCount):
    x = randint(int(screenW*0.1), int(screenW*0.9))
    y = randint(int(screenH*0.1), int(screenH*0.9))
    points.append(Point(i, x, y))

lowestX = screenW
lowestXID = 0
for pt in points:
    if pt.position[0] < lowestX:
        lowestX = pt.position[0]
        lowestXID = pt.id

# points[lowestXID].connectToPoint(points[lowestXID+1%pointCount])

# currentID = lowestXID
# currentAngle = 3 * pi / 2.0

# for _ in range(10):

#     anglesToAllOtherPoints = []
#     #     atan2((points[i].position[1]-points[currentID].position[1]))
#     for i in range(pointCount):
#         if i == currentID: continue

#         dx = points[i].position[0] - points[currentID].position[0]
#         dy = points[i].position[1] - points[currentID].position[1]
#         # dx = points[currentID].position[0] - points[i].position[0]
#         # dy = points[currentID].position[1] - points[i].position[1]
#         angle = atan2(dy, dx)
#         anglesToAllOtherPoints.append(angle)

#     """
#     Next I want to find the difference in angle between "currentAngle" and each of the list angles, 
#     and then whichever difference is lowest is the angle leading to the next point around the convex hull
#     """

#     angleDifferences = [
#         (anglesToAllOtherPoints[i] - currentAngle) 
#         for i in range(pointCount-1)
#     ]

#     minDifference = min(angleDifferences)

#     minDifferenceID = angleDifferences.index(minDifference)

#     # print(anglesToAllOtherPoints)
#     # print(angleDifferences)
#     # print(minDifference)
#     # print(minDifferenceID)

#     x1 = int(points[currentID].position[0])
#     y1 = int(points[currentID].position[1])
#     x2 = int(points[minDifferenceID].position[0])
#     y2 = int(points[minDifferenceID].position[1])
    
#     pygame.draw.line(
#         screen, (0, 0, 0),
#         (x1, y1), (x2, y2),
#         1
#     )

    
    
#     dx = points[minDifferenceID].position[0] - points[currentID].position[0]
#     dy = points[minDifferenceID].position[1] - points[currentID].position[1]
#     # dx = points[currentID].position[0] - points[minDifferenceID].position[0]
#     # dy = points[currentID].position[1] - points[minDifferenceID].position[1]
#     currentAngle = atan2(dy, dx)
#     currentID = minDifferenceID

averageX = int(sum(pt.position[0] for pt in points) / float(pointCount))
averageY = int(sum(pt.position[1] for pt in points) / float(pointCount))

pygame.draw.circle(
    screen, (0, 255, 0),
    (averageX, averageY), 8,
    0
)

vertexList = []
divisionCount = 3
for c in range(divisionCount):
    thetaC = ((2.0 * pi / divisionCount) * c) + (2.0 * pi)
    thetaC %= (2.0 * pi)
    
    n = (c + 1) % divisionCount
    thetaN = ((2.0 * pi / divisionCount) * n) + (2.0 * pi)
    thetaN %= (2.01 * pi)

    pygame.draw.line(
        screen, (0, 0, 200),
        (averageX, averageY), (
            averageX + int(cos(thetaC) * averageX * 0.5), 
            averageY + int(sin(thetaC) * averageY * 0.5)            
        ), 
        1
    )

    maxDist = -1
    maxDistID = 0
    for pt in points:
        dx = pt.position[0] - averageX
        dy = pt.position[1] - averageY
        angle = (atan2(dy, dx) + (2.0 * pi)) % (2.0 * pi)
        
        if angle > thetaC and angle < thetaN:
        
            dist = ((dx**2) + (dy**2)) ** 0.5
            # x2 = averageX + int(cos(angle) * dist)
            # y2 = averageY + int(sin(angle) * dist)
            # pygame.draw.line(
            #     screen, (150, 150, 150),
            #     (averageX, averageY),
            #     (x2, y2), 1
            # )
            # break

            if dist > maxDist:
                maxDist = dist
                maxDistID = pt.id
    
    # pygame.draw.line(
    #     screen, (150, 150, 150),
    #     (averageX, averageY), (points[maxDistID].position[0], points[maxDistID].position[1]),
    #     1
    # )

    vertexList.append(points[maxDistID])

for c in range(len(vertexList)):
    n = (c + 1) % len(vertexList)
    pygame.draw.line(
        screen, (150, 150, 0),
        points[c].position,
        points[n].position,
        1
    )


# vertexCount = 64
# vertexList = []
# for c in range(vertexCount):
#     n = (c + 1) % vertexCount
#     thetaC = (2.0 * pi / vertexCount) * c
#     thetaN = (2.0 * pi / vertexCount) * n

#     maxDist = -1
#     maxDistID = 0
#     for pt in points:
#         dx = averageX - pt.position[0]
#         dy = averageY - pt.position[1]
#         angleToPoint = atan2(dy, dx)
#         if (angleToPoint > thetaC) and (angleToPoint < thetaN):
#             dist = ((dx**2) + (dy**2)) ** 0.5
#             if dist > maxDist:
#                 maxDist = dist
#                 maxDistID = pt.id
    
#     vertexList.append(points[maxDistID])

# for c in range(len(vertexList)):
#     n = (c + 1) % vertexCount

#     x1 = vertexList[c].position[0]
#     y1 = vertexList[c].position[1]
#     x2 = vertexList[n].position[0]
#     y2 = vertexList[n].position[1]

#     pygame.draw.line(
#         screen, (0, 0, 255),
#         (x1, y1), (x2, y2),
#         1
#     )




# while(True):
#     screen.fill((0, 0, 0))

#     for ev in pygame.event.get():
#         if ev.type == pygame.MOUSEBUTTONUP:
#             pos = pygame.mouse.get_pos()

#             dx = pos[0] - averageX
#             dy = pos[1] - averageY
#             angle = (atan2(dy, dx) + (2.0 * pi)) % (2.0 * pi)
#             print(f"angle: {angle}")

for pt in points:
    pt.render()

pygame.display.flip()

input()