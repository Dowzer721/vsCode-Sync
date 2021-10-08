
import math

import os
position = 10, 100
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

import pygame
pygame.display.init()
# pygame.init()

screenW = 950
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

# pygame.font.init()
# myfont = pygame.font.SysFont('Comic Sans MS', 20)
# textSurface = myfont.render('EXAMPLE', False, (0, 0, 0))

import random

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python")
# import LukeLibrary as Luke
from LukeLibrary import *

import time

#region class Boundary : Boundaries[]
class Boundary:
    def __init__(self, start=[-1,-1], end=[-1,-1]):
        self.start = Vector(int(start[0]), int(start[1]) )
        self.end = Vector(int(end[0]), int(end[1]) )
    def setStartEnd(self, newStart, newEnd):
        self.start.x, self.start.y = newStart
        self.end.x, self.end.y = newEnd

    def display(self, colour=(255, 150, 150), thickness=1):
        pygame.draw.line(
            screen, colour,
            (self.start.x, self.start.y),
            (self.end.x, self.end.y),
            thickness
        )

outerWallEdgeDistance = 0.1
innerWallEdgeDistance = 0.2

Boundaries = []
outerWallCoords = [
    [screenW * outerWallEdgeDistance,     screenH * outerWallEdgeDistance],
    [screenW * (1-outerWallEdgeDistance), screenH * outerWallEdgeDistance],
    [screenW * (1-outerWallEdgeDistance), screenH * (1-outerWallEdgeDistance)],
    [screenW * outerWallEdgeDistance,     screenH * (1-outerWallEdgeDistance)]
]

innerWallCoords = [
    [screenW * innerWallEdgeDistance,     screenH * innerWallEdgeDistance],
    [screenW * (1-innerWallEdgeDistance), screenH * innerWallEdgeDistance],
    [screenW * (1-innerWallEdgeDistance), screenH * (1-innerWallEdgeDistance)],
    [screenW * innerWallEdgeDistance,     screenH * (1-innerWallEdgeDistance)]
]

for c in range(4):
    n = (c + 1) % 4
    start = [outerWallCoords[c][0], outerWallCoords[c][1]]
    end = [outerWallCoords[n][0], outerWallCoords[n][1]]
    Boundaries.append(Boundary(start, end))

for c in range(4):
    n = (c + 1) % 4
    start = [innerWallCoords[c][0], innerWallCoords[c][1]]
    end = [innerWallCoords[n][0], innerWallCoords[n][1]]
    Boundaries.append(Boundary(start, end))

Bx = []
By = []
for o in outerWallCoords:
    Bx.append(o[0])
    By.append(o[1])
for i in innerWallCoords:
    Bx.append(i[0])
    By.append(i[1])
#endregion

#region class Sensor
# class Sensor:
#     def __init__(self):
#         self.position = Vector()
#         self.direction = 0.0
#         self.measuredDistance = -1.0
    
#     def measure(self, vehicleIdCallingFunction=-1):
#         # https://en.m.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
        
#         cIPD = screenW * screenH

#         x1 = self.position.x
#         y1 = self.position.y
#         x2 = x1 + math.cos(self.direction)
#         y2 = y1 + math.sin(self.direction)

#         # fullBoundaryList = Boundaries
#         # if avoidNeighbours:
#         #     for V in Vehicles:
#         #         if V.id == vehicleIdCallingFunction: continue

#         #         for B in V.bodyBoundaries:
#         #             fullBoundaryList.append(B)

#         for B in Boundaries:
#             x3 = B.start.x
#             y3 = B.start.y
#             x4 = B.end.x
#             y4 = B.end.y

#             denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
#             if denominator == 0.0:
#                 continue
            
#             t =  ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
#             u = -( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

#             if (t > 0) and (u > 0) and (u < 1):
#                 x = x1 + (t * (x2-x1))
#                 y = y1 + (t * (y2-y1))
#                 dx = x1 - x
#                 dy = y1 - y
#                 dist = math.sqrt((dx**2) + (dy**2))
#                 cIPD = min(cIPD, dist)
        
        
#         if cIPD == screenW * screenH:
#             self.measuredDistance = -1
#         else:
#             self.measuredDistance = cIPD
        
