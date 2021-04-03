
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import pygame
import math
import random

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

nodeCount = 64
smoothCount = int(nodeCount * 0.6)
pathWidth = 50

vehicleCount = 2
drawVehicleSensorBeams = True

class Path:
    def __init__(self, nodeCount_, smoothCount_=int(nodeCount * 0.8), pathWidth_=50):
        self.nodeCount = nodeCount_
        
        self.noise = Luke.generate1DNoise(nodeCount_, smoothCount=smoothCount_)
        
        self.outerNodes  = []
        self.innerNodes  = []

        self.pathWidth = pathWidth_
        self.generateNodePositions(smoothCount_)
    
    def generateNodePositions(self, smoothCount_):

        centerNodes = []
        
        for c in range(self.nodeCount):
            theta = (math.pi * 2.0 / self.nodeCount) * c

            pathCenterRadiusX = (self.noise[c] * screenW * 0.5)
            pathCenterRadiusY = (self.noise[c] * screenH * 0.5)

            pathCenterNodeX = (screenW / 2) + (math.cos(theta) * pathCenterRadiusX)
            pathCenterNodeY = (screenH / 2) + (math.sin(theta) * pathCenterRadiusY)

            centerNodes.append(Luke.Vector(pathCenterNodeX, pathCenterNodeY))
        
        self.outerNodes.clear()
        self.innerNodes.clear()
        for c in range(self.nodeCount):
            n = (c + 1) % self.nodeCount

            nodeDx = centerNodes[n].x - centerNodes[c].x
            nodeDy = centerNodes[n].y - centerNodes[c].y
            angleToNextNode = math.atan2(nodeDy, nodeDx)

            outerNodeX = centerNodes[c].x + (math.cos(angleToNextNode - (math.pi / 2)) * (self.pathWidth / 2))
            outerNodeY = centerNodes[c].y + (math.sin(angleToNextNode - (math.pi / 2)) * (self.pathWidth / 2))
            self.outerNodes.append(Luke.Vector(outerNodeX, outerNodeY))

            innerNodeX = centerNodes[c].x + (math.cos(angleToNextNode + (math.pi / 2)) * (self.pathWidth / 2))
            innerNodeY = centerNodes[c].y + (math.sin(angleToNextNode + (math.pi / 2)) * (self.pathWidth / 2))
            self.innerNodes.append(Luke.Vector(innerNodeX, innerNodeY))
        
    def display(self, colour=(0, 0, 0), thickness = 1):
        
        for c in range(self.nodeCount):
            n = (c + 1) % self.nodeCount
        
            ox1 = int(self.outerNodes[c].x)
            oy1 = int(self.outerNodes[c].y)
            ox2 = int(self.outerNodes[n].x)
            oy2 = int(self.outerNodes[n].y)
            pygame.draw.line(
                screen, colour,
                (ox1, oy1), (ox2, oy2),
                thickness
            )

            ix1 = int(self.innerNodes[c].x)
            iy1 = int(self.innerNodes[c].y)
            ix2 = int(self.innerNodes[n].x)
            iy2 = int(self.innerNodes[n].y)
            pygame.draw.line(
                screen, colour,
                (ix1, iy1), (ix2, iy2),
                thickness
            )

            # if (c % int(math.log(nodeCount)) ) == 0:
            #     cx1 = int((ox1 + ix1) / 2.0)
            #     cy1 = int((oy1 + iy1) / 2.0)
            #     cx2 = int((ox2 + ix2) / 2.0)
            #     cy2 = int((oy2 + iy2) / 2.0)
            #     pygame.draw.line(
            #         screen, (100, 100, 100),
            #         (cx1, cy1), (cx2, cy2),
            #         thickness * 4
            #     )

path = Path(nodeCount, smoothCount, pathWidth)

