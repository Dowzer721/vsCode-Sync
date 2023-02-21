
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

    return [
        (circleA_x + (cos(AB_theta) * AB_dist / 2) + (cos(AB_theta - (pi/2)) * xr),
         circleA_y + (sin(AB_theta) * AB_dist / 2) + (sin(AB_theta - (pi/2)) * xr) ),
        (circleA_x + (cos(AB_theta) * AB_dist / 2) + (cos(AB_theta + (pi/2)) * xr),
         circleA_y + (sin(AB_theta) * AB_dist / 2) + (sin(AB_theta + (pi/2)) * xr) )
    ]

# import pygame

# canvasW, canvasH = 400, 600
# canvas = pygame.display.set_mode((canvasW, canvasH))

# circleA_x = int(canvasW * 0.5)
# circleA_y = int(canvasH * 0.7)
# circleRadius = int(min(canvasW, canvasH) * 0.3)

# running = True
# while running:
#     for ev in pygame.event.get():
#         if ev.type == pygame.QUIT:
#             pygame.quit()
#             exit(0)

#     canvas.fill((200,200,200))

#     circleB_x, circleB_y = pygame.mouse.get_pos()

#     circleAB_dx = circleB_x - circleA_x
#     circleAB_dy = circleB_y - circleA_y
#     circleAB_dist = ((circleAB_dx**2) + (circleAB_dy**2)) ** 0.5
#     circleAB_theta = atan2(circleAB_dy, circleAB_dx)

#     if circleAB_dist < (circleRadius*2):
#         a = asin(((circleAB_dist/2) * sin(pi/2)) / circleRadius)
#         b = pi - (pi/2 + a)
#         xr = (circleRadius * sin(b)) / sin(pi/2)

#         crossX1 = circleA_x + (cos(circleAB_theta) * circleAB_dist / 2) + (cos(circleAB_theta - (pi/2)) * xr)
#         crossY1 = circleA_y + (sin(circleAB_theta) * circleAB_dist / 2) + (sin(circleAB_theta - (pi/2)) * xr)
#         pygame.draw.circle(canvas, (200,0,0), (int(crossX1), int(crossY1)), 4, 0)

#         crossX2 = circleA_x + (cos(circleAB_theta) * circleAB_dist / 2) + (cos(circleAB_theta + (pi/2)) * xr)
#         crossY2 = circleA_y + (sin(circleAB_theta) * circleAB_dist / 2) + (sin(circleAB_theta + (pi/2)) * xr)
#         pygame.draw.circle(canvas, (200,0,0), (int(crossX2), int(crossY2)), 4, 0)
    
#     pygame.draw.circle(canvas, (0,0,0), (circleA_x, circleA_y), circleRadius, 2)
#     pygame.draw.circle(canvas, (0,200,0), (circleB_x, circleB_y), circleRadius, 2)
    
#     pygame.display.flip()