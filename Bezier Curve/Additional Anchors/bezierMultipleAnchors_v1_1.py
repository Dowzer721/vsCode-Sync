
import pygame

canvasW, canvasH = 900, 600
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("Click to add new Anchor, Click and Drag to move Anchors, 'Delete' to delete last Anchor, 'Bottom Left' to toggle 'ShowAnchor'.")

Anchors = []
AnchorCount = 0
AnchorsMoving = []
AnchorRenderRadius = 4
AnchorDragRadius = int(AnchorRenderRadius * 1.75)
ShowAnchors = True

ShowAnchorsBox = [(0, canvasH*0.95), (canvasW*0.05, canvasH*0.95), (canvasW*0.05, canvasH), (0, canvasH)]

BezierPoints = []
interpolationSteps = 1000

def interpolateBetween(start, end, interpolationAmount):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    return (start[0] + (dx * interpolationAmount), start[1] + (dy * interpolationAmount))

def findInterpolationPoints(previousAnchors=None, T=0, layer=0):
    if previousAnchors == None: previousAnchors = [A for A in Anchors]
    if len(previousAnchors) == 0: return []
    if layer == AnchorCount-1: return previousAnchors

    return findInterpolationPoints(
        [interpolateBetween(previousAnchors[AnchorIndex], previousAnchors[AnchorIndex+1], T)
        for AnchorIndex in range(len(previousAnchors)-1)], 
        
        T, 
        layer+1
    )

def generateBezierPoints():
    BezierPoints.clear()
    # BezierPoints = []
    for T in range(interpolationSteps+1):
        BezierPoints.extend(findInterpolationPoints(T=T/interpolationSteps))


while True:
    canvas.fill((255,255,255))

    # previousAnchorCount = AnchorCount

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            if (mx <= ShowAnchorsBox[1][0]) and (my >= ShowAnchorsBox[0][1]):
                ShowAnchors ^= True
                break
            
            for i, (Ax,Ay) in enumerate(Anchors):
                dx,dy = Ax - mx, Ay - my
                dist = ((dx**2)+(dy**2))**0.5
                if dist <= AnchorDragRadius:
                    AnchorsMoving[i] = True
                    break
            else:
                Anchors.append((mx,my))
                AnchorsMoving.append(False)

        if ev.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            # if ShowAnchors and AnchorCount>1:
            #     pygame.draw.line(canvas, (0,0,0), Anchors[-1], mousePosition, 1)
            #     pygame.draw.line(canvas, (0,0,0), Anchors[-2], mousePosition, 1)


            for i in range(AnchorCount):
                if AnchorsMoving[i]: 
                    Anchors[i] = mousePosition
                    generateBezierPoints()
                
        if ev.type == pygame.MOUSEBUTTONUP:
            AnchorsMoving = [False for _ in range(AnchorCount)]
            generateBezierPoints()
        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_DELETE:
                Anchors = Anchors[:-1]
                AnchorCount = len(Anchors)
                generateBezierPoints()
    
    # for Ax, Ay in Anchors:
    #     pygame.draw.circle(canvas, (0,0,0), (int(Ax), int(Ay)), AnchorRenderRadius, 0)
    #     pygame.draw.circle(canvas, (200,200,200), (int(Ax), int(Ay)), AnchorDragRadius, 1)
    
    
    AnchorCount = len(Anchors)
    # if previousAnchorCount != AnchorCount: print(AnchorCount)

    for i in range(AnchorCount):
        # if previousAnchorCount != AnchorCount: print(i)
        
        if ShowAnchors:
            x1, y1 = int(Anchors[i][0]), int(Anchors[i][1])
            pygame.draw.circle(canvas, (0,0,0), (x1, y1), AnchorRenderRadius, 0)
            # pygame.draw.circle(canvas, (200,200,200), (x1, y1), AnchorDragRadius, 1)

            if i < AnchorCount-1:
                x2, y2 = int(Anchors[i+1][0]), int(Anchors[i+1][1])
                pygame.draw.line(canvas, (0,0,0), (x1, y1), (x2, y2), 1)
    
    for Bx, By in BezierPoints:
        # pygame.draw.circle(canvas, (100,100,100), (int(Bx), int(By)), 4, 0)
        pygame.draw.circle(canvas, (0,0,0), (int(Bx), int(By)), 1, 0)
    
    pygame.draw.polygon(canvas, (200,200,200), ShowAnchorsBox, 0)

    
    pygame.display.update()