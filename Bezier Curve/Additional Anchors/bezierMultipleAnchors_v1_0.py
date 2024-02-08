
import pygame

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

Anchors = [
    # (canvasW * 0.1, canvasH * 0.1),
    # (canvasW * 0.1, canvasH * 0.9),
    # (canvasW * 0.9, canvasH * 0.9),
    # (canvasW * 0.9, canvasH * 0.1)
]
AnchorCount = len(Anchors)

interpolationSteps = 100
def interpolateBetween(start, end, T):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return (start[0] + (dx * T), start[1] + (dy * T))

def findInterpolationPoints(previousAnchors=Anchors, T=0, layer=0):
    if len(previousAnchors) == 0: return []
    interpolationPoints = [
        interpolateBetween(previousAnchors[AnchorIndex], previousAnchors[AnchorIndex+1], T)
        for AnchorIndex in range(len(previousAnchors)-1)
    ]
    
    if layer == AnchorCount-1: return previousAnchors

    return findInterpolationPoints(interpolationPoints, T, layer+1)

def setBezierPoints():
    points = []
    for T in range(interpolationSteps+1):
        points.extend(findInterpolationPoints(T=T/interpolationSteps))
    return points
points = setBezierPoints()

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            Anchors.append(pygame.mouse.get_pos())
            AnchorCount += 1
            points = setBezierPoints()
    
    canvas.fill((255,255,255))

    for c in range(AnchorCount-1):
        pygame.draw.line(canvas, (0,0,0), Anchors[c], Anchors[c+1], 1)

    for Ax,Ay in Anchors:
        pygame.draw.circle(canvas, (0,0,0), (int(Ax), int(Ay)), 8, 0)
    
    for ptx,pty in points:
        pygame.draw.circle(canvas, (0,200,0), (int(ptx), int(pty)), 4, 0)

    pygame.display.update()