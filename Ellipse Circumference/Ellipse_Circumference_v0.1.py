
# Check against:
# https://www.google.com/search?q=circumference+of+an+ellipse

import pygame
import math
import time

pygame.display.init()

screenW = 600
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

closingTime = 5

ellipseW = int(screenW * 0.8)
ellipseH = int(screenH * 0.7)

# if ellipseW==ellipseH:
#     print(2.0 * math.pi * ellipseW * 0.5)

segmentCount = 10**5 # The higher this number, the longer the process will take, but the more accurate it will be.

# while(True):
screen.fill((255, 255, 255))
pygame.draw.circle(
    screen, (200, 0, 0),
    (int(screenW/2), int(screenH/2)),
    2, 0
)

# ellipseRectLeft = (screenW / 2) - (ellipseW / 2)
# ellipseRectTop  = (screenH / 2) - (ellipseH / 2)

pygame.draw.ellipse(
    screen, (200, 0, 0), 
    pygame.Rect(
        (screenW / 2) - (ellipseW / 2),
        (screenH / 2) - (ellipseH / 2),
        ellipseW, 
        ellipseH
    ), 
    1
)


totalDist = 0.0
for i in range(0, segmentCount):
    iTheta = ((math.pi * 2.0) / segmentCount) * i
    x1 = (screenW / 2) + (math.cos(iTheta) * (ellipseW / 2))
    y1 = (screenH / 2) + (math.sin(iTheta) * (ellipseH / 2))

    n = (i + 1) % segmentCount
    nTheta = ((math.pi * 2.0) / segmentCount) * n
    x2 = (screenW / 2) + (math.cos(nTheta) * (ellipseW / 2))
    y2 = (screenH / 2) + (math.sin(nTheta) * (ellipseH / 2))

    pygame.draw.line(
        screen, (0, 0, 0),
        (x1, y1), (x2, y2),
        1
    )

    dx = x1 - x2
    dy = y1 - y2
    totalDist += math.sqrt(dx**2 + dy**2)
pygame.display.flip()


print(
    f"Using {segmentCount} segments, " +
    f"estimated circumference = {round(totalDist, 5)}. \n" +
    f"Closing in {closingTime} seconds..."
)

time.sleep(closingTime)