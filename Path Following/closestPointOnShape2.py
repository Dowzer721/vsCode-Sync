
"""
This program no longer contains any of the code. 
I have moved over all of the required code to LukeLibrary, so that it can be called from any other program.
"""

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# import LukeLibrary as LL
from LukeLibrary import closestPointOnShape

import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("closestPointOnShape2")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

vertices = [
    (int(canvasW * 0.1), int(canvasH * 0.1)),
    (int(canvasW * 0.9), int(canvasH * 0.1)),
    (int(canvasW * 0.8), int(canvasH * 0.7)),
    (int(canvasW * 0.9), int(canvasH * 0.9)),
    (int(canvasW * 0.1), int(canvasH * 0.9)),
]
vertexCount = len(vertices)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    cP = closestPointOnShape(vertices, pygame.mouse.get_pos())
    canvas.fill(WHITE)
    
    for c in range(vertexCount):
        n = (c + 1) % vertexCount

        start, end = vertices[c], vertices[n]
        pygame.draw.line(canvas, BLACK, start, end, 1)
    
    pygame.draw.circle(canvas, RED, cP, 8, 0)
    
    pygame.display.update()