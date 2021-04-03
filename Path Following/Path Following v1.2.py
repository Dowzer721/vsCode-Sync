
import sys
sys.path.insert(1, 'C:/Users/Luke/Documents/Learning Python/') # insert at 1, 0 is the script path (or '' in REPL)
import LukeLibrary as lib

import noise
# help(noise)
# noise2(x, y, octaves=1, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=0.0)

import pygame
import random
import math

screenW = 700
screenH = 700
screen = pygame.display.set_mode((screenW, screenH))

cols = 50
rows = 50

flowField = [
    [
        0.0 for _ in range(cols)
    ] for _ in range(rows)
]

xOffset = random.randint(0, 1000)
yOffset = random.randint(0, 1000)

for r in range(rows):
    for c in range(cols):
        x = (c * 0.03) + xOffset
        y = (r * -0.03) + yOffset

        theta = noise.snoise2(x, y)
        theta = lib.mapToRange(theta)
        theta *= (math.pi * 4.0)
        flowField[r][c] = theta


class Vehicle:
    def __init__(self, id_):
        self.id = id_

        x = random.randint(0, screenW)
        y = random.randint(0, screenH)
        self.position = lib.Vector(x, y)

        self.radius = random.randint(10, 20)

        # dir = lib.randomFloat(0.0, math.pi * 2.0)
        self.velocity = lib.Vector() # .fromAngle(dir)
        # self.minSpeed = lib.randomFloat(0.0, 0.1)
        # self.maxSpeed = lib.randomFloat(1.0, 1.5)
        self.minSpeed = 0.0
        self.maxSpeed = 10.0 / (self.radius ** 1.2)
    
    def display(self):
        x = int(self.position.x)
        y = int(self.position.y)
        dir = self.velocity.heading()
        rad = self.radius
        # pygame.draw.circle(
        #     screen, (100, 100, 100),
        #     (x, y),
        #     rad, 1
        # )
        pygame.draw.polygon(
            screen, (0, 0, 0),
            (
                (
                    x + (math.cos(dir) * rad),
                    y + (math.sin(dir) * rad)
                ),
                (
                    x + (math.cos(dir + (math.pi * 0.8)) * rad),
                    y + (math.sin(dir + (math.pi * 0.8)) * rad)
                ),
                (x, y),
                (
                    x + (math.cos(dir - (math.pi * 0.8)) * rad),
                    y + (math.sin(dir - (math.pi * 0.8)) * rad)
                )
            )
        )
        
    
    def flow(self):
        if lib.isBetween(self.position.x, 0, screenW) and lib.isBetween(self.position.y, 0, screenH):
            curCol = int(self.position.x / (screenW / cols))
            curRow = int(self.position.y / (screenH / rows))
            flowVel = lib.Vector().fromAngle(flowField[curRow][curCol])
            flowVel.mult(0.01)
            self.velocity.add(flowVel)

    def repel(self):
        for Veh in Population:
            if Veh.id == self.id: continue
            dist = self.position.distance(Veh.position)
            radSum = (self.radius * 0.8) + (Veh.radius * 0.8)
            if dist < radSum:
                dx = Veh.position.x - self.position.x
                dy = Veh.position.y - self.position.y
                vecToNeighbour = lib.Vector(dx, dy)
                vecToNeighbour.normalise()

                sizeRatio = Veh.radius / self.radius

                vecToNeighbour.mult(-sizeRatio / 10.0)
                self.velocity.add(vecToNeighbour)

    def move(self):
        self.velocity.limit(self.minSpeed, self.maxSpeed)
        self.position.add(self.velocity)
    
    def edges(self):
        if self.position.x > screenW + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = screenW + self.radius
        
        if self.position.y > screenH + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = screenH + self.radius
    
    def update(self):
        self.flow()
        self.repel()
        self.move()
        self.edges()
        self.display()
Population = [Vehicle(i) for i in range(10)]


def drawFlowField():
    w = (screenW / cols) * 0.45
    h = (screenH / rows) * 0.45

    for r in range(rows):
        for c in range(cols):
            x = int( (c+0.5) * (screenW / cols) )
            y = int( (r+0.5) * (screenH / rows) )
            theta = flowField[r][c]
            pygame.draw.circle(
                screen, (200, 200, 200),
                (x, y), 2, 1
            )

            pygame.draw.line(
                screen, (150, 150, 150),
                (x, y),
                (
                    x + (math.cos(theta) * int(w)),
                    y + (math.sin(theta) * int(h))
                ), 2
            )

            pygame.draw.line(
                screen, (200, 200, 200),
                (x-w, 0),
                (x-w, screenH),
                1
            )
            pygame.draw.line(
                screen, (200, 200, 200),
                (0, y-h),
                (screenW, y-h),
                1
            )



while(True):
    screen.fill((255, 255, 255))

    drawFlowField()

    for Veh in Population:
        Veh.update()


    pygame.display.flip()

