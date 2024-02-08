import os
import pathlib
import pygame

canvasW, canvasH = 700, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("Bezier Track Driving")



# customAnchorPoints = [
#     [(0.11,0.26),   (0.24,0.09),    (0.48,0.04),    (0.52,0.07)],
#     [(0.52,0.07),   (0.59,0.14),    (0.31,0.37),    (0.34,0.62)],
#     [(0.34,0.62),   (0.36,0.83),    (0.62,0.49),    (0.78,0.68)],
#     [(0.78,0.68),   (0.94,0.89),    (0.81,0.00),    (0.91,0.09)],
#     [(0.91,0.09),   (0.97,0.14),    (0.99,0.97),    (0.90,0.90)],
#     [(0.90,0.90),   (0.70,0.75),    (0.28,0.95),    (0.19,0.77)],
#     [(0.19,0.77),   (0.02,0.41),    (0.06,0.35),    (0.11,0.26)]
# ]
customAnchorPoints = [
    [(0.11,0.26),(0.24,0.09),(0.88,0.5),(0.77,0.59)],
    [(0.77,0.59),(0.49,0.78),(0.15,0.12),(0.15,0.42)],
    [(0.15,0.42),(0.18,0.81),(0.75,0.69),(0.79,0.72)],
    [(0.79,0.72),(0.93,0.83),(0.81,0.0),(0.91,0.09)],
    [(0.91,0.09),(0.97,0.14),(0.99,0.97),(0.9,0.9)],
    [(0.9,0.9),(0.7,0.75),(0.28,0.95),(0.19,0.77)],
    [(0.19,0.77),(0.02,0.41),(0.06,0.35),(0.11,0.26)]
]
TrackAnchors = [
    [(customAnchorPoints[i][a][0] * canvasW, customAnchorPoints[i][a][1] * canvasH) for a in range(4)]
    for i in range(len(customAnchorPoints))
]
# print(TrackAnchors)

TCount = 100

def dxdyh(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    return dx, dy, h

def calculateBezierPoints(Anchors):
    A, B, C, D = Anchors
    
    def interp(A, B, T):
        dx, dy, _ = dxdyh(A, B)
        return (A[0] + (T*dx/TCount), A[1] + (T*dy/TCount))
    
    points = []
    for T in range(-1, TCount + 2):
        AB = interp(A, B, T)
        BC = interp(B, C, T)
        CD = interp(C, D, T)
        AB_BC = interp(AB, BC, T)
        BC_CD = interp(BC, CD, T)
        BezierPoints = interp(AB_BC, BC_CD, T)
        points.append(
            (int(BezierPoints[0]), int(BezierPoints[1]))
        )
    return points

TrackPoints = []

for AnchorSet in TrackAnchors:
    TrackPoints.extend(calculateBezierPoints(AnchorSet))

# print(TrackPoints)

# blackSquareIcon = pygame.Surface((32,32))

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
    # allKeys = pygame.key.get_pressed()
    # if allKeys[pygame.K_ESCAPE]: pass
    
    canvas.fill((255,255,255))

    for pt in TrackPoints:
        pygame.draw.circle(canvas, (0,0,200), pt, 8, 0)
    
    pygame.display.update()

    
    