import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import pygame
pygame.display.init()

screenW = 600
screenH = 400
screen = pygame.display.set_mode((screenW, screenH))

import math
import random

class Boundary:
    def __init__(self, start_=LL.Vector(50, 50), end_=LL.Vector()):
        self.start = start_
        self.end = end_
    def set(self, newS, newE):
        self.start = newS
        self.end = newE
    def render(self, col=(200, 50, 50), thickness=1):
        pygame.draw.line(
            screen, col,
            (int(self.start.x), int(self.start.y)),
            (int(self.end.x), int(self.end.y)),
            thickness
        )
screenBoundaries = [
    Boundary(LL.Vector(0, 0),               LL.Vector(screenW, 0)),
    Boundary(LL.Vector(screenW, 0),         LL.Vector(screenW, screenH)),
    Boundary(LL.Vector(screenW, screenH),   LL.Vector(0, screenH)),
    Boundary(LL.Vector(0, screenH),         LL.Vector(0, 0))
]

class Obstacle:
    def __init__(self, center, width, height):
        self.center = center
        self.left = center.x - (width / 2)
        self.right = center.x + (width / 2)
        self.top = center.y - (height / 2)
        self.bottom = center.y + (height / 2)

        self.walls = []
        centerOffsetMultiplier = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for i in range(0, 4):
            n = (i + 1) % 4
            x1 = center.x + ((width / 2) * centerOffsetMultiplier[i][0])
            y1 = center.y + ((height/ 2) * centerOffsetMultiplier[i][1])
            x2 = center.x + ((width / 2) * centerOffsetMultiplier[n][0])
            y2 = center.y + ((height/ 2) * centerOffsetMultiplier[n][1])

            start = LL.Vector(x1, y1)
            end = LL.Vector(x2, y2)
            self.walls.append(Boundary(start, end))
    def render(self):
        
        vertices = [
            (int(self.walls[i].start.x), int(self.walls[i].start.y))
                for i in range(0, 4)
        ]

        pygame.draw.polygon(
            screen, (200, 50, 50),
            vertices, 0
        )
BlockingObstacle = Obstacle(LL.Vector(screenW * 0.35, screenH/3), screenW * 0.7, screenH * 0.1)

directionCount = 16
populationSize = 10
rocketRadius = min([screenW, screenH]) * 0.05
rocketRenderAngles = [
    0,
    LL.degreesToRadians(160),
    math.pi,
    LL.degreesToRadians(200)
]
rocketRenderRadii = [
    rocketRadius,
    rocketRadius * 0.9,
    rocketRadius * 0.5,
    rocketRadius * 0.9
]

targetRadius = rocketRadius * 0.8
targetPosition = LL.Vector(LL.randomFloat(screenW * 0.1, BlockingObstacle.center.x - targetRadius), screenH * LL.randomFloat(0.1, 0.2))

targetObstacleIntersectionDistance = 0.0
furthestIntersectionPoint = LL.Vector()
n = 1000
for i in range(0, n):
    angle = (math.pi/2) - (((math.pi/2) / n) * i)
    x1 = targetPosition.x
    y1 = targetPosition.y
    x2 = x1 + (math.cos(angle) * screenW * screenH)
    y2 = y1 + (math.sin(angle) * screenW * screenH)
    
    x3 = BlockingObstacle.walls[0].start.x
    y3 = BlockingObstacle.walls[0].start.y
    x4 = BlockingObstacle.walls[1].start.x
    y4 = BlockingObstacle.walls[1].start.y

    intersectionPoint = LL.LineLineIntersection(targetPosition, LL.Vector(x2, y2), BlockingObstacle.walls[0].start, BlockingObstacle.walls[0].end)
    if intersectionPoint == -1:
        continue

    dist = targetPosition.distance(intersectionPoint)
    if dist > targetObstacleIntersectionDistance:
        targetObstacleIntersectionDistance = dist
        furthestIntersectionPoint = intersectionPoint