#         return self.measuredDistance
    
#     def display(self, colour=(255, 150, 150), thickness=1):
#         if self.measuredDistance > 0:
#             x1 = int(self.position.x)
#             y1 = int(self.position.y)
#             x2 = int(self.position.x + (math.cos(self.direction) * self.measuredDistance))
#             y2 = int(self.position.y + (math.sin(self.direction) * self.measuredDistance))
            
#             if thickness > 0:
#                 pygame.draw.line(
#                     screen, colour,
#                     (x1, y1), (x2, y2),
#                     thickness
#                 )
#             else:
#                 thickness = 3

#             pygame.draw.circle(
#                 screen, colour,
#                 (x2, y2), thickness + 1,
#                 0
#             )

            


#endregion

#region class Vehicle : Vehicles[]
oiWED_Diff = abs(outerWallEdgeDistance - innerWallEdgeDistance)
minR = min(screenW * oiWED_Diff, screenH * oiWED_Diff) * 0.2 * 0.5
maxR = max(screenW * oiWED_Diff, screenH * oiWED_Diff) * 0.4 * 0.5

vehicleCount = 8
avoidNeighbours = True
showSensors = True
bodyBoundaryCount = 6

class Vehicle:
    def __init__(self, id_):
        
        self.id = id_
        
        self.radius = 10# random.randint(int(minR), int(maxR)) # 10

        self.direction = 0.0

        # Use odd  numbers for x-axis reference
        # Use even numbers for y-axis reference
        #   ______0______
        #  |   _______   |
        #  |  |   4   |  |
        # 3|  |7     5|  |1
        #  |  |___6___|  |
        #  |_____________|
        #         2

        # Setting default start position to middle of top left corner.
        x = outerWallEdgeDistance * 1.5 * screenW
        y = outerWallEdgeDistance * 1.5 * screenH
        try:
            startingSegment = (id_ % 4) # random.randint(0, 3) # (id_ % 4) # 0:T 1:R 2:B 3:L
            if startingSegment==0:
                x = random.randint(Bx[7] + self.radius, Bx[5] - self.radius)
                y = random.randint(By[0] + self.radius, By[4] - self.radius)
                self.direction = math.pi * random.randint(0, 1)
            elif startingSegment==1:
                x = random.randint(Bx[5] + self.radius, Bx[1] - self.radius)
                y = random.randint(By[4] + self.radius, By[6] - self.radius)
                self.direction = (math.pi/2) + (math.pi * random.randint(0, 1))
            elif startingSegment==2:
                x = random.randint(Bx[7] + self.radius, Bx[5] - self.radius)
                y = random.randint(By[6] + self.radius, By[2] - self.radius) 
                self.direction = math.pi * random.randint(0, 1)
            elif startingSegment==3:
                x = random.randint(Bx[3] + self.radius, Bx[7] - self.radius)
                y = random.randint(Bx[4] + self.radius, Bx[6] - self.radius)
                self.direction = (math.pi/2) + (math.pi * random.randint(0, 1))
        except:
            pass

        # EMPTY RANDRANGE ERROR: This is because the coordinates supplied here don't have enough of a gap to be used 
        # in this random function. I quite honestly don't know how to solve this problem. 
        # Using try-except because I'm lazy.

        self.position = Vector(x, y)

        self.speed = 0.1
        self.maxSpeed = randomFloat(1.0, 3.0) # 1.0 # 2.5

        self.sensorCount = random.randint(4, 11)
        self.sensorAngle = math.pi / randomFloat(0.8, 2.0) # random.randint(1, 3) # math.pi / 1.0
        self.sensors = [Sensor() for _ in range(self.sensorCount)]

        # These sensors are not used by the robot, but instead are 
        # used for stopping the robot passing through the walls.
        # self.wallLimitSensors = [Sensor() for _ in range(4)]

        if avoidNeighbours:
            # self.bodyBoundaries = [Boundary() for _ in range(bodyBoundaryCount)]
            for _ in range(bodyBoundaryCount):
                Boundaries.append(Boundary())
    
    def move(self):
        self.position.x += math.cos(self.direction) * self.speed
        self.position.y += math.sin(self.direction) * self.speed
        
    def wallLimits(self):
        # This function prevents the Vehicle from leaving the corridor. 
        # This is just simulating the walls being real and disallowing the Vehicle to pass right through. 
        # There is a bug where the Vehicle can pass through the inner corners, of which it is easier to just 
        # reset the Vehicle than to solve this problem properly.

        if (
            # Vehicle is within the central area (where it should never reach), so reset it to the start position.
            (self.position.x > Bx[7]) and (self.position.x < Bx[5]) and (self.position.y > By[4]) and (self.position.y < By[6])
        ) or (
            # Vehicle is outside the external walls, so reset it to the start position.
            (self.position.x > Bx[1] - self.radius) or (self.position.x < Bx[3] + self.radius) or (self.position.y > By[2] - self.radius) or (self.position.y < By[0] + self.radius)
        ):
            # Recall the __init__() function to 'respawn' the Vehicle
            self.__init__(self.id)
 
    def neighbourBump(self):
        # This function prevents the Vehicles from passing through one another. 
        # This function also pushes the Vehicles apart according to their relative size; the larger Vehicle 
        # will push the smaller Vehicle back, but lots of small Vehicles could push back one large Vehicle 
        # (as long as the total size was greater). This is merely done for adding an additional layer of 
        # realism to the simulation.

        for V in Vehicles:
            if V.id == self.id: continue

            radSum = self.radius + V.radius
            dist = self.position.distance(V.position)
            if dist < radSum:
                angleToNeighbour = self.position.angleBetween(V.position)
                
                self.position.x -= math.cos(angleToNeighbour) * (V.radius / self.radius)
                self.position.y -= math.sin(angleToNeighbour) * (V.radius / self.radius)
                V.position.x    += math.cos(angleToNeighbour) * (self.radius / V.radius)
                V.position.y    += math.sin(angleToNeighbour) * (self.radius / V.radius)
    
    def updateSensors(self):
        for i in range(self.sensorCount):
            theta = self.direction - (self.sensorAngle / 2) + ((self.sensorAngle / (self.sensorCount-1)) * i)
            sX = self.position.x + (math.cos(theta) * self.radius)
            sY = self.position.y + (math.sin(theta) * self.radius)
            self.sensors[i].position.set(sX, sY)
            self.sensors[i].direction = theta
            
            # self.sensors[i].measure(self.id, Boundaries)
            # self.sensors[i].measure(screen, Boundaries)
            self.sensors[i].measure(Boundaries)

    def updateBodyBoundaries(self):
        for c in range(bodyBoundaryCount):
            n = (c + 1) % bodyBoundaryCount
            
            cAngle = (math.pi * 2.0 / bodyBoundaryCount) * c
            nAngle = (math.pi * 2.0 / bodyBoundaryCount) * n

            cX = self.position.x + (math.cos(self.direction + cAngle) * self.radius)
            cY = self.position.y + (math.sin(self.direction + cAngle) * self.radius)
            nX = self.position.x + (math.cos(self.direction + nAngle) * self.radius)
            nY = self.position.y + (math.sin(self.direction + nAngle) * self.radius)

            # self.bodyBoundaries[c].start.set(cX, cY)
            # self.bodyBoundaries[c].end.set(nX, nY)

            bodyBoundaryStartIndex = 8 + (self.id * bodyBoundaryCount) + c

            Boundaries[bodyBoundaryStartIndex].start.set(cX, cY)
            Boundaries[bodyBoundaryStartIndex].end.set(nX, nY)

            # start = Vector(cX, cY)
            # end = Vector(nX, nY)
            # self.bodyBoundaries[c].start = start
            # self.bodyBoundaries[c].end = end
            
    def moveAccordingToSensors(self): 
        
        totalSensorRatio = 0.0
        for i in range(int(self.sensorCount / 2)):
            leftSensorNum = i
            rightSensorNum = (self.sensorCount - 1) - i
            leftSensorValue = max(0.0001, self.sensors[leftSensorNum].measuredDistance) # Prevents division by zero.
            rightSensorValue = self.sensors[rightSensorNum].measuredDistance
            sensorRatio = rightSensorValue / leftSensorValue
            totalSensorRatio += (sensorRatio - 1.0)
        
        self.direction += (totalSensorRatio / 10.0)

    def adjustSpeed(self):
        sensorReading = 0.0
        if self.sensorCount % 2 == 0:
            # self.sensorCount IS EVEN, MEANING THERE ARE TWO CENTRAL SENSORS
            midSensors = [
                int(self.sensorCount / 2),
                int(self.sensorCount / 2) + 1
            ]
            sensorReading = (self.sensors[midSensors[0]].measuredDistance + self.sensors[midSensors[1]].measuredDistance) / 2.0
        else:
            # self.sensorCount IS ODD, MEANING THERE IS ONE CENTRAL SENSOR
            midSensor = int(self.sensorCount / 2)
            sensorReading = self.sensors[midSensor].measuredDistance

        forwardTargetDistance = self.radius * 8.0
        dDist = sensorReading - forwardTargetDistance
        self.speed += (dDist / 100.0)
        self.speed = max(1, min(self.speed, self.maxSpeed))

    def display(self, colour=(0, 0, 0), thickness=1):
        x = int(self.position.x)
        y = int(self.position.y)
        dir = self.direction

        if avoidNeighbours:
            bodyBoundaryStartIndex = 8 + (self.id * bodyBoundaryCount)
            bodyBoundaryEndIndex = bodyBoundaryStartIndex + bodyBoundaryCount

            for i in range(bodyBoundaryStartIndex, bodyBoundaryEndIndex):
                Boundaries[i].display(colour, thickness)
        else:
            pygame.draw.circle(
                screen, colour,
                (x, y), self.radius,
                thickness
            )
        
        pygame.draw.line(
            screen, colour,
            (x, y),
            (
                x + int(math.cos(dir) * self.radius),
                y + int(math.sin(dir) * self.radius)
            ), thickness
        )

        if showSensors:
            for s in self.sensors:
                s.render(screen)
    
    def update(self):
        self.updateSensors()
        self.moveAccordingToSensors()
        self.adjustSpeed()

        self.neighbourBump()
        self.wallLimits()

        self.move()
        if avoidNeighbours:
            self.updateBodyBoundaries()

        self.display()

