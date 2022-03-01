
# Inspired by the work of Daniel Shiffman @ The Coding Train (YouTube)


import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import pygame
canvasW, canvasH = 700, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

from Vehicle import Vehicle
v = Vehicle(LL.Vector(200, 200), vel_=0.1)

vehicleRadius = 8

from Path import PathSection

# pathRadius = 20
pathPoints = [
    ( int(canvasW * 0.1), int(canvasH * 0.1) ),
    ( int(canvasW * 0.5), int(canvasH * 0.3) ),
    ( int(canvasW * 0.8), int(canvasH * 0.2) ),
    ( int(canvasW * 0.8), int(canvasH * 0.8) ),
    ( int(canvasW * 0.2), int(canvasH * 0.7) )
]
numberOfPathPoints = len(pathPoints)


# pathPointReachDistance = vehicleRadius * 2

# coefficients = [
#     LL.LineCoefficientsFromTwoPoints(
#         pathPoints[i],
#         pathPoints[(i+1)%numberOfPathPoints]
#     )
#     for i in range(numberOfPathPoints)
# ]

Paths = []
for i in range(numberOfPathPoints):
    start = pathPoints[i]
    end = pathPoints[(i + 1) % numberOfPathPoints]
    Paths.append(PathSection(start, end))

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    canvas.fill((255, 255, 255))
    
    # findTarget(self, canvas, currentPath, nextPath, numberOfPathPoints, distanceAhead=100)
    v.findTarget(canvas, Paths[v.seekingIndex], Paths[(v.seekingIndex+1)%numberOfPathPoints], numberOfPathPoints)
    v.steerToSeekPoint()
    v.move()
        
    
    for P in Paths:
        P.render(canvas)
    for P in Paths:
        P.render(canvas, renderMid=True)

    v.render(canvas)

    pygame.display.flip()


# lineStart = (50, 300) # (50, 50)
# lineEnd = (350, 50) # (350, 300)

# a, b, c = LL.LineCoefficientsFromTwoPoints(lineStart, lineEnd)

# P = (0, 0)


# while True:
#     for ev in pygame.event.get():
#         if ev.type == pygame.QUIT:
#             pygame.quit()
#             exit(0)
        
#         if ev.type == pygame.MOUSEMOTION:
#             P = pygame.mouse.get_pos()
    
#     canvas.fill((255, 255, 255))

#     pygame.draw.line(
#         canvas, (0,0,0),
#         lineStart,
#         lineEnd, 1
#     )

#     pygame.draw.circle(canvas, (0,0,0), P, 8, 0)

#     cX = int( (b * (b*P[0] - a*P[1]) - a*c) / (a**2 + b**2) )
#     cY = int( (a * (-b*P[0] + a*P[1]) - b*c) / (a**2 + b**2) )

#     # cX = max(lineStart[0], min(cX, lineEnd[0]))
#     # cY = max(lineStart[1], min(cY, lineEnd[1]))

#     pygame.draw.circle(
#         canvas, (255, 0, 0),
#         (cX, cY), 8, 0
#     )

#     dx = cX - P[0]
#     dy = cY - P[1]
#     d = ((dx**2)+(dy**2))**0.5

#     if d > 1:
#         pygame.draw.circle(canvas, (100,100,100), P, int(d), 1)







#     pygame.display.flip()