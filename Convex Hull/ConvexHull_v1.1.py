
from math import pi, cos, sin, atan2
import pygame
from random import randint
from time import time

screenW, screenH = 600, 500
screen = pygame.display.set_mode((screenW, screenH))

def rF(min_=0.0, max_=1.0, dec_=2):
    rng = max_ - min_
    pct = randint(0, 10**dec_) / float(10**dec_)
    return round(min_ + (rng * pct), dec_)

def wait(secs):
    timeStart = time()
    while(timeStart + secs > time()):
        pass

pointCount = 16
points = []
class Point:
    def __init__(self, id_, x_, y_):
        self.id = id_

        self.position = (x_, y_)
    def render(self, renderColour=(255, 100, 100), radius=4):
        pygame.draw.circle(
            screen, renderColour,
            self.position, radius, 0
        )
for i in range(pointCount):
    x = int(screenW * rF(0.1, 0.9))
    y = int(screenH * rF(0.1, 0.9))
    points.append(Point(i, x, y))

leftMostX = screenW
leftMostID = 0
for pt in points:
    if pt.position[0] < leftMostX:
        leftMostX = pt.position[0]
        leftMostID = pt.id

currentID = leftMostID
currentAngle = (3.0 * pi / 2.0)

vertexList = []

def drawCurrent(drawID=True, drawAngle=True):
    if drawID:
        pygame.draw.circle(
            screen, (100, 255, 100),
            points[currentID].position, 8, 1
        )
    if drawAngle:
        pygame.draw.line(
            screen, (100, 255, 100),
            points[currentID].position,
            (
                int(points[currentID].position[0] + (cos(currentAngle) * screenW * 0.1)),
                int(points[currentID].position[1] + (sin(currentAngle) * screenH * 0.1))
            )
        )

while(not (leftMostID in vertexList)):
    screen.fill((0,0,0))
    for pt in points:
        pt.render()

    # for ev in pygame.event.get():
    #     if ev.type == pygame.MOUSEBUTTONUP:
    #         pos = pygame.mouse.get_pos()

    drawCurrent()
    
    minAngle = currentAngle
    minDifference = (2.0 * pi)
    minDifferenceID = 0


    for pt in points:
        screen.fill((0,0,0))
        for pti in points:
            pti.render()
        drawCurrent()
        
        if pt.id == currentID: continue
        if pt.id in vertexList: continue

        dx = pt.position[0] - points[currentID].position[0]
        dy = pt.position[1] - points[currentID].position[1]
        angle = (atan2(dy, dx) + (pi * 2.0))# % (pi * 2.0)

        difference = abs(angle - currentAngle)
        # print(difference)

        if difference < minDifference:
            minAngle = angle
            minDifference = difference
            minDifferenceID = pt.id

        x2 = int(points[currentID].position[0] + (cos(angle) * screenW * 0.1) )
        y2 = int(points[currentID].position[1] + (sin(angle) * screenH * 0.1) )

        pygame.draw.line(
            screen, (255, 255, 255),
            points[currentID].position,
            (x2, y2),
            1
        )

        wait(0.01)
        pygame.display.flip()
    
    vertexList.append(minDifferenceID)
    currentID = minDifferenceID
    currentAngle = minAngle
        


    pygame.display.flip()

screen.fill((0,0,0))

for pt in points:
    pt.render()

for c in range(len(vertexList)):
    n = (c + 1) % len(vertexList)

    pygame.draw.line(
        screen, (200, 200, 200),
        points[vertexList[c]].position,
        points[vertexList[n]].position,
        1
    )

pygame.display.flip()

input("COMPLETE")