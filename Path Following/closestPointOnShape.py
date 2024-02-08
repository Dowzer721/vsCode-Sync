
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
#import LukeLibrary as LL
from LukeLibrary import generate1DNoise, colours, closestPointOnShape

WHITE = colours["WHITE"]
BLACK = colours["BLACK"]
RED   = colours["RED"]

import pygame
pygame.init()

from math import pi, cos, sin

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("Click to generate new shape")

vertexCount = 64
midX, midY = canvasW/2, canvasH/2

def newNoise():
    newVertices = []
    vertexRadiusNoise = generate1DNoise(vertexCount, 0.01)
    # input(vertexRadiusNoise)
    for v in range(vertexCount):
        angle = 2 * pi * v / vertexCount
        
        newVertices.append(
            (int(midX + (cos(angle) * canvasW * vertexRadiusNoise[v])),
             int(midY + (sin(angle) * canvasH * vertexRadiusNoise[v])))
        )
    return newVertices
vertices = newNoise()


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            vertices = newNoise()

    canvas.fill(WHITE)
    for c in range(vertexCount):
        n = (c + 1) % vertexCount
        pygame.draw.line(canvas, BLACK, vertices[c], vertices[n], 1)

    mx, my = pygame.mouse.get_pos()
    cP = closestPointOnShape(vertices, (mx, my), True)
    pygame.draw.circle(canvas, RED, cP, 8, 0)

    pygame.display.update()