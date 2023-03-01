
from math import atan2, cos, sin

import pygame

canvasW, canvasH = 800, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

A = (int(canvasW * 0.2), int(canvasH * 0.2))
Ac = (255, 100, 100)

B = (int(canvasW * 0.7), int(canvasH * 0.8))
Bc = (100, 255, 100)

AB_dx = A[0] - B[0]
AB_dy = A[1] - B[1]
AB_angle = atan2(AB_dy, AB_dx)

C = (int(canvasW * 0.4), int(canvasH * 0.2))
Cc = (100, 100, 255)


firstLoop = True
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP or firstLoop:
            if not firstLoop:
                C = pygame.mouse.get_pos()

            AC_dx = C[0] - A[0]
            AC_dy = C[1] - A[1]
            AC_dist = int( ((AC_dx**2)+(AC_dy**2))**0.5 )

            BC_dx = C[0] - B[0]
            BC_dy = C[1] - B[1]
            BC_dist = int( ((BC_dx**2)+(BC_dy**2))**0.5 )
            BC_angle = atan2(BC_dy, BC_dx)
            # BC_toward = (int( B[0] + (cos(BC_angle) * BC_dist * 0.75) ), int( B[1] + (sin(BC_angle) * BC_dist * 0.75) ) )

            AC_BC_angle_d = AB_angle - BC_angle
            BC_flip = (int( B[0] + (cos(AB_angle + (AC_BC_angle_d)) * BC_dist ) ), int( B[1] + (sin(AB_angle + (AC_BC_angle_d)) * BC_dist) ))

            C_closest = (
                (C[0] + BC_flip[0]) // 2,
                (C[1] + BC_flip[1]) // 2
            )

            firstLoop = False
        
        
    canvas.fill((100,100,100))

    pygame.draw.circle(canvas, Ac, A, 4, 0)
    #pygame.draw.circle(canvas, Ac, A, AC_dist, 1)

    pygame.draw.circle(canvas, Bc, B, 4, 0)
    #pygame.draw.circle(canvas, Bc, B, BC_dist, 1)

    # pygame.draw.line(canvas, Bc, B, BC_toward, 1)
    # pygame.draw.line(canvas, Bc, B, BC_flip, 1)
    #pygame.draw.circle(canvas, Cc, BC_flip, 4, 0)

    pygame.draw.line(canvas, (200,200,200), A, B, 2)
    pygame.draw.circle(canvas, Cc, C, 4, 0)

    pygame.draw.circle(canvas, (200,200,200), C_closest, 4, 0)

    pygame.draw.line(canvas, (200,200,200), C, C_closest, 1)
    
    pygame.display.flip()