
import pygame
screenW, screenH = (700, 500)
screen = pygame.display.set_mode((screenW, screenH))

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from random import randint

from math import pi, cos, sin, atan2, exp

robotTurnRate = 0.1 # 
robotSpeed = 1 # How fast the robot moves through the corridor
corridorWidth = screenH * 0.5 # How wide the corridor is
corridorSegmentCount = 8 # The number of corridor segments before looping
noiseLength = int(corridorSegmentCount * robotSpeed) # The number of values in the noise list
corridorStartYNoise = LL.generate1DNoise(noiseLength, noiseScale=1.0, precisionDP=4, noiseMin=0.0, noiseMax=1.0, smooth=False) # 
# corridorStartYNoise = [LL.randomFloat(0.1, 0.9) for _ in range(noiseLength)]
noiseMax = max(corridorStartYNoise)
noiseMin = min(corridorStartYNoise)
noiseRange = noiseMax - noiseMin

# print(f"noise: {corridorStartYNoise}")

class Wall:
    def __init__(self, side, startNoiseIndex):
        self.side = side
        self.start = LL.Vector()
        self.end = LL.Vector()
        self.colour = (0,0,0) # (randint(0, 255), randint(0, 255), randint(0, 255))
        self.noiseIndex = startNoiseIndex

        self.setStartEnd()
    
    def setStartEnd(self, firstCall=True):

        startY = screenH * corridorStartYNoise[self.noiseIndex]
        endY = screenH * corridorStartYNoise[(self.noiseIndex+1) % noiseLength]

        dx = screenW
        dy = endY - startY
        angle = atan2(dy, dx)
        # print(f"side:{self.side}, dx:{dx}, dy:{dy}, angle:{angle}")

        leftWallMid = LL.Vector(
            (screenW/2) + (cos(angle-(pi/2)) * corridorWidth * 0.5),
            (screenH/2) + (sin(angle-(pi/2)) * corridorWidth * 0.5)
        )

        rightWallMid = LL.Vector(
            (screenW/2) + (cos(angle+(pi/2)) * corridorWidth * 0.5),
            (screenH/2) + (sin(angle+(pi/2)) * corridorWidth * 0.5)
        )

        wallWidth = screenW * 0.3
        wallHeight= screenH * 0.3

        if self.side == 'L':
            self.start = LL.Vector(
                leftWallMid.x - (cos(angle) * wallWidth),
                leftWallMid.y - (sin(angle) * wallHeight)
            )
            self.end = LL.Vector(
                leftWallMid.x + (cos(angle) * wallWidth),
                leftWallMid.y + (sin(angle) * wallHeight)
            )
        elif self.side == 'R':
            self.start = LL.Vector(
                rightWallMid.x - (cos(angle) * wallWidth),
                rightWallMid.y - (sin(angle) * wallHeight)
            )
            self.end = LL.Vector(
                rightWallMid.x + (cos(angle) * wallWidth),
                rightWallMid.y + (sin(angle) * wallHeight)
            )
        
        if firstCall:
            self.start.add(LL.Vector(screenW * self.noiseIndex))
            self.end.add(LL.Vector(screenW * self.noiseIndex))
        else:
            self.start.add(LL.Vector(screenW * 1))
            self.end.add(LL.Vector(screenW * 1))
    
    def move(self):
        
        movementVector = LL.Vector(-robotSpeed, 0)
        self.start.add(movementVector)
        self.end.add(movementVector)
        if self.end.x < 0:
            self.noiseIndex = (self.noiseIndex + 2) % noiseLength
            self.setStartEnd(False)
            # self.start.add(LL.Vector(screenW*2))
            # self.end.add(LL.Vector(screenW*2))

            # newIndex = (self.noiseIndex + 1) % noiseLength
            # self.__init__(self.side, newIndex)
    
    def render(self, renderColour=(100,100,100), renderThickness=4):
        x1 = int(self.start.x)
        y1 = int(self.start.y)
        x2 = int(self.end.x)
        y2 = int(self.end.y)
        pygame.draw.line(
            screen, self.colour, #renderColour,
            (x1, y1), (x2, y2),
            renderThickness
        )

