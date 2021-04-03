
# Allows me to add to the system path (where the compiler looks for Modules and Packages) on the fly.
# It may be easier to edit the actual path, but for now this is fine.
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# The following line allows me not to have to type LukeLibrary.Vector(0, 0) each time, but instead just 
# Vector(0, 0), as if it were stock Python. 
# The downside to this is that in order to use other portions of LukeLibrary, I have to include them all here. 
# If I knew I was using everything in LukeLibrary, I could instead just put an asterisk in place, 
# as this tells the compiler to include everything.
from LukeLibrary import Vector, Sensor, randomFloat

import math

# Used for visuals only; actual Mathematics, Physics and simulation doesn't depend on this.
import pygame
pygame.display.init()
screenW = 600
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))



class Boundary:
    def __init__(self, x1, y1, x2, y2):
        self.start = Vector(int(x1), int(y1) )
        self.end = Vector(int(x2), int(y2) )
    def display(self, colour=(0, 200, 0), thickness=1):
        pygame.draw.line(
            screen, colour,
            (self.start.x, self.start.y),
            (self.end.x, self.end.y),
            thickness
        )
screenBorderSize = 20
Boundaries = [
    Boundary(screenBorderSize, screenBorderSize, screenW - screenBorderSize, screenBorderSize),
    Boundary(screenW - screenBorderSize, screenBorderSize, screenW - screenBorderSize, screenH - screenBorderSize),
    Boundary(screenW - screenBorderSize, screenH - screenBorderSize, screenBorderSize, screenH - screenBorderSize),
    Boundary(screenBorderSize, screenH - screenBorderSize, screenBorderSize, screenBorderSize)
]

globallyRecordedPoints = []
def drawRecordedPoints(colour=(0, 0, 255)):
    
    pointCount = len(globallyRecordedPoints)
    if pointCount < 2: return

    for c in range(pointCount):

        x1 = int(globallyRecordedPoints[c].x)
        y1 = int(globallyRecordedPoints[c].y)
        pygame.draw.circle(
            screen, colour,
            (x1, y1),
            2, 0
        )
        
        # This is not correct, because instead of joining each point up with the next one in the array, 
        # it should instead join with whichever point is closest to it in 2D distance, 
        # and is not already connected.

        # n = (c + 1) % pointCount

        # x1 = int(globallyRecordedPoints[c].x)
        # y1 = int(globallyRecordedPoints[c].y)
        # x2 = int(globallyRecordedPoints[n].x)
        # y2 = int(globallyRecordedPoints[n].y)
        # pygame.draw.line(
        #     screen, colour, 
        #     (x1, y1), (x2, y2),
        #     1
        # )





    for V in globallyRecordedPoints:
        x = int(V.x)
        y = int(V.y)
        pygame.draw.circle(
            screen, colour, 
            (x, y), 2, 0
        )


class Vehicle:
    def __init__(self):
        x = int(randomFloat(screenW * 0.2, screenW * 0.8) )
        y = int(randomFloat(screenH * 0.2, screenH * 0.8) )
        self.position = Vector(x, y)
        self.direction = randomFloat(0.0, math.pi * 2.0)
        self.speed = 0.1

        self.radius = 10

        self.sensorCount = 3
        self.sensorAngle = math.pi
        self.sensors = [Sensor() for _ in range(self.sensorCount)]
    def display(self, colour=(0, 0, 0), thickness=1):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, colour,
            (x1, y1), self.radius, thickness
        )
        x2 = x1 + int(math.cos(self.direction) * self.radius)
        y2 = y1 + int(math.sin(self.direction) * self.radius)
        pygame.draw.line(
            screen, colour,
            (x1, y1), (x2, y2),
            thickness
        )
    def move(self):
        self.position.x += (math.cos(self.direction) * self.speed)
        self.position.y += (math.sin(self.direction) * self.speed)
    def edgeBounce(self):
        xVel = math.cos(self.direction) * self.speed
        yVel = math.sin(self.direction) * self.speed
        if (self.position.x < screenBorderSize + self.radius) or (self.position.x > screenW - screenBorderSize - self.radius):
            xVel *= -1
            self.position.x += xVel
        if (self.position.y < screenBorderSize + self.radius) or (self.position.y > screenH - screenBorderSize - self.radius):
            yVel *= -1
            self.position.y += yVel
        self.direction = math.atan2(yVel, xVel)
    def updateSensors(self):
        for i in range(self.sensorCount):
            theta = self.direction - (self.sensorAngle / 2.0) + ((self.sensorAngle / (self.sensorCount - 1)) * i)
            sensorPos = Vector(
                self.position.x + (math.cos(theta) * self.radius),
                self.position.y + (math.sin(theta) * self.radius)
            )
            self.sensors.append(Sensor())
            self.sensors[i].update(sensorPos, theta)
    def measureSensors(self):
        
        for i in range(self.sensorCount):
            dist  = self.sensors[i].measure(screen, Boundaries)
            theta = self.sensors[i].direction
            ptX = self.sensors[i].position.x + (math.cos(theta) * dist)
            ptY = self.sensors[i].position.y + (math.sin(theta) * dist)
            globallyRecordedPoints.append( Vector(ptX, ptY) )
            self.sensors[i].display(screen, (255, 0, 0), 8)

    def update(self, sensorRead):
        self.move()
        self.edgeBounce() # Need to implement steering via sensors, but for now this is fine.
        self.updateSensors()

        if sensorRead:
            self.measureSensors()

        self.display()

Population = [Vehicle() for _ in range(1)]

frameCount = 1
sensorBlipFrame = 500
sensorBlipTime  = 10
sensorBlipOff = sensorBlipFrame + sensorBlipTime
sensorsReading = False

while True:
    screen.fill((255, 255, 255))

    if frameCount % sensorBlipFrame == 0:
        sensorsReading = True
        sensorBlipOff = sensorBlipFrame + sensorBlipTime
    if frameCount >= sensorBlipOff:
        sensorsReading = False
        frameCount = 0

    for B in Boundaries:
        B.display()

    for V in Population:
        V.update(sensorsReading)
    
    drawRecordedPoints()

    pygame.display.flip()

    # print(frameCount)
    frameCount += 1