Vehicles = [Vehicle(i) for i in range(vehicleCount)]
#endregion

def findClosestWallPositionToVehicle(id=0):
    midToVehicleSensor = Sensor()

    dx = Vehicles[id].position.x - (screenW / 2)
    dy = Vehicles[id].position.y - (screenH / 2)
    theta = math.atan2(dy, dx)

    midToVehicleSensor.position.set(screenW / 2, screenH / 2)
    midToVehicleSensor.direction = theta

    # midToVehicleSensor.measure(screen, Boundaries)
    midToVehicleSensor.measure(Boundaries)
    if showSensors:
        # midToVehicleSensor.display((0, 255, 0), -1)
        midToVehicleSensor.render(screen, (0, 255, 0), 1)

#region Main Simulation Loop
startTime = time.time()
frameCount = 0
while(True):
    screen.fill((255, 255, 255))
    
    for i in range(8):
        Boundaries[i].display()
    
    for V in Vehicles:
        V.update()
    
        findClosestWallPositionToVehicle(V.id)

    pygame.display.flip()

    frameCount += 1

    fpsShowTime = 1 / 16
    if time.time() - startTime >= fpsShowTime:
        fps = frameCount / fpsShowTime
        print("FPS: ~%.1f" %fps)

        startTime = time.time()
        frameCount = 0
    
#endregion