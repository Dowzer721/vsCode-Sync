
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import math

import pygame
# pygame.init()



from Path import Path
# from Vehicle import Vehicle

screenW = 800
screenH = 400
screen = pygame.display.set_mode((screenW, screenH))

pathNodeCount = 16
smoothingCount = int(pathNodeCount * 0.8)
path = Path(pathNodeCount, smoothingCount, screenW, screenH)

class Vehicle:
    
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

            nodeCount = path.nodeCount * 2 #len(nodeList_)
            for c in range(nodeCount):
                if c < (nodeCount < 2):
                    n = (c + 1) % nodeCount
                else:
                    n = min((c + 1), nodeCount-1)

                x3 = path.nodes[c].x
                y3 = path.nodes[c].y
                x4 = path.nodes[n].x
                y4 = path.nodes[n].y

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
            if self.measuredDistance < 0:
                return

            x1 = int(self.pos.x)
            y1 = int(self.pos.y)
            pygame.draw.circle(
                screen, colour,
                (x1, y1), 2
            )

            x2 = x1 + int(math.cos(self.facingDir) * self.measuredDistance)
            y2 = y1 + int(math.sin(self.facingDir) * self.measuredDistance)
            pygame.draw.line(
                screen, colour,
                (x1, y1), (x2, y2),
                thickness
            )

    # Vehicle class initialisation:
    def __init__(self, x_=None, y_=None):
        if (x_ != None) and (y_ != None):
            self.position = Luke.Vector(x_, y_)
        else:
            x = Luke.randomFloat(screenW * 0.1, screenW * 0.9)
            y = Luke.randomFloat(screenH * 0.1, screenH * 0.9)
            self.position = Luke.Vector(x, y)
        
        self.velocity = Luke.Vector()

        self.radius = 10
        self.sensorCoverageAngle = math.pi * 0.8
        self.sensorCount = 3
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
            self.sensors[i].measure()
            
    
    def move(self):
        self.position.add(self.velocity)
    
    def edgeBounce(self):
        if (self.position.x < self.radius) or (self.position.x > screenW - self.radius):
            self.position.sub(self.velocity)
            self.velocity.x *= -0.9
        if (self.position.y < self.radius) or (self.position.y > screenH - self.radius):
            self.position.sub(self.velocity)
            self.velocity.y *= -0.9

    def display(self):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, (0, 0, 0),
            (x1, y1),
            self.radius, 1
        )
        
        dir = self.velocity.heading()
        x2 = x1 + int(math.cos(dir) * self.radius)
        y2 = y1 + int(math.sin(dir) * self.radius)
        pygame.draw.line(
            screen, (0, 0, 0),
            (x1, y1), (x2, y2),
            1
        )

        for sen in self.sensors:
            sen.display()

populationSize = 1
Population = []
for _ in range(populationSize):
    Population.append(Vehicle())

path.pathWidth = Population[0].radius * 8
path.generateNodePositions(screenW, screenH)

simRunning = True
while simRunning:
    screen.fill((255, 255, 255))
    path.display(screen)

    mouseX, mouseY = pygame.mouse.get_pos()

    for Veh in Population:

        # Veh.position.x = screenW / 2
        # Veh.position.y = screenH / 2

        mDx = mouseX - Veh.position.x
        mDy = mouseY - Veh.position.y
        angToMouse = math.atan2(mDy, mDx)
        Veh.velocity.x = math.cos(angToMouse) * 0.1
        Veh.velocity.y = math.sin(angToMouse) * 0.1
        # Veh.velocity = Luke.Vector().fromAngle(angToMouse)

        Veh.move()
        Veh.edgeBounce()
        Veh.updateSensors()
        Veh.display()

    pygame.display.flip()

    # # Press 'esc' to end program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = Path(pathNodeCount, smoothingCount, screenW, screenH)

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                simRunning = False

