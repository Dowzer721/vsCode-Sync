
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\Route Navigation\\Maze\\")
from mazeGenerator import generate

sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin, atan2

from random import randint

import pygame

colCount, rowCount = 5, 5
mazeSize = colCount * rowCount

screenW = 500
screenH = int(screenW * (rowCount/colCount))
screen = pygame.display.set_mode((screenW, screenH))

gridW = screenW / colCount
gridH = screenH / rowCount

# generate(colCount, rowCount, startingLocation = -1, renderScreen=-1)
global maze
global allWalls

def newMaze():
    global maze
    global allWalls

    maze = generate(colCount, rowCount, (0,0), screen)

    allWalls = [] #Grid[i].walls for i in range(mazeSize)]
    class Wall:
        def __init__(self, start, end):
            self.start = start
            self.end = end

    for c in range(mazeSize):
        cellCol = maze[c].col
        cellColN= maze[c].col + 1
        cellRow = maze[c].row
        cellRowN= maze[c].row + 1

        cellCorners = [
            LL.Vector(cellCol * gridW, cellRow * gridH),
            LL.Vector(cellColN* gridW, cellRow * gridH),
            LL.Vector(cellColN* gridW, cellRowN* gridH),
            LL.Vector(cellCol * gridW, cellRowN* gridH)
        ]

        for w in range(4):
            if maze[c].walls[w] == 0: continue

            n = (w + 1) % 4
            allWalls.append(Wall(cellCorners[w], cellCorners[n]) )
newMaze()

robotTurnRate = 0.01
class Robot:
    def __init__(self):
        self.position = LL.Vector(gridW / 2, gridH / 2)
        self.facingDir = randint(-100, 100) / 1000.0
        self.velocity = 0.25

        self.radius = int( min(gridW, gridH) * 0.1 )

        self.sensorCount = 32
        self.sensorAngle = pi * 0.8
        self.sensors = [LL.Sensor() for _ in range(self.sensorCount)]
        self.updateSensors()
    
    def updateSensors(self):
        for s in range(self.sensorCount):
            angle = self.facingDir - (self.sensorAngle / 2) + (self.sensorAngle * s/(self.sensorCount-1))
            sensorPosition = LL.Vector(
                self.position.x + (cos(angle) * self.radius),
                self.position.y + (sin(angle) * self.radius)
            )
            self.sensors[s].update(sensorPosition, angle)
            self.sensors[s].measure(allWalls)
        
        # for s in range(self.sensorCount):
        #     if self.sensors[s].measuredDistance <= self.radius*4:
        #         oppositeSensor = (self.sensorCount - s - 1)
                
        #         self.sensors[s].measuredDistance /= 2.0
        #         self.sensors[oppositeSensor].measuredDistance *= 2.0
    
    def steer(self):
        
        directionVectorList = []
        angleSegment = self.sensorAngle / (self.sensorCount-1)
        for s in range(self.sensorCount):

            angle = self.facingDir - (self.sensorAngle / 2) + (angleSegment * s)

            steeringVector = LL.Vector().fromAngle(angle)
            steeringVector.mult(self.sensors[s].measuredDistance**3)
            directionVectorList.append(steeringVector)
        
        averageVector = LL.Vector().sum(directionVectorList, True)

        directionDiff = averageVector.heading() - self.facingDir
        self.facingDir += (directionDiff * robotTurnRate)

        self.facingDir = (self.facingDir + (pi * 2.0)) % (pi * 2.0)

        # self.facingDir += randint(-100, 100) / 10000.0

    def throttle(self):
        # midSensor = int(self.sensorCount / 2)
        # self.velocity = self.sensors[midSensor].measuredDistance / 100.0
        # self.velocity = sum([s.measuredDistance for s in self.sensors]) / self.sensorCount
        # print(self.velocity)

        sensorReadings = [
            self.sensors[s].measuredDistance
            for s in range(int(self.sensorCount * 0.45), int(self.sensorCount * 0.55))
        ]

        # sensorReadings = [s.measuredDistance for s in self.sensors]
        sensorAverage = sum(sensorReadings) / len(sensorReadings)
        speed = sensorAverage / 500.0
        self.velocity = speed
        # normalisedReadings = [round(s.measuredDistance / sensorAverage,2) for s in self.sensors]
        # input(f"r:{sensorReadings}, a:{sensorAverage}, n:{normalisedReadings}")
    
    def move(self):
        self.position.set(
            self.position.x + (cos(self.facingDir) * self.velocity),
            self.position.y + (sin(self.facingDir) * self.velocity)
        )
    
    def render(self, fillColour=(200,200,200), outlineColour=(0,0,0), outlineThickness=1):
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

        x2 = int(x1 + (cos(self.facingDir) * self.radius))
        y2 = int(y1 + (sin(self.facingDir) * self.radius))
        pygame.draw.line(
            screen, outlineColour,
            (x1, y1), (x2, y2),
            outlineThickness
        )

        if self.sensorCount <= 32:
            # for s in range(int(self.sensorCount * 0.45), int(self.sensorCount * 0.55)):
            #     self.sensors[s].render(screen)
            for s in self.sensors:
                s.render(screen)

robot = Robot()


while(True):
    screen.fill((255, 255, 255))

    for cell in maze:
        cell.render(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP:
            newMaze()
            # mousePos = pygame.mouse.get_pos()
            # dx = mousePos[0] - robot.position.x
            # dy = mousePos[1] - robot.position.y
            # robot.facingDir = atan2(dy, dx)
            # robot.velocity = 0.1

    robot.updateSensors()
    # robot.throttle()
    robot.steer()
    robot.move()
    robot.render()

    pygame.display.flip()