
import pygame
pygame.display.init()

screenW = 800
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

import math
import random

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python")

import LukeLibrary as Luke

class Boundary: # (self, startPos, endPos)
    def __init__(self, startPos, endPos):
        self.start = startPos.copy()
        self.end = endPos.copy()
    def display(self, colour = (0, 0, 0), thickness = 1):
        pygame.draw.line(
            screen, colour,
            (self.start.x, self.start.y),
            (self.end.x, self.end.y),
            thickness
        )
borderSizeW = (screenW * 0.1)
borderSizeH = (screenH * 0.1)
innerBorderSizeW = borderSizeW * 3
innerBorderSizeH = borderSizeH * 3

objects = [
    [
        Boundary( # Outside Top edge
            Luke.Vector(borderSizeW, borderSizeH), Luke.Vector(screenW - borderSizeW, borderSizeH)
        ),
        Boundary( # Outside Right edge
            Luke.Vector(screenW - borderSizeW, borderSizeH), Luke.Vector(screenW - borderSizeW, screenH - borderSizeH)
        ),
        Boundary( # Outside Bottom edge
            Luke.Vector(screenW - borderSizeW, screenH - borderSizeH), Luke.Vector(borderSizeW, screenH - borderSizeH)
        ),
        Boundary( # Outside Left edge
            Luke.Vector(borderSizeW, screenH - borderSizeH), Luke.Vector(borderSizeW, borderSizeH)
        ),

        Boundary( # Inside Top edge
            Luke.Vector(innerBorderSizeW, innerBorderSizeH), Luke.Vector(screenW - innerBorderSizeW, innerBorderSizeH)
        ),
        Boundary( # Inside Right edge
            Luke.Vector(screenW - innerBorderSizeW, innerBorderSizeH), Luke.Vector(screenW - innerBorderSizeW, screenH - innerBorderSizeH)
        ),
        Boundary( # Inside Bottom edge
            Luke.Vector(screenW - innerBorderSizeW, screenH - innerBorderSizeH), Luke.Vector(innerBorderSizeW, screenH - innerBorderSizeH)
        ),
        Boundary( # Inside Left edge
            Luke.Vector(innerBorderSizeW, screenH - innerBorderSizeH), Luke.Vector(innerBorderSizeW, innerBorderSizeH)
        )
    ]
]

rW = borderSizeW * 0.9
rH = innerBorderSizeH * 0.75
num = 16
newObject = []
for c in range(num):
    n = (c + 1) % num
    sAngle = (math.pi * 2.0 / num) * c
    eAngle = (math.pi * 2.0 / num) * n
    
    mx = screenW - innerBorderSizeW
    my = screenH / 2 # - innerBorderSizeH

    start = Luke.Vector(
        mx + (math.cos(sAngle) * rW),
        my + (math.sin(sAngle) * rH)
    )
    end = Luke.Vector(
        mx + (math.cos(eAngle) * rW),
        my + (math.sin(eAngle) * rH)
    )

    newObject.append(Boundary(start, end) )
objects.append(newObject)

mouseObjectVertexCount = 8
mouseObjectRadius = 20
newObject = []
    # Boundary(Luke.Vector(0, 0), Luke.Vector(0, 0)) for _ in range(mouseObjectVertexCount)
#]
mx = borderSizeW * 1.8
my = screenH / 2.0
for c in range(mouseObjectVertexCount):
    n = (c + 1) % mouseObjectVertexCount

    sAngle = (math.pi * 2.0 / mouseObjectVertexCount) * c
    eAngle = (math.pi * 2.0 / mouseObjectVertexCount) * n

    start = Luke.Vector(
        mx + (math.cos(sAngle) * mouseObjectRadius),
        my + (math.sin(sAngle) * mouseObjectRadius)
    )
    end = Luke.Vector(
        mx + (math.cos(eAngle) * mouseObjectRadius),
        my + (math.sin(eAngle) * mouseObjectRadius)
    )

    newObject.append(Boundary(start, end))

objects.append(newObject)

