
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin
import pygame

screenW, screenH = (600, 400)
screen = pygame.display.set_mode((screenW, screenH))

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def render(self, colour=(0,0,0), thickness=1):
        x1, y1, _ = self.start.toInt()
        x2, y2, _ = self.end.toInt()
        pygame.draw.line(
            screen, colour,
            (x1, y1), (x2, y2),
            thickness
        )

roomCorners = [
    (screenW * 0.1, screenH * 0.1), # Top left corner

    (screenW * 0.4, screenH * 0.1), # Top left top-alcove corner
    (screenW * 0.4, screenH * 0.2), # Bottom left top-alcove corner
    (screenW * 0.6, screenH * 0.2), # Bottom right top-alcove corner
    (screenW * 0.6, screenH * 0.1), # Top right top-alcove corner
    
    (screenW * 0.9, screenH * 0.1), # Top right corner
    (screenW * 0.9, screenH * 0.9), # Bottom right corner
    (screenW * 0.1, screenH * 0.9)  # Bottom left corner
]
cornerCount = len(roomCorners)

Walls = []
for c in range(cornerCount):
    n = (c+1) % cornerCount
    start = LL.Vector(roomCorners[c][0], roomCorners[c][1])
    end = LL.Vector(roomCorners[n][0], roomCorners[n][1])

    Walls.append(Wall(start, end))


while(True):
    screen.fill((255, 255, 255))

    for w in Walls:
        w.render()
    
    pygame.display.flip()