
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

rocketRadius = 10
rocketSpeed = 0.1
rocketRenderSettings = [
    (math.pi * 0.0, rocketRadius * 1.0),
    (math.pi * 0.8, rocketRadius * 0.8),
    (math.pi * 1.0, rocketRadius * 0.5),
    (math.pi * 1.2, rocketRadius * 0.8)
]

targetPosition = (screenW * 0.2, screenH * 0.1)
targetRadius = rocketRadius * 1.5

def heading(tup):
    return math.atan2(tup[1], tup[0])
def tupleFromAngle(angle, mag = 1.0):
    x = math.cos(angle) * mag
    y = math.sin(angle) * mag
    return (x, y)

class Boundary:
    def __init__(self, start_, end_):
        self.start = start_
        self.end = end_
    def render(self, colour=(200, 50, 50), thickness=2):
        pygame.draw.line(
            screen, colour,
            (int(self.start[0]), int(self.start[1])),
            (int(self.end[0]), int(self.end[1])),
            thickness
        )

class Obstacle:
    def __init__(self, *pointList):
        self.boundaries = [
            Boundary(pointList[i], pointList[(i+1)%len(pointList)]) for i in range(0, len(pointList))
        ]

    def render(self):
        for b in self.boundaries:
            b.render()
obs = Obstacle(
    (screenW * 0.01, screenH * 0.01),
    (screenW * 0.99, screenH * 0.01),
    (screenW * 0.99, screenH * 0.99),
    (screenW * 0.01, screenH * 0.99),
    (screenW * 0.01, screenH * 0.30),
    (screenW * 0.60, screenH * 0.30),
    (screenW * 0.60, screenH * 0.20),
    (screenW * 0.01, screenH * 0.20))

class Rocket:
    def __init__(self):
        self.position = (screenW / 2, screenH - (rocketRadius * 1.2))

        self.velocityAngles = []
        for _ in range(0, 100):
            dir = LL.degreesToRadians(random.randint(180, 360))
            self.velocityAngles.append(dir)

        self.velocity = tupleFromAngle(self.velocityAngles[0], rocketSpeed)
        
        self.boundaries = [Boundary((0, 0), (0, 0)) for _ in range(0, len(rocketRenderSettings))]
        self.updateBoundaries()

        self.dead = False
    def move(self):
        self.position = tuple(sum(x) for x in zip(self.position, self.velocity))

    def updateBoundaries(self):
        dir = heading(self.velocity)
        for i in range(0, len(rocketRenderSettings)):
            n = (i + 1) % len(rocketRenderSettings)
            self.boundaries[i].start = (
                self.position[0] + (math.cos(dir + rocketRenderSettings[i][0]) * rocketRenderSettings[i][1]),
                self.position[1] + (math.sin(dir + rocketRenderSettings[i][0]) * rocketRenderSettings[i][1])
            )
            self.boundaries[i].end = (
                self.position[0] + (math.cos(dir + rocketRenderSettings[n][0]) * rocketRenderSettings[n][1]),
                self.position[1] + (math.sin(dir + rocketRenderSettings[n][0]) * rocketRenderSettings[n][1])
            )
    
    def checkCollision(self):
        for selfBoundary in self.boundaries:
            for obstacleBoundary in obs.boundaries:
                if LL.LineLineIntersection(selfBoundary.start, selfBoundary.end, obstacleBoundary.start, obstacleBoundary.end) != -1:
                    self.dead = True
                    return
    
    def render(self):
        for b in self.boundaries:
            b.render((0, 0, 0), 1)
    
    def update(self):
        if self.dead == False:
            self.move()
            self.updateBoundaries()
            self.checkCollision()
        self.render()

# rkt = Rocket(0)
Population = [
    Rocket() for _ in range(0, 20)
]

while(True):
    screen.fill((255, 255, 255))

    pygame.draw.circle(
        screen, (100, 255, 100),
        (int(targetPosition[0]), int(targetPosition[1])), int(targetRadius), 0
    )

    obs.render()

    for rocket in Population:
        rocket.update()

    pygame.display.flip()