class Sensor: # (self, Luke.Vector() pos_, float dir_)
    def __init__(self, pos_, dir_):
        self.position = pos_.copy()
        self.direction = Luke.Vector().fromAngle(dir_)
        self.measuredDistance = screenW * screenH
    
    def updatePosition(self, newPos, newDir):
        Px = newPos.x
        Py = newPos.y
        self.position.set(Px, Py)

        self.direction.x = math.cos(newDir)
        self.direction.y = math.sin(newDir)
    
    def measure(self):
        
        cIPD = screenW * screenH

        x1 = self.position.x
        y1 = self.position.y
        x2 = self.position.x + self.direction.x
        y2 = self.position.y + self.direction.y

        for Obj in objects:
            for B in Obj:
                x3 = B.start.x
                y3 = B.start.y
                x4 = B.end.x
                y4 = B.end.y

                denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
                if denominator == 0:
                    continue

                t = ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4))
                t /= denominator

                u = ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3))
                u *= -1 / denominator

                if (t > 0) and (u > 0) and (u < 1):
                    x = x1 + (t*(x2-x1))
                    y = y1 + (t*(y2-y1))
                    intersectPoint = Luke.Vector(x, y)
                    cIPD = min(cIPD, self.position.distance(intersectPoint) )
        
        if cIPD == (screenW * screenH):
            self.measuredDistance = -1
        else:
            self.measuredDistance = cIPD
        
        return self.measuredDistance
    
    def display(self, colour = (255, 150, 150), thickness = 1):
        if self.measuredDistance < 0: return

        dir = self.direction.heading()

        sX = int(self.position.x)
        sY = int(self.position.y)
        eX = int(sX + (math.cos(dir) * self.measuredDistance) )
        eY = int(sY + (math.sin(dir) * self.measuredDistance) )

        pygame.draw.line(
            screen, colour,
            (sX, sY), (eX, eY),
            thickness
        )

        pygame.draw.circle(
            screen, (200, 0, 0),
            (eX, eY), 2, 
            0
        )


