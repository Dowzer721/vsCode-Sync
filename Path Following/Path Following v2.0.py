
import sys
sys.path.insert(1, 'C:/Users/Luke/Documents/Learning Python/') # insert at 1, 0 is the script path (or '' in REPL)
import LukeLibrary as Luke

import pygame
import random
import math

screenW = 900
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

nodeCount = 128
minR = min(screenW, screenH) * 0.4
maxR = min(screenW, screenH) * 0.45
pathRadii = [
    Luke.randomFloat(minR, maxR) for _ in range(nodeCount)
]
smoothCount = int(nodeCount * 1.5)

def smoothRadii():
    for _ in range(smoothCount):
        for cur in range(nodeCount):
            pre = (cur + nodeCount - 1) % nodeCount
            nex = (cur + 1) % nodeCount
            preDiff = pathRadii[pre] - pathRadii[cur]
            nexDiff = pathRadii[nex] - pathRadii[cur]
            diffSum = preDiff + nexDiff
            pathRadii[cur] += (diffSum * 0.01)
smoothRadii()

class Path:
    def __init__(self):
        self.nodes = []
        for i in range(nodeCount):
            theta  = ((math.pi * 2.0) / nodeCount) * i
            radius = pathRadii[i]
            x = (screenW / 2) + (math.cos(theta) * radius)
            y = (screenH / 2) + (math.sin(theta) * radius)
            self.nodes.append(Luke.Vector(x, y))
    def display(self):
        for c in range(nodeCount):
            n = (c + 1) % nodeCount

            pygame.draw.line(
                screen, (0, 0, 0),
                (self.nodes[c].x, self.nodes[c].y),
                (self.nodes[n].x, self.nodes[n].y),
                1
            )
simPath = Path()

class Vehicle:
    def __init__(self, id_):
        self.id = id_
        x = random.randint(0, screenW)
        y = random.randint(0, screenH)
        self.position = Luke.Vector(x, y)
        self.velocity = Luke.Vector().fromAngle(Luke.randomFloat(max=2.0)*math.pi)
        self.radius = 10

    def move(self):
        self.position.add(self.velocity)
        self.edgeBounce()
    
    def edgeBounce(self):
        if (self.position.x <= self.radius):
            self.position.x += 1
            self.velocity.x *= -1
        elif (self.position.x >= screenW-self.radius):
            self.position.x -= 1
            self.velocity.x *= -1

        if (self.position.y <= self.radius):
            self.position.y += 1
            self.velocity.y *= -1
        elif (self.position.y >= screenH-self.radius):
            self.position.y -= 1
            self.velocity.y *= -1

    def display(self):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, (0, 0, 0), 
            (x1, y1),
            self.radius, 1
        )
        dir = self.velocity.heading()
        x2 = int(x1 + math.cos(dir) * self.radius)
        y2 = int(y1 + math.sin(dir) * self.radius)
        pygame.draw.line(
            screen, (0, 0, 0),
            (x1, y1), (x2, y2),
            1
        )
Population = [Vehicle(i) for i in range(2)]

while True:
    screen.fill((255, 255, 255))

    simPath.display()
    for Veh in Population:
        Veh.move()
        Veh.display()
        # if Veh.id == 0:
        #     print(Veh.velocity.getMag())
    
    pygame.display.flip()