Walls = [
    Wall('L', 0),
    Wall('R', 0),

    Wall('L', 1),
    Wall('R', 1)
]

class Robot:
    def __init__(self, startFacingDirection):
        self.position = LL.Vector(screenW * 0.1, screenH * 0.5)
        self.facingDir = startFacingDirection

        self.radius = int(corridorWidth * 0.1)
        
        self.sensorCount = 10 # 20
        self.sensorAngle = pi * 0.75 # 0.5

        # self.sensorCount = 10
        # self.sensorAngle = pi * (exp(-(self.sensorCount-1.2)) + 0.65)

        self.sensors = [LL.Sensor() for _ in range(self.sensorCount)]
        self.updateSensors()

    def updateSensors(self):
        posX = int(self.position.x)
        posY = int(self.position.y)

        for sensor in range(self.sensorCount):
            angle = self.facingDir - (self.sensorAngle / 2) + ((self.sensorAngle / (self.sensorCount-1)) * sensor)
            sensorX = posX + (cos(angle) * self.radius)
            sensorY = posY + (sin(angle) * self.radius)
            self.sensors[sensor].update(LL.Vector(sensorX, sensorY), angle)
            self.sensors[sensor].measure(Walls)
    
    def steer(self):
        # sensorReadings = [sensor.measuredDistance for sensor in self.sensors]
        # minReading = min(sensorReadings)

        # sensorReadingMultipliers = [
        #     sensorReadings[s] / minReading
        #     for s in range(self.sensorCount)
        # ]

        # sC = 5
        #  0,  1, 2, 3, 4
        # (sC-1)/2 = 2.0
        # -2, -1, 0, 1, 2
        
        # sC = 8
        #  0,    1,    2,    3,   4,   5,   6,   7
        # (sC-1)/2 = 3.5
        # -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5

        # sC = 12
        #  0,    1,    2,    3,    4,    5,   6,   7,   8,   9,   10,  11
        # (sC-1)/2 = 5.5
        # -5.5, -4.5, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5

        directionVectorList = []
        for s in range(self.sensorCount):
            
            angle = self.facingDir - (self.sensorAngle / 2) + ( (self.sensorAngle / (self.sensorCount-1)) * s )
            
            steeringVector = LL.Vector().fromAngle(angle)
            steeringVector.mult(self.sensors[s].measuredDistance**2)
            directionVectorList.append(steeringVector)
        
        averageVector = LL.Vector().sum(directionVectorList, True)

        directionDiff = averageVector.heading() - self.facingDir
        self.facingDir += (directionDiff * robotTurnRate)

    
    def move(self):
        self.position.y += (sin(self.facingDir) * robotSpeed)

        if self.position.y <= -self.radius:
            self.position.y = screenH + self.radius
        elif self.position.y > screenH + self.radius:
            self.position.y = -self.radius
    
    def render(self, fillColour=(150,150,150), outlineColour=(0,0,0), outlineThickness=2):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, fillColour,
            (x1, y1), self.radius,
            0
        )
        pygame.draw.circle(
            screen, outlineColour,
            (x1, y1), self.radius,
            outlineThickness
        )

        x2 = int( x1 + (cos(self.facingDir) * self.radius) )
        y2 = int( y1 + (sin(self.facingDir) * self.radius) )
        pygame.draw.line(
            screen, outlineColour,
            (x1, y1), (x2, y2),
            outlineThickness
        )

        for sensor in self.sensors:
            sensor.display(screen, thickness=outlineThickness)
        
robot = Robot(0.0)


while(True):
    screen.fill((255, 255, 255))

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP:
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - robot.position.x
            dy = mouseY - robot.position.y
            angle = atan2(dy, dx)
            robot.facingDir = angle

    for w in Walls:
        w.move()
        w.render()
    
    robot.updateSensors()
    robot.steer()
    robot.move()
    robot.render()

    pygame.display.flip()