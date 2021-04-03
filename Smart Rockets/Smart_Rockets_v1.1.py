
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import math
import pygame
import random

pygame.display.init()
screenW = 600
screenH = 400
screen = pygame.display.set_mode((screenW, screenH))

rocketRadius = 20
rocketSpeed = 0.1
rocketStartPosition = LL.Vector(screenW * 0.5, screenH - (rocketRadius * 1.5))

# (rocketCornerAngle, rocketCornerRadius)
rocketCornerSettings = [
    (math.pi * 0.0, rocketRadius * 1.00),
    (math.pi * 0.8, rocketRadius * 0.75),
    (math.pi * 1.0, rocketRadius * 0.25),
    (math.pi * 1.2, rocketRadius * 0.75)
]

populationSize = 10
mutationChance = 0.2

targetRadius = rocketRadius * 1.2
targetPosition = (int(screenW * LL.randomFloat(0.1, 0.4)), int(LL.randomFloat(targetRadius, (screenH * 0.2)-targetRadius)))

rocketVelocityAngleCount = 4 # int(LL.Vector(targetPosition[0], targetPosition[1]).distance(rocketStartPosition) / rocketSpeed)
print(rocketVelocityAngleCount)

# ---

class Boundary:
    def __init__(self, startPosition, endPosition):
        self.start = startPosition 
        self.end = endPosition
    def render(self, colour=(255, 100, 100), thickness=2):
        pygame.draw.line(
            screen, colour,
            (self.start[0], self.start[1]), (self.end[0], self.end[1]),
            thickness
        )

class Obstacle:
    def __init__(self, points):
        self.corners = points
        self.boundaries = []
        for i in range(0, len(points)):
            n = (i + 1) % len(points)
            start = (points[i][0], points[i][1])
            end   = (points[n][0], points[n][1])
            self.boundaries.append(Boundary(start, end))

    def render(self, colour=(200, 50, 50), thickness=0):
        pygame.draw.polygon(
            screen, colour,
            self.corners,
            thickness
        )
        for b in self.boundaries:
            b.render()

obs = Obstacle([
    (screenW * 0.01, screenH * 0.01),
    (screenW * 0.99, screenH * 0.01),
    (screenW * 0.99, screenH * 0.99),
    (screenW * 0.01, screenH * 0.99),
    (screenW * 0.01, screenH * 0.30),
    (screenW * 0.60, screenH * 0.30),
    (screenW * 0.60, screenH * 0.20),
    (screenW * 0.01, screenH * 0.20)])

class Rocket:
    def __init__(self, id):
        self.id = id
        self.position = rocketStartPosition
        # self.position.x = (screenW / (populationSize-1)) * id
        self.velocityAngles = [
            LL.randomFloat(math.pi * 0.9, math.pi * 2.1)
                for _ in range(0, rocketVelocityAngleCount)
        ]
        # dir = LL.randomFloat(math.pi * 0.9, math.pi * 2.1)
        dir = LL.randomFloat(math.pi * 0.0, math.pi * 2.0)
        
        self.velocity = LL.Vector().fromAngle(dir)
        # self.velocity.setMag(0.1)

        self.shapeBoundaries = [Boundary((0, 0), (0, 0)) for _ in range(0, 4)]
        # self.updateBoundaries()
        
        self.dead = False
    
    def move(self):
        self.position.add(self.velocity)
        
    def updateBoundaries(self):
        dir = self.velocity.heading()
        
        for i in range(0, 4):
            n = (i + 1) % 4
            self.shapeBoundaries[i].start = (
                self.position.x + (math.cos(dir + rocketCornerSettings[i][0]) * rocketCornerSettings[i][1]),
                self.position.y + (math.sin(dir + rocketCornerSettings[i][0]) * rocketCornerSettings[i][1])
            )
            self.shapeBoundaries[i].end = (
                self.position.x + (math.cos(dir + rocketCornerSettings[n][0]) * rocketCornerSettings[n][1]),
                self.position.y + (math.sin(dir + rocketCornerSettings[n][0]) * rocketCornerSettings[n][1])
            )

            print("%d: %.2f, %.2f" %(self.id, self.position.x, self.position.y))
    
    def checkCollision(self):
        for sB in self.shapeBoundaries:
            x1 = sB.start[0]
            y1 = sB.start[1]
            x2 = sB.end[0]
            y2 = sB.end[1]
            for oB in obs.boundaries:
                x3 = oB.start[0]
                y3 = oB.start[1]
                x4 = oB.end[0]
                y4 = oB.end[1]

                if LL.LineLineIntersection((x1, y1), (x2, y2), (x3, y3), (x4, y4)) != -1:
                    self.dead = True
                    return
    
    
    def render(self, colour=(0, 0, 0)):
        for b in self.shapeBoundaries:
            b.render(colour, 1)
        pygame.draw.circle(
            screen, (0, 0, 0),
            (int(self.position.x), int(self.position.y)),
            4, 0
        )

        # dir = self.velocity.heading()
        # x1 = int(self.position.x)
        # y1 = int(self.position.y)
        # x2 = int(x1 + (math.cos(dir) * rocketRadius * 2))
        # y2 = int(y1 + (math.sin(dir) * rocketRadius * 2))
        # pygame.draw.line(
        #     screen, (0, 0, 0),
        #     (x1, y1), (x2, y2),
        #     1
        # )
    
    def update(self):
        if self.dead == False:
            self.move()
            self.updateBoundaries()
            self.checkCollision()
            #pass
        self.render()

# I can't for the life of work out why, but the Rocket()'s within Population are interacting with each other, 
# even though they are not supposed to. I really am not sure as to why this is happening, and despite numerous 
# attempts to debug the situation step by step, I just can't figure it out.
            
    
Population = [Rocket(i) for i in range(0, populationSize)]
# print(Population[0].velocity.heading())
# print(Population[1].velocity.heading())
# print(Population[2].velocity.heading())
# input()

while(True):
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (150, 250, 150), targetPosition, int(targetRadius), 0)
    obs.render(thickness=1)
    
    for rkt in Population:
        rkt.update()

    pygame.display.flip()