class Vehicle: # (self, id_)
    def __init__(self, id_):
        self.id = id_

        minR = 5
        maxR = 15
        self.radius = random.randint(minR, maxR)
        
        x = (borderSizeW * 1.5) + self.radius # random.randint(0, screenW)
        y = (borderSizeH * 1.5) + self.radius # random.randint(0, screenH)
        self.position = Luke.Vector(x, y)

        self.topSpeed = Luke.randomFloat(0.5, 1.0) #1.0 / abs(minR - self.radius)
        self.velocity = Luke.Vector()

        self.radius = random.randint(10, 20)

        self.sensorCount = 7
        self.sensorAngle = math.pi / 1.0
        self.sensors = [Sensor(self.position, 0) for _ in range(self.sensorCount)]

    def repelNeighbours(self): # Not avoidance yet, merely simulating physical 'bumping'

        # return # Doesn't work at the moment, so return drops out of function immediately.
        for neighbour in Population:
            if self.id == neighbour.id: continue

            dx = self.position.x - neighbour.position.x
            dy = self.position.y - neighbour.position.y
            dist = math.sqrt((dx**2) + (dy**2))
            radSum = self.radius + neighbour.radius

            if dist < radSum:
                angleToNeighbour = neighbour.position.angleBetween(self.position) #self.position.angleBetween(neighbour.position)
                vecToNeighbour = Luke.Vector().fromAngle(angleToNeighbour)
                vecToNeighbour.mult(radSum / 4.0)

                self.position.sub(vecToNeighbour)



    def move(self):
        self.position.add(self.velocity)

    def edgeBounce(self):
        if (self.position.x > screenW - borderSizeW - self.radius):
            self.position.x = screenW - borderSizeW - self.radius - 1
            self.velocity.x *= -1
        elif (self.position.x < borderSizeW + self.radius):
            self.position.x = borderSizeW + self.radius + 1
            self.velocity.x *= -1
        
        if (self.position.y > screenH - borderSizeH - self.radius):
            self.position.y = screenH - borderSizeH - self.radius - 1
            self.velocity.y *= -1
        elif (self.position.y < borderSizeH + self.radius):
            self.position.y = borderSizeH + self.radius + 1
            self.velocity.y *= -1

    def updateSensors(self): # This function updates the location and direction of each of the onboard sensors.
        for i in range(self.sensorCount):
            theta = self.velocity.heading() - (self.sensorAngle / 2.0) + ((self.sensorAngle / (self.sensorCount-1)) * i )
            sensorX = self.position.x + (math.cos(theta) * self.radius)
            sensorY = self.position.y + (math.sin(theta) * self.radius)
            sensorPos = Luke.Vector(sensorX, sensorY)

            self.sensors[i].updatePosition(sensorPos, theta)
    
    def moveAccordingToSensors(self):
        # Step through each sensor, and subtract from the current velocity according to the angle of the 
        # sensor and the distance which it has measured. 
        # 
        # The closer the sensor angle is to the current heading, the stronger the effect it has upon the 
        # fleeing of walls.
        # What this means is that the direction of travel is altered to attempt to steer away from the 
        # closest objects and walls, and therefore towards the further ones.
        
        # The following numbers alongside are assuming 'self.sensorCount = 7'.
        for i in range(self.sensorCount): # 0 1 2 3 4 5 6
            forcePercent = abs(i - int(self.sensorCount / 2)) * 0.1 # 0.3 0.2 0.1 0.0 0.1 0.2 0.3
            
            # Inclusion of the following line makes the frontal sensors more effective
            # Exclusion of the following line makes the frontal sensors less effective
            forcePercent = 1.0 - forcePercent # 0.7 0.8 0.9 1.0 0.9 0.8 0.7

            # self.sensors[i].measure()
            distanceFromSensor = self.sensors[i].measure() # This function both sets the sensor distance, and 
            #                                                also returns it, allowing for this function to only 
            #                                                be called once before taking data from it, but also 
            #                                                drawing the sensor and laser beam.

            forceFromSensor = distanceFromSensor * forcePercent * 2.0

            sensorAngle = self.sensors[i].direction.heading() - math.pi # The opposite to the direction the sensor is facing.

            forceFromSensorVector = Luke.Vector().fromAngle(sensorAngle)
            forceFromSensorVector.mult(forceFromSensor)

            self.velocity.sub(forceFromSensorVector) # Take the force from the sensor away from the current velocity vector.

            # print(abs(forcePercent))
        
        self.velocity.limit(max_=self.topSpeed) # Once all the changing of the velocity has finished, limit the velocity.

    
    def display(self):
        x = int(self.position.x)
        y = int(self.position.y)

        pygame.draw.circle(
            screen, (0, 0, 0),
            (x, y), self.radius,
            1
        )

        for s in self.sensors:
            if s.measuredDistance > 0:
                s.display((255, 100, 100), 2)
    


    def update(self):
        self.updateSensors()
        # self.measureSensors()
        
        self.repelNeighbours()
        self.moveAccordingToSensors()
        self.move()
        self.edgeBounce()

        self.display()

Population = [Vehicle(i) for i in range(1)]

followMouse = True
def updateMouseObject():

    mx, my = pygame.mouse.get_pos()

    for c in range(mouseObjectVertexCount):
        n = (c + 1) % mouseObjectVertexCount

        cTheta = (math.pi * 2.0 / mouseObjectVertexCount) * c
        nTheta = (math.pi * 2.0 / mouseObjectVertexCount) * n

        sX = mx + (math.cos(cTheta) * mouseObjectRadius)
        sY = my + (math.sin(cTheta) * mouseObjectRadius)
        eX = mx + (math.cos(nTheta) * mouseObjectRadius)
        eY = my + (math.sin(nTheta) * mouseObjectRadius)
        
        objects[-1][c].start.x = sX
        objects[-1][c].start.y = sY
        objects[-1][c].end.x = eX
        objects[-1][c].end.y = eY



while(True):
    screen.fill((255, 255, 255))

    for Veh in Population:
        Veh.update()
    
    if followMouse:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                updateMouseObject()

    for Obj in objects:
        for B in Obj:
            B.display((100, 100, 100), 2)
    
    pygame.display.flip()
