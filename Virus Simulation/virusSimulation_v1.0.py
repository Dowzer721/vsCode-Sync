
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin, atan2

from random import randint

import pygame
canvasW, canvasH = 600, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

populationSize = 1
individualRadius = 8
infectionRadius = int(individualRadius * 1.5)

class Individual:
    def __init__(self):
        self.pos = LL.Vector(randint(0, canvasW), randint(0, canvasH))
        self.vel = LL.Vector.fromAngle(LL.randomFloat(0.0, pi * 2.0))
        self.vel.mult(0.1)

        self.infected = False
        self.dead = False
    
    def move(self):
        self.pos.add(self.vel)
        if self.pos.x < -individualRadius:
            self.pos.x = canvasW + individualRadius
        elif self.pos.x > canvasW + individualRadius:
            self.pos.x = -individualRadius

        if self.pos.y < -individualRadius:
            self.pos.y = canvasH + individualRadius
        elif self.pos.y > canvasH + individualRadius:
            self.pos.y = -individualRadius
        
    
    def render(self):

        renderColour = (0, 200, 0)
        if self.infected: renderColour = (200, 0, 0)
        if self.dead: renderColour = (0, 0, 0)

        x, y, _ = self.pos.toInt()
        pygame.draw.circle(
            canvas, renderColour,
            (x, y), individualRadius,
            0
        )

Population = [Individual() for _ in range(populationSize)]

# Population[0].vel.set(0, 1)
# Population[0].steer()

while True:
    canvas.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pass
            # x, y = pygame.mouse.get_pos()
            # Population[0].pos.set(x, y)

    for i in Population:
        i.steer()
        i.move()
        i.render()

    pygame.display.flip()