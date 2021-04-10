
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import pygame
screenW, screenH = (600, 400)
screen = pygame.display.set_mode((screenW, screenH))

global terrainPoints
def generateTerrain():
    global terrainPoints

    pointCount = int(screenW / 1)
    terrainNoise = LL.generate1DNoise(pointCount, smoothCount=int(pointCount * 5))
    terrainPoints = [(0, screenH)]

    for x in range(screenW):
        i = x % pointCount
        y = terrainNoise[i] * screenH
        terrainPoints.append((x, y))
    
    terrainPoints.append((screenW, screenH))

generateTerrain()

while(True):
    screen.fill((255, 255, 255))

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP:
            generateTerrain()
    
    mouseX, _ = pygame.mouse.get_pos()
    pygame.draw.line(
        screen, (0, 0, 200),
        (mouseX, 0),
        (mouseX, terrainPoints[mouseX][1]),
        1
    )

    pygame.draw.polygon(
        screen, (0, 0, 0),
        terrainPoints,
        1
    )

    # for x in range(screenW):
    #     terrainHeight = terrainNoise[x % len(terrainNoise)]
    #     y1 = screenH
    #     y2 = screenH * terrainHeight
    #     pygame.draw.line(
    #         screen, (0, 0, 0),
    #         (x, y1),
    #         (x, y2),
    #         1
    #     )

    pygame.display.flip()