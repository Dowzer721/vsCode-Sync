
from math import cos, sin, pi
import pygame
from random import randint

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from closestPointOnLine import getClosestPointAlongLine

canvasW, canvasH = 600, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def toInt(self):
        return int(self.x), int(self.y), int(self.z)
    
    @staticmethod
    def random(xMin, xMax, yMin, yMax):
        return Vector(
            randint(int(xMin), int(xMax)),
            randint(int(yMin), int(yMax))
        )


a = Vector.random(canvasW * 0.1, canvasW * 0.9, canvasH * 0.1, canvasH * 0.9)
b = Vector.random(canvasW * 0.1, canvasW * 0.9, canvasH * 0.1, canvasH * 0.9)
m = Vector()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        elif event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    canvas.fill((255, 255, 255))

    pygame.display.flip()