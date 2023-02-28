
from math import atan2, pi, sin, cos, asin

def findCrossPoints(circleA_x, circleA_y, circleA_radius, circleB_x, circleB_y, circleB_radius):
    AB_dx = circleB_x - circleA_x
    AB_dy = circleB_y - circleA_y
    AB_dist = ((AB_dx**2) + (AB_dy**2)) ** 0.5
    if AB_dist > (circleA_radius + circleB_radius): return False
    
    AB_theta= atan2(AB_dy, AB_dx)
    a = asin(((AB_dist/2) * sin(pi/2)) / circleA_radius )
    b = pi - ((pi/2) + a)

    xr = (circleA_radius * sin(b)) / sin(pi/2)

    # averageRadius = (circleA_radius + circleB_radius) / 2
    averageRadius = ((AB_dist - circleA_radius) + (AB_dist - circleB_radius)) / 2

    # return [
    #     (circleA_x + (cos(AB_theta) * AB_dist / 2) + (cos(AB_theta - (pi/2)) * xr),
    #      circleA_y + (sin(AB_theta) * AB_dist / 2) + (sin(AB_theta - (pi/2)) * xr) ),
    #     (circleA_x + (cos(AB_theta) * AB_dist / 2) + (cos(AB_theta + (pi/2)) * xr),
    #      circleA_y + (sin(AB_theta) * AB_dist / 2) + (sin(AB_theta + (pi/2)) * xr) )
    # ]

    return [
        (circleA_x + (cos(AB_theta) * averageRadius) + (cos(AB_theta - (pi/2)) * xr),
         circleA_y + (sin(AB_theta) * averageRadius) + (sin(AB_theta - (pi/2)) * xr) ),
        (circleA_x + (cos(AB_theta) * averageRadius) + (cos(AB_theta + (pi/2)) * xr),
         circleA_y + (sin(AB_theta) * averageRadius) + (sin(AB_theta + (pi/2)) * xr) )
    ]

import pygame

canvasW, canvasH = 400, 600
canvas = pygame.display.set_mode((canvasW, canvasH))

circleA_x = int(canvasW * 0.5)
circleA_y = int(canvasH * 0.7)
circleA_r = int(min(canvasW, canvasH) * 0.3)

circleB_r = int(circleA_r * 0.4)

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    canvas.fill((200,200,200))

    circleB_x, circleB_y = pygame.mouse.get_pos()

    crossoverPoints = findCrossPoints(circleA_x, circleA_y, circleA_r, circleB_x, circleB_y, circleB_r)
    if crossoverPoints:
        crossX1, crossY1 = crossoverPoints[0]
        crossX2, crossY2 = crossoverPoints[1]
        pygame.draw.circle(canvas, (200,0,0), (int(crossX1), int(crossY1)), 4, 0)
        pygame.draw.circle(canvas, (200,0,0), (int(crossX2), int(crossY2)), 4, 0)
    
    pygame.draw.circle(canvas, (0,0,0), (circleA_x, circleA_y), circleA_r, 2)
    pygame.draw.circle(canvas, (0,200,0), (circleB_x, circleB_y), circleB_r, 2)

    pygame.draw.line(canvas, (200,200,0),
        (circleA_x, circleA_y),
        (circleB_x, circleB_y),
        2
    )

    # radRatio = circleB_r / circleA_r
    # avgX = int( (circleA_x + circleB_x) / radRatio )
    # avgY = int( (circleA_y + circleB_y) / radRatio )
    AB_dx = circleB_x - circleA_x
    AB_dy = circleB_y - circleA_y
    AB_dist = ((AB_dx**2) + (AB_dy**2)) ** 0.5
    if AB_dist <= (circleA_r + circleB_r):
        AB_theta= atan2(AB_dy, AB_dx)

        avg1X = circleA_x + (cos(AB_theta) * circleA_r)
        avg1Y = circleA_y + (sin(AB_theta) * circleA_r)
        avg2X = circleB_x + (cos(AB_theta+pi) * circleB_r)
        avg2Y = circleB_y + (sin(AB_theta+pi) * circleB_r)

        avgX = (avg1X + avg2X) / 2
        avgY = (avg1Y + avg2Y) / 2
        
        pygame.draw.circle(canvas, (0,0,200), (int(avg1X), int(avg1Y)), 4, 0)
        pygame.draw.circle(canvas, (0,0,200), (int(avg2X), int(avg2Y)), 4, 0)
        pygame.draw.circle(canvas, (0,0,200), (int(avgX), int(avgY)), 4, 0)
    
    pygame.display.flip()