class Vehicle:
    def __init__(self):
        randomNode = random.randint(0, nodeCount-1)
        x = ((path.innerNodes[randomNode].x + path.outerNodes[randomNode].x) / 2.0) + Luke.randomFloat(-0.1, 0.1)
        y = ((path.innerNodes[randomNode].y + path.outerNodes[randomNode].y) / 2.0) + Luke.randomFloat(-0.1, 0.1)

        self.position = Luke.Vector(x, y)

        self.velocity = Luke.Vector().fromAngle(Luke.randomFloat(max=math.pi * 2.0))

        self.radius = 10
        self.sensorCoverageAngle = math.pi * Luke.randomFloat(0.5, 1.0)
        self.sensorCount = random.randint(3, 11)
        self.sensors = [Vehicle.Sensor() for _ in range(self.sensorCount)]
    
    def updateSensors(self):

        for i in range(self.sensorCount):
            
            sensorAngle = self.velocity.heading() - (self.sensorCoverageAngle / 2.0) + ((self.sensorCoverageAngle / (self.sensorCount-1) ) * i)
            
            sensorNewX = self.position.x + (math.cos(sensorAngle) * self.radius)
            sensorNewY = self.position.y + (math.sin(sensorAngle) * self.radius)
            self.sensors[i].updatePosDir(
                Luke.Vector(sensorNewX, sensorNewY), 
                sensorAngle
            )
            # self.sensors[i].measure()
    
    def blipSensors(self):
        for sen in self.sensors:
            sen.measure()
    
    def steer(self):
        # This is only gonna work with x3 sensors, need to refactor this to work with any number of sensors:
        # leftSensorForce = self.sensors[0].measuredDistance * -0.05
        # rightSensorForce = self.sensors[2].measuredDistance * 0.05

        # totalSensorForce = leftSensorForce + rightSensorForce
        # self.velocity.add(Luke.Vector().fromAngle(totalSensorForce))
        # self.velocity.normalise()

        totalSensorForce = 0.0
        for i in range(self.sensorCount):
            angleDiff = self.velocity.heading() - self.sensors[i].facingDir

            inverseDist = (screenW * screenH) - self.sensors[i].measuredDistance
            
            angleXdist = angleDiff * inverseDist #self.sensors[i].measuredDistance
            
            totalSensorForce += angleXdist
        
        totalSensorForceAngle = totalSensorForce * 0.001

        dir = self.velocity.heading()
        self.velocity.rotateToAngle(dir + totalSensorForceAngle)


    def move(self):
        self.velocity.setMag(1.0 - (1.0 / self.sensorCount))
        self.position.add(self.velocity)

    
    def display(self):

        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, (0, 0, 0),
            (x1, y1), self.radius,
            1
        )

        x2 = x1 + int(math.cos(self.velocity.heading()) * self.radius)
        y2 = y1 + int(math.sin(self.velocity.heading()) * self.radius)
        pygame.draw.line(
            screen, (0, 0, 0),
            (x1, y1), (x2, y2),
            1
        )

        for sen in self.sensors:
            sen.display()
    
    class Sensor:
        def __init__(self, pos_=Luke.Vector(), dir_=0.0):
            if not isinstance(pos_, Luke.Vector):
                return
            self.pos = pos_ # Vector[2d]
            self.facingDir = dir_ # [f]loat
            self.measuredDistance = -1 # [f]loat
        def updatePosDir(self, newPos, newDir):
            if not isinstance(newPos, Luke.Vector):
                return
            self.pos = newPos
            self.facingDir = newDir
        def measure(self):
            cIPD = screenW * screenH

            x1 = self.pos.x
            y1 = self.pos.y
            x2 = x1 + math.cos(self.facingDir)
            y2 = y1 + math.sin(self.facingDir)
            
            # Outer
            for c in range(nodeCount):
                n = (c + 1) % nodeCount

                x3 = path.outerNodes[c].x
                y3 = path.outerNodes[c].y
                x4 = path.outerNodes[n].x
                y4 = path.outerNodes[n].y

                denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
                if denominator == 0.0:
                    continue
            
                t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
                u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

                if (t > 0.0) and (u > 0.0) and (u < 1.0):
                    x = x1 + (t * (x2-x1))
                    y = y1 + (t * (y2-y1))
                    dist = self.pos.distance(Luke.Vector(x, y))
                    cIPD = min(cIPD, dist)

            # Inner
            for c in range(nodeCount):
                n = (c + 1) % nodeCount

                x3 = path.innerNodes[c].x
                y3 = path.innerNodes[c].y
                x4 = path.innerNodes[n].x
                y4 = path.innerNodes[n].y

                denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
                if denominator == 0.0:
                    continue
            
                t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
                u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

                if (t > 0.0) and (u > 0.0) and (u < 1.0):
                    x = x1 + (t * (x2-x1))
                    y = y1 + (t * (y2-y1))
                    dist = self.pos.distance(Luke.Vector(x, y))
                    cIPD = min(cIPD, dist)

            if cIPD == screenW * screenH:
                self.measuredDistance = -1
            else:
                self.measuredDistance = cIPD
            
            return self.measuredDistance
        def display(self, colour=(255, 100, 100), thickness=2):
            x1 = int(self.pos.x)
            y1 = int(self.pos.y)
            pygame.draw.circle(
                screen, colour,
                (x1, y1), 2
            )

            if self.measuredDistance < 0:
                return

            if drawVehicleSensorBeams:
                x2 = x1 + int(math.cos(self.facingDir) * self.measuredDistance)
                y2 = y1 + int(math.sin(self.facingDir) * self.measuredDistance)
                pygame.draw.line(
                    screen, colour,
                    (x1, y1), (x2, y2),
                    thickness
                )

Population = []
for _ in range(vehicleCount):
    Population.append(Vehicle())

def restart():
    global path
    path = Path(nodeCount, smoothCount, pathWidth)

    for Veh in Population:
        Veh.__init__()
    
restart()


simRunning = True
while simRunning:
    screen.fill((255, 255, 255))
    path.display()

    mouseX, mouseY = pygame.mouse.get_pos()
    for Veh in Population:

        # mDx = mouseX - Veh.position.x
        # mDy = mouseY - Veh.position.y
        # angleToMouse = math.atan2(mDy, mDx)
        # Veh.velocity = Luke.Vector().fromAngle(angleToMouse)

        Veh.blipSensors()
        Veh.steer()
        Veh.move()

        Veh.updateSensors()
        Veh.display()

        if (Veh.position.x < 0) or (Veh.position.x > screenW) or (Veh.position.y < 0) or (Veh.position.y > screenH):
            Veh.__init__()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # path = Path(nodeCount)
                restart()
                continue

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                simRunning = False