
import pygame
import math
import random

screenW = 900
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

def randomFloat(min, max):
    rng = max - min
    pct = random.randint(0, 1000) / 1000.0
    return min + (rng * pct)

def valueIsBetween(val, min, max):
    return (min < val) and (val < max)

class Vector:
    def __init__(self, x_=0.0, y_=0.0):
        self.x = x_
        self.y = y_
    def fromAngle(self, angle):
        x = math.cos(angle)
        y = math.sin(angle)
        return Vector(x, y)
    def random(self, minX = 0, maxX = 1, minY = 0, maxY = 1):
        x = randomFloat(minX, maxX)
        y = randomFloat(minY, maxY)
        return Vector(x, y)
    def angleBetween(self, vecA, vecB):
        dx = vecA.x - vecB.x
        dy = vecA.y - vecB.y
        return math.atan2(dy, dx)
    def distance(self, vec):
        dx = vec.x - self.x
        dy = vec.y - self.y
        return math.sqrt((dx**2) + (dy**2))
    def copy(self):
        return Vector(self.x, self.y)
    # ---
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
    def mult(self, val):
        self.x *= val
        self.y *= val
    def limit(self, min, max):
        if (self.mag() < min):
            self.setMag(min)
        if (self.mag() > max):
            self.setMag(max)
    def setMag(self, newMag):
        dir = self.heading()
        self.x = math.cos(dir) * newMag
        self.y = math.sin(dir) * newMag
    # ---
    def heading(self):
        return math.atan2(self.y, self.x)
    def mag(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

Path = []

debugDraw = False
pathFluctuationAmount = 16
nodeCount = 32
for i in range(nodeCount):
    theta = ((math.pi * 2.0 / nodeCount) * i) + randomFloat(-0.1, 0.1)
    x = (screenW * 0.5) + (math.cos(theta) * screenW * 0.4) + random.randint(-pathFluctuationAmount, pathFluctuationAmount)
    y = (screenH * 0.5) + (math.sin(theta) * screenH * 0.4) + random.randint(-pathFluctuationAmount, pathFluctuationAmount)
    Path.append(Vector(int(x), int(y)) )

radius = 10
vehicleCount = 10
avoidanceDistance = int(radius * 4.0)
avoidanceSensorAngle = (math.pi * 0.1)
nodeReachedDistance = (radius * 2.0)
class Individual:
    def __init__(self, id_):
        self.id = id_
        self.position = Vector().random(screenW * 0.1, screenW * 0.9, screenH * 0.1, screenH * 0.9)
        
        self.velocity = Vector().fromAngle(randomFloat(0, math.pi * 2.0))
        self.velocity.mult(0.1)
        self.minSpeed = randomFloat(0.0, 0.1)
        self.maxSpeed = randomFloat(self.minSpeed, 1.0) #0.3

        lowestDist = math.pow(screenW, 2)
        lowestDistIndex = 0
        for i in range(nodeCount):
            dx = Path[i].x - self.position.x
            dy = Path[i].y - self.position.y
            dist = math.sqrt((dx ** 2) + (dy ** 2))
            if dist < lowestDist:
                lowestDist = dist
                lowestDistIndex = i
        self.seekingNode = lowestDistIndex

        # self.pathDirection = -1 # Counter clockwise
        # if random.randint(0, 1) == 1:
        #     self.pathDirection = 1 # Clockwise

        self.pathDirection = 1
        if id_ % 2 == 0:
            self.pathDirection = -1

    def seekNode(self):
        if self.position.distance(Path[self.seekingNode]) < nodeReachedDistance:
            self.seekingNode = ((self.seekingNode + self.pathDirection) % nodeCount)
            return
        angToNode = Vector().angleBetween(Path[self.seekingNode], self.position)
        vecToNode = Vector().fromAngle(angToNode)
        if debugDraw:
            pygame.draw.line(
                screen, (0, 0, 255),
                (self.position.x, self.position.y),
                (
                    self.position.x + (vecToNode.x * radius * 2),
                    self.position.y + (vecToNode.y * radius * 2)
                ), 2
            )
        vecToNode.mult(0.005)
        self.velocity.add(vecToNode)
    
    def avoidNeighbours(self):
        # for i in range(vehicleCount):
        #     if i == self.id: continue
        #     if self.position.distance(Population[i].position) < (avoidanceDistance * 2.0):
        #         angleToNeighbour = Vector().angleBetween(self.position, Population[i].position) + math.pi
        #         vecToNeighbour = Vector().fromAngle(angleToNeighbour)
        #         vecToNeighbour.mult(-0.01)
        #         self.velocity.add(vecToNeighbour)
        for i in range(vehicleCount):
            if i == self.id: continue
            if self.position.distance(Population[i].position) < avoidanceDistance:
                angleToNeighbour = Vector().angleBetween(Population[i].position, self.position)
                dir = self.velocity.heading()
                if debugDraw:
                    pygame.draw.line(
                        screen, (150, 0, 0),
                        (self.position.x, self.position.y),
                        (
                            self.position.x + (math.cos(angleToNeighbour) * radius * 2.0),
                            self.position.y + (math.sin(angleToNeighbour) * radius * 2.0)
                        ), 1
                    )
                if valueIsBetween(angleToNeighbour, dir - (avoidanceSensorAngle/2.0), dir + (avoidanceSensorAngle/2.0)):
                    # self.velocity.add(Vector().fromAngle(0.1))
                    if angleToNeighbour < dir:
                        self.velocity.add(Vector().fromAngle(0.05))
                    else:
                        self.velocity.add(Vector().fromAngle(-0.05))

    def move(self):
        self.velocity.limit(self.minSpeed, self.maxSpeed)
        self.velocity.mult(0.99)
        self.position.add(self.velocity)
    def edgeLoop(self):
        if (self.position.x < -radius): self.position.x = screenW + radius
        elif (self.position.x > screenW + radius): self.position.x = -radius

        if (self.position.y < -radius): self.position.y = screenH + radius
        elif (self.position.y > screenH + radius): self.position.y = -radius
    def display(self):
        dir = self.velocity.heading()
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.polygon(
            screen, (50, 50, 50),
            (
                (
                    int( x + (math.cos(dir) * radius) ),
                    int( y + (math.sin(dir) * radius) )
                ),
                (
                    int( x + (math.cos(dir + (math.pi * 0.8)) * radius) ),
                    int( y + (math.sin(dir + (math.pi * 0.8)) * radius) )
                ),
                (
                    x,
                    y
                ),
                (
                    int( x + (math.cos(dir - (math.pi * 0.8)) * radius) ),
                    int( y + (math.sin(dir - (math.pi * 0.8)) * radius) )
                ),
            )
        )
        if self.id == 0 and debugDraw:
            pygame.draw.circle(
                screen, (255, 0, 0),
                (x, y),
                avoidanceDistance, 1
            )
    def update(self):
        self.seekNode()
        # self.avoidNeighbours()
        self.move()
        self.edgeLoop()
        self.display()
Population = [Individual(i) for i in range(vehicleCount)]

while(True):
    screen.fill((200, 200, 200))

    for i in range(nodeCount):
        if debugDraw:
            pygame.draw.circle(
                screen, (0, 150, 0),
                (Path[i].x, Path[i].y), 4
            )
            pygame.draw.circle(
                screen, (0, 0, 150),
                (Path[i].x, Path[i].y), int(nodeReachedDistance), 1
            )
        n = (i + 1) % nodeCount
        pygame.draw.line(
            screen, (0, 150, 0),
            (Path[i].x, Path[i].y),
            (Path[n].x, Path[n].y),
            2
        )

    for Ind in Population:
        Ind.update()

    pygame.display.flip()