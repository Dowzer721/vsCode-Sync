
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import math
import pygame

screenW = 700
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

vehicleRadius = 20

class Path:
    def __init__(self, nodeCount, smoothingCount=-1, pathWidth_=vehicleRadius*2.5):
        self.nodeCount = nodeCount
        
        self.pathNoise = LL.generate1DNoise(self.nodeCount, noiseScale=0.1, smoothCount=smoothingCount)

        self.innerNodes = []
        self.outerNodes = []

        self.pathWidth = pathWidth_
        self.setNodePositions()

    def setNodePositions(self):

        centerNodes = []

        for c in range(0, self.nodeCount):
            theta = (math.pi * 2.0 / self.nodeCount) * c

            pathCenterRadiusX = (self.pathNoise[c] * screenW * 0.5)
            pathCenterRadiusY = (self.pathNoise[c] * screenH * 0.5)

            pathCenterNodeX = (screenW / 2) + (math.cos(theta) * pathCenterRadiusX)
            pathCenterNodeY = (screenH / 2) + (math.sin(theta) * pathCenterRadiusY)

            centerNodes.append(LL.Vector(pathCenterNodeX, pathCenterNodeY))
        
        self.innerNodes.clear()
        self.outerNodes.clear()
        for c in range(0, self.nodeCount):
            n = (c + 1) % self.nodeCount

            nodeDx = centerNodes[n].x - centerNodes[c].x
            nodeDy = centerNodes[n].y - centerNodes[c].y
            angleToNextNode = math.atan2(nodeDy, nodeDx)

            self.outerNodes.append(LL.Vector(
                centerNodes[c].x + (math.cos(angleToNextNode - (math.pi/2)) * (self.pathWidth / 2)),
                centerNodes[c].y + (math.sin(angleToNextNode - (math.pi/2)) * (self.pathWidth / 2))
                )
            )

            self.innerNodes.append(LL.Vector(
                centerNodes[c].x + (math.cos(angleToNextNode + (math.pi/2)) * (self.pathWidth / 2)),
                centerNodes[c].y + (math.sin(angleToNextNode + (math.pi/2)) * (self.pathWidth / 2))
                )
            )

    def render(self):
        
        for c in range(0, self.nodeCount):
            n = (c + 1) % self.nodeCount

            ix1 = int(self.innerNodes[c].x)
            iy1 = int(self.innerNodes[c].y)
            ix2 = int(self.innerNodes[n].x)
            iy2 = int(self.innerNodes[n].y)
            pygame.draw.line(
                screen, (0, 0, 0),
                (ix1, iy1), (ix2, iy2),
                1
            )

            ox1 = int(self.outerNodes[c].x)
            oy1 = int(self.outerNodes[c].y)
            ox2 = int(self.outerNodes[n].x)
            oy2 = int(self.outerNodes[n].y)
            pygame.draw.line(
                screen, (0, 0, 0),
                (ox1, oy1), (ox2, oy2),
                1
            )
path = Path(64) #Path(256, 1200)

# see "path following 2.2: line 187 for next step"
class Vehicle:
    def __init__(self):
        startX = (path.innerNodes[0].x + path.outerNodes[0].x) / 2
        startY = (path.innerNodes[0].y + path.outerNodes[0].y) / 2
        self.position = LL.Vector(startX, startY)
        self.velocity = LL.Vector(0, 0.001)

        self.sensorAngle = math.pi
        self.sensorCount = 5
        self.sensors = [LL.Sensor() for _ in range(0, self.sensorCount)]
    def move(self):
        self.position.add(self.velocity)

    def updateSensors(self):
        for i in range(0, self.sensorCount):
            theta = self.velocity.heading() + ((self.sensorAngle / (self.sensorCount-1)) * i) - (self.sensorAngle / 2)
            x = self.position.x + (math.cos(theta) * vehicleRadius)
            y = self.position.y + (math.sin(theta) * vehicleRadius)
            self.sensors[i].update(LL.Vector(x, y), theta)
            self.sensors[i].measure(screen, wallList)

    def render(self):
        pygame.draw.circle(
            screen, (150, 100, 150),
            (int(self.position.x), int(self.position.y)),
            vehicleRadius, 1
        )
        for s in self.sensors:
            s.display(screen)

    def update(self):
        self.move()
        self.updateSensors()
        self.render()



Population = [Vehicle() for _ in range(0, 1)]

while(True):
    screen.fill((255, 255, 255))
    path.render()

    for veh in Population:
        veh.update()

    
    pygame.display.flip()