class Rocket:
    def __init__(self, startPos):
        self.position = startPos # LL.Vector
        
        self.steeringDirections = [
            LL.Vector().fromAngle(LL.randomFloat(math.pi * 0.9, math.pi * 2.1, 5))
                for _ in range(0, directionCount)
        ]
        print(self.steeringDirections[0].heading())
        self.velocity = self.steeringDirections[0]
        self.distanceCovered = 0.0
        self.dead = False

        self.boundaries = [Boundary() for _ in range(0, 4)]
        self.updateBoundaries()

    def move(self):

        self.velocity.add(self.steeringDirections[0])
        self.velocity.normalise(0.1)
        self.position.add(self.velocity)
        self.distanceCovered += (self.velocity.getMag() * int(not self.dead))
    
    def updateBoundaries(self):
        dir = self.velocity.heading()
        for i in range(0, 4):
            n = (i + 1) % 4
            x1 = self.position.x + (math.cos(dir + rocketRenderAngles[i]) * rocketRenderRadii[i])
            y1 = self.position.y + (math.sin(dir + rocketRenderAngles[i]) * rocketRenderRadii[i])
            x2 = self.position.x + (math.cos(dir + rocketRenderAngles[n]) * rocketRenderRadii[n])
            y2 = self.position.y + (math.sin(dir + rocketRenderAngles[n]) * rocketRenderRadii[n])
            # print("x1:%.1f, y1:%.1f, x2:%.1f, y2:%.1f" %(x1, y1, x2, y2))
            self.boundaries[i].set(LL.Vector(x1, y1), LL.Vector(x2, y2))
    
    def checkObstacleCollision(self):
        for i in range(0, 4):

            x1 = self.boundaries[i].start.x
            y1 = self.boundaries[i].start.y
            x2 = self.boundaries[i].end.x
            y2 = self.boundaries[i].end.y

            for w in BlockingObstacle.walls:
                x3 = w.start.x
                y3 = w.start.y
                x4 = w.end.x
                y4 = w.end.y

                denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
                if denominator == 0.0:
                    continue

                t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
                u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

                if (t > 0.0) and (t < 1.0) and (u > 0.0) and (u < 1.0):
                    self.dead = True
                    return
            
            for b in screenBoundaries:
                x3 = b.start.x
                y3 = b.start.y
                x4 = b.end.x
                y4 = b.end.y

                denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
                if denominator == 0.0:
                    continue

                t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
                u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

                if (t > 0.0) and (t < 1.0) and (u > 0.0) and (u < 1.0):
                    self.dead = True
                    return
    
    def render(self):

        dir = self.velocity.heading()
        for i in range(0, 4):
            n = (i + 1) % 4
            x1 = int(self.position.x + (math.cos(dir + rocketRenderAngles[i]) * rocketRenderRadii[i]))
            y1 = int(self.position.y + (math.sin(dir + rocketRenderAngles[i]) * rocketRenderRadii[i]))
            x2 = int(self.position.x + (math.cos(dir + rocketRenderAngles[n]) * rocketRenderRadii[n]))
            y2 = int(self.position.y + (math.sin(dir + rocketRenderAngles[n]) * rocketRenderRadii[n]))

            pygame.draw.line(
                screen, (100, 100, 100),
                (x1, y1), (x2, y2), 2
            )

        for B in self.boundaries:
            B.render((0, 0, 0), 1)

        if self.dead:
            pygame.draw.circle(
                screen, (255, 50, 50),
                (int(self.position.x), int(self.position.y)),
                int(rocketRadius * 0.25), 0
            )

    def update(self):
        if not self.dead:
            self.move()
            self.updateBoundaries()
            self.checkObstacleCollision()
        self.render()

Population = []
for i in range(0, populationSize):
    x = screenW * 0.5 # (screenW / (populationSize - 1)) * i
    y = screenH - rocketRadius
    Population.append(Rocket(LL.Vector(x, y)))
    # if i == 0:
    #     for b in range(0, 4):
    #         print(Population[i].boundaries[b].end.x)

def distanceFromPositionToTarget(position):
    dx = position.x - BlockingObstacle.right.x
    dy = position.y - BlockingObstacle.center.y
    dist = math.sqrt(dx^2 + dy^2)
    if position.y > BlockingObstacle.center.y:
        dx = BlockingObstacle.right.x - targetPosition.x
        dy = BlockingObstacle.center.y - targetPosition.y
        dist += math.sqrt(dx^2 + dy^2)
    return dist 

while(True):
    screen.fill((255, 255, 255))
    for b in screenBoundaries:
        b.render(thickness=4)

    BlockingObstacle.render()

    x = int(furthestIntersectionPoint.x)
    y = int(furthestIntersectionPoint.y)
    pygame.draw.circle(
        screen, (50, 50, 255),
        (x, y), 3
    )

    pygame.draw.circle(
        screen, (150, 255, 150),
        (int(targetPosition.x), int(targetPosition.y)),
        int(targetRadius), 0
    )


    for R in Population:
        R.update()

    pygame.display.flip()
