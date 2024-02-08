
import pygame

canvasW, canvasH = (900, 600)
canvas = pygame.display.set_mode((canvasW, canvasH))

SampleCount = 100

PathWidth = 10
dragDistance = int(PathWidth * 1.2)

PathSegments = []
class PathSegment:
    def __init__(self, start, end, closeEnds=False):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        anchor1Position = (
            max(dragDistance//2, min(start[0] + (dx/2) - (dy/4), canvasW-(dragDistance//2))),
            max(dragDistance//2, min(start[1] + (dy/2) + (dx/4), canvasH-(dragDistance//2)))
        )
        anchor2Position = (
            max(dragDistance//2, min(start[0] + (dx/2) + (dy/4), canvasW-(dragDistance//2))),
            max(dragDistance//2, min(start[1] + (dy/2) - (dx/4), canvasH-(dragDistance//2)))
        )

        self.Anchors = [start, anchor1Position, anchor2Position, end]
        self.AnchorMoving = [False for _ in range(4)]
        self.closeEnds = closeEnds
        self.renderAnchors = True
        self.SegmentPoints = []
        self.calculatePathPoints()
    def checkDrag(self, mousePosition):
        for i in range(4):
            dx = self.Anchors[i][0] - mousePosition[0]
            dy = self.Anchors[i][1] - mousePosition[1]
            if ((dx**2)+(dy**2))**0.5 <= dragDistance:
                self.AnchorMoving[i] = True
                return True
        return False
    def calculatePathPoints(self):
        def interp(start, end, T):
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            return (start[0] + (T * dx / SampleCount), start[1] + (T * dy / SampleCount))
        
        points = []
        for T in range(SampleCount+1):
            
            P0 = interp(
                interp(
                    interp(self.Anchors[0], self.Anchors[1], T), 
                    interp(self.Anchors[1], self.Anchors[2], T), 
                T), 
                interp(
                    interp(self.Anchors[1], self.Anchors[2], T), 
                    interp(self.Anchors[2], self.Anchors[3], T),
                T), 
            T)

            # points.append(P0)

            P1 = interp(
                interp(
                    interp(self.Anchors[0], self.Anchors[1], T+1), 
                    interp(self.Anchors[1], self.Anchors[2], T+1), 
                T+1), 
                interp(
                    interp(self.Anchors[1], self.Anchors[2], T+1), 
                    interp(self.Anchors[2], self.Anchors[3], T+1),
                T+1), 
            T+1)

            dx = P1[0] - P0[0]
            dy = P1[1] - P0[1]
            h = ((dx**2)+(dy**2))**0.5

            points.append( (P0[0] + (PathWidth*dy/h), P0[1] - (PathWidth*dx/h)) )
            points.append( (P0[0] - (PathWidth*dy/h), P0[1] + (PathWidth*dx/h)) )
        
        self.SegmentPoints = points
    
    def render(self):
        
        for Ax, Ay in self.Anchors:
            if self.renderAnchors:
                x1 = Ax - (dragDistance * 0.5 * (2**0.5))
                y1 = Ay - (dragDistance * 0.5 * (2**0.5))
                x2 = Ax + (dragDistance * 0.5 * (2**0.5))
                y2 = Ay + (dragDistance * 0.5 * (2**0.5))
                pygame.draw.line(canvas,(0,0,0),(x1,y1),(x2,y2),1)
                pygame.draw.line(canvas,(0,0,0),(x2,y1),(x1,y2),1)
            else:
                pass#pygame.draw.circle(canvas, (0,0,0), (int(Ax), int(Ay)), 1, 0)
        
        if self.renderAnchors:
            pygame.draw.line(canvas, (0,0,0), self.Anchors[0], self.Anchors[1], 1)
            pygame.draw.line(canvas, (0,0,0), self.Anchors[2], self.Anchors[3], 1)

        if self.closeEnds: 
            pygame.draw.line(canvas, (0,0,0), self.SegmentPoints[0], self.SegmentPoints[1], 1)
            pygame.draw.line(canvas, (0,0,0), self.SegmentPoints[-2], self.SegmentPoints[-1], 1)

        for i in range(len(self.SegmentPoints)-2):
            x1, y1 = self.SegmentPoints[i]
            # pygame.draw.circle(canvas,(0,0,200),(int(x1),int(y1)),4,0)
            x2, y2 = self.SegmentPoints[i+2]
            pygame.draw.line(canvas, (0,0,0), (int(x1), int(y1)), (int(x2), int(y2)), 1)
        
def resetPath():
    return [
        PathSegment((canvasW*0.1, canvasH*0.1), (canvasW*0.4, canvasH*0.1)),
        PathSegment((canvasW*0.4, canvasH*0.1), (canvasW*0.5, canvasH*0.4)),
        PathSegment((canvasW*0.5, canvasH*0.4), (canvasW*0.8, canvasH*0.1)),
        PathSegment((canvasW*0.6, canvasH*0.1), (canvasW*0.9, canvasH*0.1)),
        PathSegment((canvasW*0.9, canvasH*0.1), (canvasW*0.9, canvasH*0.9)),
        PathSegment((canvasW*0.9, canvasH*0.9), (canvasW*0.1, canvasH*0.9)),
        PathSegment((canvasW*0.1, canvasH*0.9), (canvasW*0.1, canvasH*0.1)),
    ]
PathSegments = resetPath()

def customPath():
    customAnchorPoints = [
        [(0.11,0.26),   (0.24,0.09),    (0.48,0.04),    (0.52,0.07)],
        [(0.52,0.07),   (0.59,0.14),    (0.31,0.37),    (0.34,0.62)],
        [(0.34,0.62),   (0.36,0.83),    (0.62,0.49),    (0.78,0.68)],
        [(0.78,0.68),   (0.94,0.89),    (0.81,0.0),     (0.91,0.09)],
        [(0.91,0.09),   (0.97,0.14),    (0.99,0.97),    (0.9,0.9)],
        [(0.9,0.9),     (0.7,0.75),     (0.28,0.95),    (0.19,0.77)],
        [(0.19,0.77),   (0.02,0.41),    (0.06,0.35),    (0.11,0.26)]
    ]

    for i in range(7):
        PathSegmentAnchors = []
        for x,y in customAnchorPoints[i]:
            PathSegmentAnchors.append((x*canvasW, y*canvasH))
        PathSegments[i].Anchors = PathSegmentAnchors

    for Seg in PathSegments:
        Seg.calculatePathPoints()

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            AnchorClicked = False
            for Seg in PathSegments:
                if Seg.checkDrag(mousePosition):
                    AnchorClicked = True
            if not AnchorClicked:
                for Seg in PathSegments:
                    Seg.renderAnchors ^= True

        
        if ev.type == pygame.MOUSEMOTION:
            mousePosition = pygame.mouse.get_pos()
            for Seg in PathSegments:
                for i in range(4):
                    if Seg.AnchorMoving[i]: 
                        Seg.Anchors[i] = mousePosition
                        Seg.calculatePathPoints()
                        break
        
        if ev.type == pygame.MOUSEBUTTONUP:
            for Seg in PathSegments:
                Seg.AnchorMoving = [False for _ in range(4)]
                #Seg.calculatePathPoints()
        
    allKeys = pygame.key.get_pressed()

    if allKeys[pygame.K_r]: PathSegments = resetPath()
    if allKeys[pygame.K_p]: 
        print("customAnchorPoints = [")
        for i, Seg in enumerate(PathSegments):
            Anchors = [(str(round(Ax/canvasW, 2)) + ',' + str(round(Ay/canvasH, 2))) for Ax, Ay in Seg.Anchors]
            print(f"    [({'),('.join(Anchors)})]", end='')
            finalChar = ',' if i < len(PathSegments)-1 else ''#\n'
            print(finalChar)

        print("]")
    if allKeys[pygame.K_c]: customPath()
    if allKeys[pygame.K_ESCAPE]: 
        pygame.quit()
        exit(0)
        
    canvas.fill((255,255,255))

    for Seg in PathSegments:
        Seg.render()
    
    pygame.display.update()
