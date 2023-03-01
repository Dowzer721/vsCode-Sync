
from math import pi, cos, sin
from random import random
import pygame

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
from LukeLibrary import closestPointOnLine

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

class PathSegment:
    def __init__(self, start_, end_):
        self.start = start_
        self.end = end_
    def render(self, renderColour=(100,100,100), renderThickness=4):
        x1, y1 = int(self.start[0]), int(self.start[1])
        x2, y2 = int(self.end[0]), int(self.end[1])
        pygame.draw.line(canvas, renderColour, (x1,y1), (x2,y2), renderThickness)

Path = []
def newPath():
    numberOfCorners = 8
    corners = []
    for c in range(numberOfCorners):
        angle = 2 * pi * c / numberOfCorners
        x = (canvasW*0.5) + (cos(angle) * canvasW * random() * 0.5)
        y = (canvasH*0.5) + (sin(angle) * canvasH * random() * 0.5)
        corners.append((x,y))

    Path.clear()
    for i in range(numberOfCorners):
        Path.append(PathSegment(corners[i], corners[(i+1)%numberOfCorners]))
newPath()

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            newPath()

    canvas.fill((255,255,255))

    C = (int(canvasW * 0.9), int(canvasH * 0.6))
    pt = closestPointOnLine(Path[0].start, Path[0].end, C)
    pygame.draw.circle(canvas, (0,255,0), C, 4, 0)
    pygame.draw.circle(canvas, (0,0,255), pt, 4, 0)

    for Segment in Path:
        Segment.render()

    pygame.display.flip()