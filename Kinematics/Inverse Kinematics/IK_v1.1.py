
from math import pi, cos, sin, atan2
from random import randint
def rF(min_=0.0, max_=1.0, dp_=2):
    rng = max_ - min_
    pct = randint(0, 10 ** dp_) / float(10 ** dp_)
    return min_ + (rng * pct)

import pygame
canvasW, canvasH = 900, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

class Tentacle:
    def __init__(self, *initArguments):
        # self.id, self.basePosition, self.segmentCount, finalLength = initArguments
        self.id, self.basePosition, self.segmentCount, self.segmentLength = initArguments
        # print(f"{self.id}- pos:{self.basePosition}, count:{self.segmentCount}, len:{self.segmentLength}")

        # finalLength = firstLength / self.segmentCount
        # finalLength /= self.segmentCount

        # self.segmentLengths = [(i+1) * finalLength for i in range(self.segmentCount)]
        self.starts = [[0,0] for _ in range(self.segmentCount)]
        self.ends = [[0,0] for _ in range(self.segmentCount)]

    def target(self, tX_, tY_):
        for s in range(self.segmentCount):
            if s == 0:
                x1, y1 = tX_, tY_
            else:
                x1 = self.starts[s-1][0]
                y1 = self.starts[s-1][1]
            
            dx = x1 - self.starts[s][0]
            dy = y1 - self.starts[s][1]
            theta = atan2(dy, dx)

            # self.starts[s] = [
            #     x1 + (cos(theta + pi) * self.segmentLengths[s]),
            #     y1 + (sin(theta + pi) * self.segmentLengths[s])
            # ]
            self.starts[s] = [
                x1 + (cos(theta + pi) * self.segmentLength),
                y1 + (sin(theta + pi) * self.segmentLength)
            ]
            self.ends[s] = [x1, y1]

        
        totalDx = self.starts[-1][0] - self.basePosition[0]
        totalDy = self.starts[-1][1] - self.basePosition[1]

        for s in range(self.segmentCount):
            self.starts[s][0] -= totalDx
            self.starts[s][1] -= totalDy
            self.ends[s][0] -= totalDx
            self.ends[s][1] -= totalDy
    
    def render(self):
        for s in range(self.segmentCount):
            x1 = int(self.starts[s][0])
            y1 = int(self.starts[s][1])
            x2 = int(self.ends[s][0])
            y2 = int(self.ends[s][1])
            pygame.draw.line(
                canvas, 
                (0, 0, 0), 
                (x1, y1), 
                (x2, y2), 
                s + 1
            )

    

tentacleCount = 8
segmentCount = 4
segmentLength = (min(canvasW, canvasH) * 0.8) / segmentCount
tentacles = []
for i in range(tentacleCount):
    # angle = (2.0 * pi / tentacleCount) * i
    # basePosition = [
    #     (canvasW/2) + (cos(angle) * canvasW * 0.2),
    #     (canvasH/2) + (sin(angle) * canvasH * 0.2)
    # ]

    basePosition = [
        rF() * canvasW,
        rF() * canvasH
    ]
    
    # Tentacle(id, basePosition, segmentCount, segmentLength)
    tentacles.append( Tentacle(i, basePosition, segmentCount, segmentLength) )



targetX = rF(canvasW*0.25, canvasW*0.75)
targetY = rF(canvasH*0.25, canvasH*0.75)
targetXVel = rF(-0.2, 0.2)
targetYVel = rF(-0.2, 0.2)
while True:
    canvas.fill((255, 255, 255))

    # averageBaseX = int( sum([t.basePosition[0] for t in tentacles]) / tentacleCount )
    # averageBaseY = int( sum([t.basePosition[1] for t in tentacles]) / tentacleCount )
    # pygame.draw.circle(
    #     canvas, 
    #     (50, 50, 50), 
    #     (averageBaseX, averageBaseY), 
    #     4, 
    #     0
    # )

    # averageEndX = int( sum([t.ends[0][0] for t in tentacles]) / tentacleCount )
    # averageEndY = int( sum([t.ends[0][1] for t in tentacles]) / tentacleCount )
    # pygame.draw.circle(
    #     canvas, 
    #     (50, 50, 50), 
    #     (averageEndX, averageEndY), 
    #     4, 
    #     0
    # )

    # avgBase_To_avgEnd_angle = atan2(averageEndY-averageBaseY, averageEndX-averageBaseX)
    # pygame.draw.line(canvas, (150, 255, 150), (averageBaseX, averageBaseY), 
    #     (
    #         averageBaseX + int(cos(avgBase_To_avgEnd_angle) * canvasW),
    #         averageBaseY + int(sin(avgBase_To_avgEnd_angle) * canvasW)
    #     ), 
    #     2
    # )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            for t in tentacles:
                t.basePosition = [
                    rF(canvasW*0.2, canvasW*0.8),
                    rF(canvasH*0.2, canvasH*0.8)
                ]
            
            targetX = rF(canvasW*0.1, canvasW*0.9)
            targetY = rF(canvasH*0.1, canvasH*0.9)
            targetXVel = rF(-0.2, 0.2)
            targetYVel = rF(-0.2, 0.2)

    
    targetX += targetXVel
    targetY += targetYVel
    if targetX < 0 or targetX > canvasW: targetXVel *= -1
    if targetY < 0 or targetY > canvasH: targetYVel *= -1
    pygame.draw.circle(
        canvas, 
        (150, 255, 150), 
        (int(targetX), int(targetY)), 
        12, 
        0
    )
    
    for t in tentacles:
        t.target(targetX, targetY)
        t.render()

    pygame.display.flip()