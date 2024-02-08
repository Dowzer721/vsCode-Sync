
import pygame

canvasW, canvasH = 800, 600
canvas = pygame.display.set_mode((canvasW, canvasH))

Anchors = [
    (canvasW * 0.2, canvasH * 0.8),
    (canvasW * 0.4, canvasH * 0.2),
    (canvasW * 0.6, canvasH * 0.2),
    (canvasW * 0.8, canvasH * 0.8)
]
AnchorMoving = [False for _ in range(4)]
dragDistance = 20

drawAnchor = lambda x,y: pygame.draw.circle(canvas,(0,0,200),(int(x), int(y)), dragDistance, 1)
drawPoint = lambda x,y,c=(0,0,0),r=4: pygame.draw.circle(canvas,c,(int(x), int(y)), r, 0)

SampleCount = 50

def interp(start, end, T):
    return (
        start[0] + (T * (end[0]-start[0]) / SampleCount),
        start[1] + (T * (end[1]-start[1]) / SampleCount)
    )

def calculateBezierPoints():
    ab = [interp(Anchors[0], Anchors[1], T) for T in range(SampleCount+1)]
    bc = [interp(Anchors[1], Anchors[2], T) for T in range(SampleCount+1)]
    cd = [interp(Anchors[2], Anchors[3], T) for T in range(SampleCount+1)]

    ab_bc = [interp(ab[T], bc[T], T) for T in range(SampleCount+1)]
    bc_cd = [interp(bc[T], cd[T], T) for T in range(SampleCount+1)]

    B = [interp(ab_bc[T], bc_cd[T], T) for T in range(SampleCount+1)]
    return ab, bc, cd, ab_bc, bc_cd, B

interp_ab, interp_bc, interp_cd, interp_ab_bc, interp_bc_cd, BezierPoints = calculateBezierPoints()

frame = 0
animationTickFrame = 100
animationFrame = 0
animationFrameMax = SampleCount


while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for i, (Ax, Ay) in enumerate(Anchors):
                if (((Ax - mx)**2)+((Ay - my)**2))**0.5 <= dragDistance:
                    AnchorMoving[i] = True
                    break
        
        if ev.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            for i in range(4):
                if AnchorMoving[i]: 
                    Anchors[i] = mousePosition
                    interp_ab, interp_bc, interp_cd, interp_ab_bc, interp_bc_cd, BezierPoints = calculateBezierPoints()
                    break
        
        if ev.type == pygame.MOUSEBUTTONUP:
            AnchorMoving = [False for _ in range(4)]
    
    frame += 1
    if frame >= animationTickFrame:
        frame = 0
        animationFrame = (animationFrame + 1) % animationFrameMax

    canvas.fill((255,255,255))

    for A in Anchors:
        drawAnchor(*A)
    pygame.draw.line(canvas, (0,0,0), Anchors[0], Anchors[1], 1)
    pygame.draw.line(canvas, (0,0,0), Anchors[1], Anchors[2], 1)
    pygame.draw.line(canvas, (0,0,0), Anchors[2], Anchors[3], 1)

    # _=[drawPoint(x,y,r=2) for x,y in interp_ab]
    # _=[drawPoint(x,y,r=2) for x,y in interp_bc]
    # _=[drawPoint(x,y,r=2) for x,y in interp_cd]
    # _=[drawPoint(x,y,r=3) for x,y in interp_ab_bc]
    # _=[drawPoint(x,y,r=3) for x,y in interp_bc_cd]
    # _=[drawPoint(x,y,r=4) for x,y in BezierPoints]

    for i in range(SampleCount):
        x1, y1 = interp_ab_bc[i]
        x2, y2 = interp_ab_bc[i+1]
        pygame.draw.line(canvas, (0,0,0), (int(x1), int(y1)), (int(x2), int(y2)), 1)

        x3, y3 = interp_bc_cd[i]
        x4, y4 = interp_bc_cd[i+1]
        pygame.draw.line(canvas, (0,0,0), (int(x3), int(y3)), (int(x4), int(y4)), 1)

        x5, y5 = BezierPoints[i]
        x6, y6 = BezierPoints[i+1]
        pygame.draw.line(canvas, (0,0,0), (int(x5), int(y5)), (int(x6), int(y6)), 1)

    animationInterpPoints = [
        interp_ab[animationFrame],
        interp_bc[animationFrame],
        interp_cd[animationFrame],
        interp_ab_bc[animationFrame],
        interp_bc_cd[animationFrame],
        BezierPoints[animationFrame]
    ]

    for x,y in animationInterpPoints[:-1]:
        drawPoint(x, y, (200,0,0), 8)
    drawPoint(*animationInterpPoints[-1], (0,200,0), 8)
    
    pygame.draw.line(canvas, (200,0,0), animationInterpPoints[0], animationInterpPoints[1], 1) # ab_bc
    pygame.draw.line(canvas, (200,0,0), animationInterpPoints[1], animationInterpPoints[2], 1) # bc_cd
    
    pygame.draw.line(canvas, (200,0,0), animationInterpPoints[3], animationInterpPoints[4], 1) # B
    
    pygame.display.update()