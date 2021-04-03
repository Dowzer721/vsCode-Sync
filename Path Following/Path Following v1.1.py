
import math
import pygame
import random

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))

def randomFloat(min = 0.0, max = 0.0):
    rng = max - min
    pct = random.randint(0, 1000) / 1000.0
    return min + (rng * pct)

class Vector:
    def __init__(self, x_=0.0, y_=0.0):
        self.x = x_
        self.y = y_
    def fromAngle(self, angle):
        x = math.cos(angle)
        y = math.sin(angle)
        return Vector(x, y)
    def copy(self):
        return Vector(self.x, self.y)
    # ----
    # def add(self, vecA, vecB = 0):
    #     if vecB.x + vecB.y != 0.0:
    #         x = vecA.x + vecB.x
    #         y = vecA.y + vecB.y
    #         return Vector(x, y)
    #     else:
    #         self.x += vecA.x
    #         self.y += vecB.x
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
    def mult(self, val):
        self.x *= val
        self.y *= val
    # ---
    def heading(self):
        return math.atan2(self.y, self.x)


vehicleCount = 1
radius = 20
class Individual:
    def __init__(self):
        x = random.randint(0, screenW)
        y = random.randint(0, screenH)
        self.position = Vector(x, y)
        
        dir = randomFloat(0, math.pi * 2.0)
        self.velocity = Vector().fromAngle(dir)

        self.minSpeed = randomFloat(0.0, 0.1)
        self.maxSpeed = randomFloat(self.minSpeed, 1.0)
    def move(self):
        self.position.add(self.velocity)
    def edges(self):
        if self.position.x < -radius:
            self.position.x = screenW + radius
        elif self.position.x > screenW + radius:
            self.position.x = -radius
        if self.position.y < -radius:
            self.position.y = screenH + radius
        elif self.position.y > screenH + radius:
            self.position.y = -radius
    def display(self):
        dir = self.velocity.heading()
        x = int(self.position.x)
        y = int(self.position.y)

        pygame.draw.polygon(
            screen, (0, 0, 0),
            (
                (
                    x + (math.cos(dir) * radius),
                    y + (math.sin(dir) * radius)
                ),
                (
                    x + (math.cos(dir + (math.pi * 0.8)) * radius),
                    y + (math.sin(dir + (math.pi * 0.8)) * radius)
                ),
                (x, y),
                (
                    x + (math.cos(dir - (math.pi * 0.8)) * radius),
                    y + (math.sin(dir - (math.pi * 0.8)) * radius)
                )
            ), 1
        )
        pygame.draw.line(
            screen, (0, 0, 0),
            (x, y),
            (
                x + (math.cos(dir) * radius),
                y + (math.sin(dir) * radius)
            )
        )
    def update(self):
        self.move()
        self.edges()
        self.display()


Population = [Individual() for _ in range(vehicleCount)]

while(True):
    screen.fill((255, 255, 255))

    for Ind in Population:
        Ind.update()
    
    pygame.display.flip()