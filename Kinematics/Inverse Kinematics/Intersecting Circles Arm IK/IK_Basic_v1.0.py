
from math import pi, cos, sin, atan2, asin

import pygame

canvasW, canvasH = 400, 600
canvas = pygame.display.set_mode((canvasW, canvasH))

baseLocation = (canvasW*0.5, canvasH*0.9)

armLength = canvasH * 1.2
segmentCount = 10
segmentLength = armLength / segmentCount
# print(segmentLength)
jointMovementSpeed = 0.001

targetLocation = (int(canvasW * 0.8), int(canvasH * 0.4))

arm = []
class Segment:
    def __init__(self, index_=0):
        self.index = index_

        self.start = list(baseLocation)
        self.jointAngle = 0

        # self.end = [
        #     self.start[0] + (cos(self.jointAngle) * segmentLength),
        #     self.start[1] + (sin(self.jointAngle) * segmentLength)
        # ]
        self.end = [0,0]
        # self.updateEnd()

        # self.generateNextSegment()
    
    # def generateNextSegment(self):
    #     if self.index >= segmentCount - 1: return
    #     arm.append(Segment(self.index + 1, self.end, self.jointAngle + 0.1))
    
    def updateEnd(self):
        totalAngle = arm[0].jointAngle
        for segmentIndex in range(1, self.index+1):
            totalAngle += arm[segmentIndex].jointAngle

        self.end = [
            self.start[0] + (cos(totalAngle) * segmentLength),
            self.start[1] + (sin(totalAngle) * segmentLength)
        ]
        if self.index < segmentCount - 1:
            arm[self.index + 1].start = self.end
            # arm[self.index + 1].updateEnd()

    def render(self, renderColour=(0,0,0), renderThickness=1):
        x1, y1 = int(self.start[0]), int(self.start[1])
        # pygame.draw.circle(canvas, renderColour, (x1, y1), int(renderThickness * 2), 0)

        x2, y2 = int(self.end[0]), int(self.end[1])
        pygame.draw.line(canvas, renderColour,
            (x1, y1), (x2, y2),
            renderThickness
        )

        # pygame.draw.circle(canvas, (200, 200, 200), (x1, y1), int(segmentLength), 2)

for i in range(segmentCount):
    arm.append(Segment(i))
arm[0].jointAngle = 3 * pi / 2

def armAngleBeforeSegment(segmentIndex):
    return sum([arm[i].jointAngle for i in range(segmentIndex)])

def moveArm():
    # print(f"Targetting: x{targetX}, y{targetY}")

    for seg in arm:
        if seg.index == segmentCount-1:
            seg.jointAngle = atan2(targetLocation[1] - seg.start[1], targetLocation[0] - seg.start[0]) - armAngleBeforeSegment(segmentCount-1) #+ (pi/2)
            seg.updateEnd()
            # print(seg.jointAngle)
            continue

        endDx = targetLocation[0] - seg.end[0]
        endDy = targetLocation[1] - seg.end[1]
        endDist = ((endDx**2)+(endDy**2))**0.5

        startDx = targetLocation[0] - seg.start[0]
        startDy = targetLocation[1] - seg.start[1]
        startDist = ((startDx**2)+(startDy**2))**0.5
        #print(startDist)

        if (endDist <= segmentLength) or (startDist <= segmentLength*2):
            
            startAngle = atan2(startDy, startDx)
            
            eq = ((startDist / 2) * sin(pi/2)) / segmentLength
            a = 0
            try:
                a = asin(eq)
            except:
                pass
                # print(f"startDist: {round(startDist, 2)}, Error: {round(eq, 2)}")
                # pygame.quit()
                # exit(0)

            b = pi - ((pi/2) + a)
            xr = (segmentLength * sin(b)) / sin(pi/2)
            cPt1 = ( # crossoverPoint
                seg.start[0] + (cos(startAngle) * startDist / 2) + (cos(startAngle-(pi/2)) * xr),
                seg.start[1] + (sin(startAngle) * startDist / 2) + (sin(startAngle-(pi/2)) * xr)
            )
            cPt2 = ( # crossoverPoint
                seg.start[0] + (cos(startAngle) * startDist / 2) + (cos(startAngle+(pi/2)) * xr),
                seg.start[1] + (sin(startAngle) * startDist / 2) + (sin(startAngle+(pi/2)) * xr)
            )
            # return cPt

            # Which crossoverPoint is closer:
            cpt1dx = seg.end[0]-cPt1[0]
            cpt1dy = seg.end[1]-cPt1[1]
            cpt1Dist = ((cpt1dx**2)+(cpt1dy**2))**0.5
            cpt2dx = seg.end[0]-cPt2[0]
            cpt2dy = seg.end[1]-cPt2[1]
            cpt2Dist = ((cpt2dx**2)+(cpt2dy**2))**0.5
            tgtX, tgtY = cPt1
            if cpt2Dist<cpt1Dist:
                tgtX, tgtY = cPt2
            
            tgtX = seg.end[0] + ((tgtX - seg.end[0])*jointMovementSpeed)
            tgtY = seg.end[1] + ((tgtY - seg.end[1])*jointMovementSpeed)

            # # pygame.draw.circle(canvas, (0, 255, 0), (int(cPt[0]), int(cPt[1])), 4, 0)
            angleToCPT = atan2(tgtY - seg.start[1], tgtX - seg.start[0]) - armAngleBeforeSegment(seg.index) # - (pi / 2)
            seg.jointAngle = angleToCPT
            seg.updateEnd()

    # return (0,0)

mx, my = 0, 0
running = True
while running:
    canvas.fill((255, 255, 255))
    # mx, my = pygame.mouse.get_pos()
    
    targetLocation = pygame.mouse.get_pos()
    moveArm()
    #pygame.draw.circle(canvas, (0,0,0), (int(cpt[0]), int(cpt[1])), 4, 0)
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            pass
            # targetLocation = pygame.mouse.get_pos()
    
    # baseAngle = atan2(my - baseLocation[1], mx - baseLocation[0])
    for seg in arm:
        seg.updateEnd()
    
    # pygame.draw.circle(canvas, (100, 200, 100), targetLocation, 8, 0)
    # pygame.draw.circle(canvas, (200, 255, 200), targetLocation, int(segmentLength), 4)

    for armSegment in arm:
        armSegment.render(renderThickness=segmentCount - armSegment.index)
    
    pygame.display.flip()