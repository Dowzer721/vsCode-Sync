
import pygame
screenW, screenH = 700, 500
screen = pygame.display.set_mode((screenW, screenH))

from math import pi, cos, sin

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from random import randint

robotSpeed = 1 # How fast the robot moves through the corridor
corridorWidth = screenH * 0.5 # How wide the corridor is
corridorSegmentCount = 16 # The number of corridor segments before looping
noiseLength = corridorSegmentCount * robotSpeed # The number of values in the noise list
corridorDirectionNoise = LL.generate1DNoise(noiseLength) # The noise determining the directions of each segment of the corridor
noiseMax = max(corridorDirectionNoise) # Maximum value in noise
noiseMin = min(corridorDirectionNoise) # Minimum value in noise
noiseRange = noiseMax - noiseMin # Range of noise
# print(f"max:{round(noiseMax, 2)}, min:{round(noiseMin, 2)}, range:{round(noiseRange, 2)}")

class Wall:
    def __init__(self, side, startNoiseIndex):
        self.side = side
        self.start = LL.Vector()
        self.end = LL.Vector()
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.noiseIndex = startNoiseIndex

        self.setStartEnd()
    
    def setStartEnd(self):
        angle = corridorDirectionNoise[self.noiseIndex]

        leftWallMid = LL.Vector(
            (screenW/2) + (cos(angle - (pi/2)) * corridorWidth * 0.5),
            (screenH/2) + (sin(angle - (pi/2)) * corridorWidth * 0.5)
        )

        rightWallMid= LL.Vector(
            (screenW/2) + (cos(angle + (pi/2)) * corridorWidth * 0.5),
            (screenH/2) + (sin(angle + (pi/2)) * corridorWidth * 0.5)
        )

        if self.side == 'L':

            self.start = LL.Vector(
                leftWallMid.x - (cos(angle) * screenW * 0.5),
                leftWallMid.y - (sin(angle) * screenH * 0.5)
            )

            self.end = LL.Vector(
                leftWallMid.x + (cos(angle) * screenW * 0.5),
                leftWallMid.y + (sin(angle) * screenH * 0.5)
            )

        else:
            self.start = LL.Vector(
                rightWallMid.x - (cos(angle) * screenW * 0.5),
                rightWallMid.y - (sin(angle) * screenH * 0.5)
            )

            self.end = LL.Vector(
                rightWallMid.x + (cos(angle) * screenW * 0.5),
                rightWallMid.y + (sin(angle) * screenH * 0.5)
            )
    
    def move(self):
        angle = corridorDirectionNoise[self.noiseIndex]

        corridorDirection = LL.Vector().fromAngle(angle)

        self.start.sub(corridorDirection)
        self.end.sub(corridorDirection)

        if self.end.x < 0:
            self.noiseIndex = (self.noiseIndex + 1) % noiseLength

            # newAngle = 

            # dx = self.end.x - self.start.x
            # dy = self.end.y - self.start.y
            # # self.start.x = self.resetPosition.x
            # # self.start.y = self.resetPosition.y
            # self.start = self.resetPosition
            # self.end.x = self.start.x + dx
            # self.end.y = self.start.y + dy
    
    def render(self, renderColour=(100, 100, 100), renderThickness=(4)):
        if self.start.x > screenW: return

        x1, y1, _ = self.start.toInt()
        x2, y2, _ = self.end.toInt()
        pygame.draw.line(
            screen, self.colour, # renderColour,
            (x1, y1), (x2, y2),
            renderThickness
        )

Walls = [
    Wall('L', 0),
    Wall('R', 0),

    Wall('L', 1),
    Wall('R', 1)
]

class Vehicle:
    def __init__(self, startPosition, startFacingDirection):
        self.pos = startPosition
        self.dir = startFacingDirection

        self.radius = int(min(screenW, screenH) * 0.05)
        self.sensorCount = 4
        self.sensorAngle = pi
        self.sensors = [LL.Sensor() for _ in range(self.sensorCount)]
        self.updateSensors()
    
    def updateSensors(self):
        startAngle = self.dir - (self.sensorAngle / 2)
        for i in range(self.sensorCount):
            sensorAngle = startAngle + ( (self.sensorAngle / (self.sensorCount-1)) * i )
            sensorPosition = LL.Vector(
                self.pos.x + (cos(sensorAngle) * self.radius),
                self.pos.y + (sin(sensorAngle) * self.radius)
            )
            self.sensors[i].update(sensorPosition, sensorAngle)
            self.sensors[i].measure(Walls)
    
    def render(self, fillColour=(150,150,150), borderColour=(0,0,0), borderThickness=1):
        x1 = int(self.pos.x)
        y1 = int(self.pos.y)
        pygame.draw.circle(
            screen, fillColour,
            (x1, y1), self.radius,
            0
        )
        pygame.draw.circle(
            screen, borderColour,
            (x1, y1), self.radius,
            borderThickness
        )

        x2 = int(x1 + (cos(self.dir) * self.radius))
        y2 = int(y1 + (sin(self.dir) * self.radius))
        pygame.draw.line(
            screen, borderColour,
            (x1, y1),
            (x2, y2),
            borderThickness
        )

        for sensor in self.sensors:
            #display(self, screen, colour=(255, 100, 100), thickness=1):
            sensor.render(screen)
            
startPosition = LL.Vector(screenW*0.2, screenH*0.5)
startDirection= LL.randomFloat(-pi*0.1, pi*0.1)
robot = Vehicle(startPosition, startDirection)

while(True):
    screen.fill((255, 255, 255))

    for w in Walls:
        w.render()

    # for wall in Walls:
    #     wall.move()
    #     wall.render()


    robot.render()
    
    pygame.display.flip()