
import pygame

canvasW, canvasH = (400, 600)
canvas = pygame.display.set_mode((canvasW, canvasH))

Anchors = [
    (canvasW * 0.2, canvasH * 0.8),
    (canvasW * 0.2, canvasH * 0.2),
    (canvasW * 0.8, canvasH * 0.2),
    (canvasW * 0.8, canvasH * 0.8)
]
AnchorMoving = [False for _ in range(4)]
dragDistance = 8

PathWidth = 30
SampleCount = 50

def calculatePathPoints():
    def interp(start, end, T):
        return (
            start[0] + (T * (end[0] - start[0]) / SampleCount),
            start[1] + (T * (end[1] - start[1]) / SampleCount)
        )
    
    points = []
    for T in range(SampleCount + 1):
        current_ab = interp(Anchors[0], Anchors[1], T)
        current_bc = interp(Anchors[1], Anchors[2], T)
        current_cd = interp(Anchors[2], Anchors[3], T)

        current_ab_bc = interp(current_ab, current_bc, T)
        current_bc_cd = interp(current_bc, current_cd, T)

        current_P = interp(current_ab_bc, current_bc_cd, T)
        # points.append(current_P)

        next_ab = interp(Anchors[0], Anchors[1], T+1)
        next_bc = interp(Anchors[1], Anchors[2], T+1)
        next_cd = interp(Anchors[2], Anchors[3], T+1)

        next_ab_bc = interp(next_ab, next_bc, T+1)
        next_bc_cd = interp(next_bc, next_cd, T+1)

        next_P = interp(next_ab_bc, next_bc_cd, T+1)

        dx = next_P[0] - current_P[0]
        dy = next_P[1] - current_P[1]
        h = ((dx**2)+(dy**2))**0.5

        # normal = (dy, -dx)
        points.append((current_P[0] + (PathWidth*dy/h), current_P[1] - (PathWidth*dx/h)))
        points.append((current_P[0] - (PathWidth*dy/h), current_P[1] + (PathWidth*dx/h)))
    return points
PathwayPoints = calculatePathPoints()

mx, my = (-1, -1)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, (Ax, Ay) in enumerate(Anchors):
                dx = Ax - mx
                dy = Ay - my
                if ((dx**2)+(dy**2))**0.5 <= dragDistance:
                    AnchorMoving[i] = True
                    break
        
        if ev.type == pygame.MOUSEMOTION:
            for i in range(4):
                if AnchorMoving[i]: Anchors[i] = pygame.mouse.get_pos()
        
        if ev.type == pygame.MOUSEBUTTONUP:
            AnchorMoving = [False for _ in range(4)]
            PathwayPoints = calculatePathPoints()
    
    canvas.fill((255,255,255))

    for Ax, Ay in Anchors:
        Ax, Ay = int(Ax), int(Ay)
        # pygame.draw.circle(canvas, (0,0,0), (Ax, Ay), dragDistance, 1)
        x1 = Ax - (dragDistance * 0.5 * (2**0.5))
        y1 = Ay - (dragDistance * 0.5 * (2**0.5))
        x2 = Ax + (dragDistance * 0.5 * (2**0.5))
        y2 = Ay + (dragDistance * 0.5 * (2**0.5))
        pygame.draw.line(canvas,(0,0,0),(x1,y1),(x2,y2),1)
        pygame.draw.line(canvas,(0,0,0),(x2,y1),(x1,y2),1)
    
    for i in range(SampleCount*2):
        x1 = int(PathwayPoints[i][0])
        y1 = int(PathwayPoints[i][1])
        x2 = int(PathwayPoints[i+2][0])
        y2 = int(PathwayPoints[i+2][1])
        pygame.draw.line(canvas, (0,0,0), (x1,y1), (x2,y2), 1)

    # for pt in PathwayPoints:
    #     pygame.draw.circle(canvas, (0,0,200), (int(pt[0]), int(pt[1])), 2, 0)

    pygame.display.update()