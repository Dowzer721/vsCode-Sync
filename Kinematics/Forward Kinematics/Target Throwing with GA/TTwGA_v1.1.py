
from math import pi, cos, sin
import pygame
from random import randint

canvasW, canvasH = 600, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

def rf(min_=0.0, max_=1.0, dp_=2):
    rng = max_ - min_
    pct = randint(0, 10 ** dp_) / float(10 ** dp_)
    return round(min_ + (rng * pct), dp_)

segmentCount = 16
angles = [rf(pi*0.05, pi*0.45) for _ in range(segmentCount)]
segmentLength = (min(canvasW, canvasH) * 0.9) / segmentCount

print(f"N: {segmentCount}, L: {segmentLength}")

basePosition = (0, 0)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    canvas.fill((255, 255, 255))

    endEffectorPosition = list(basePosition)
    for i in range(segmentCount):

        # pygame.draw.circle(
        #     canvas, 
        #     (0,0,0), 
        #     (int(endEffectorPosition[0]), int(endEffectorPosition[1])), 
        #     4, 
        #     0
        # )

        x = cos(angles[i]) * segmentLength
        y = sin(angles[i]) * segmentLength

        pygame.draw.line(
            canvas, 
            (0,0,0), 
            (
                int(endEffectorPosition[0]),
                int(endEffectorPosition[1])
            ),
            (
                # int(endEffectorPosition[0] + (x * 0.9)),
                # int(endEffectorPosition[1] + (y * 0.9))
                int(endEffectorPosition[0] + x),
                int(endEffectorPosition[1] + y)
            ), 
            1
        )

        endEffectorPosition[0] += x
        endEffectorPosition[1] += y
    
    pygame.draw.circle(
        canvas, 
        (0,0,0), 
        (
            int(endEffectorPosition[0]),
            int(endEffectorPosition[1])
        ), 
        4, 
        0
    )
    
    pygame.display.flip()