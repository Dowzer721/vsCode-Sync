
from math import pi, atan2, cos, sin
import pygame
from random import randint

screenW, screenH = 600, 500
screen = pygame.display.set_mode((screenW, screenH))

pointCount = 16
points = []
class Point:
    def __init__(self, id_, x_, y_):
        self.id = id_

        self.position = (x_, y_)

        self.connectedPoint = None
    
    def connectToPoint(self, pt):
        self.connectedPoint = pt
    
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

currentID = lowestXID
currentAngle = pi / 2.0
anglesToAllOtherPoints = []
#     atan2((points[i].position[1]-points[currentID].position[1]))
for i in range(pointCount):
    if i == currentID: continue

    dx = points[i].position[0] - points[currentID].position[0]
    dy = points[i].position[1] - points[currentID].position[1]
    angle = atan2(dy, dx)
    anglesToAllOtherPoints.append(angle)

"""
Next I want to find the difference in angle between "currentAngle" and each of the list angles, 
and then whichever difference is lowest is the angle leading to the next point around the convex hull
"""


while(True):
    screen.fill((255, 255, 255))

    for pt in points:
        pt.render()

    pygame.display.flip()