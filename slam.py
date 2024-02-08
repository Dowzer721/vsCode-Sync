# TODO: Implement this work into the original code

from math import cos, sin, atan2
import pygame
from random import randint

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

def randFloat():
    _percentage = randint(0, 1000) / 1000.0
    _range = 1
    return 0.0 + (_percentage * _range)

numberOfPoints = 10
recordedPoints = [
    (canvasW * randFloat(), canvasH * randFloat())
    for _ in range(numberOfPoints)
]

class Robot:
    def __init__(self, _startingPosition=None):
        self.pos = [canvasW * 0.3, canvasH * 0.5] if _startingPosition==None else _startingPosition
        self.facing = 0
        self.radius = 16

        self.records = []
        for pt in recordedPoints:
            dx = pt[0] - self.pos[0]
            dy = pt[1] - self.pos[1]
            angle = atan2(dy, dx)
            dist = ((dx**2)+(dy**2))**0.5
            self.records.append( (angle, dist) )
    def move(self):
        
        currentX, currentY = self.pos
        
        for index, (currentAngle, currentDist) in enumerate(self.records):
            # currentAngle, currentDist = self.record
            # if index==0: print(f"START: {currentAngle}, {currentDist}")

            recordedPoint_RelativeLocation = (
                currentX + (cos(currentAngle) * currentDist),
                currentY + (sin(currentAngle) * currentDist)
            )

            nextPosition = (
                currentX + (cos(self.facing) * self.radius),
                currentY + (sin(self.facing) * self.radius)
            )

            dx = recordedPoint_RelativeLocation[0] - nextPosition[0]
            dy = recordedPoint_RelativeLocation[1] - nextPosition[1]
            
            angle = atan2(dy, dx)
            distance = ((dx**2)+(dy**2))**0.5
            
            self.records[index] = (angle, distance)
            # if index==0: print(f"END: {self.records[index]}")
        
        self.pos = [
            currentX + (cos(self.facing) * self.radius),
            currentY + (sin(self.facing) * self.radius)
        ]

        # previousAngle, previousDist = self.record
        # previousX, previousY = self.pos

        # previousRelativeX = previousX + (cos(previousAngle) * previousDist)
        # previousRelativeY = previousY + (sin(previousAngle) * previousDist)

        # movementX = cos(self.facing) * self.radius
        # movementY = sin(self.facing) * self.radius

        # self.pos[0] += movementX
        # self.pos[1] += movementY

        # dx = previousRelativeX - self.pos[0]
        # dy = previousRelativeY - self.pos[1]
        # self.record = (atan2(dy, dx), ((dx**2)+(dy**2))**0.5)




    def render(self):
        x1, y1 = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(canvas, (0,0,0), (x1, y1), self.radius, 1)

        x2 = x1 + int(cos(self.facing) * self.radius)
        y2 = y1 + int(sin(self.facing) * self.radius)
        pygame.draw.line(canvas, (0,0,0), (x1, y1), (x2, y2), 1)

        for recordedAngle, recordedDistance in self.records:
            x3 = x1 + int(cos(recordedAngle) * recordedDistance)
            y3 = y1 + int(sin(recordedAngle) * recordedDistance)
            pygame.draw.line(canvas, (200,0,0), (x1, y1), (x3, y3), 1)

R = Robot()

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            dx = mx - R.pos[0]
            dy = my - R.pos[1]
            R.facing = atan2(dy, dx)
        if ev.type == pygame.MOUSEBUTTONUP:
            # R.pos[0] += cos(R.facing) * R.radius
            # R.pos[1] += sin(R.facing) * R.radius
            R.move()
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_r:
                recordedPoints = [
                    (canvasW * randFloat(), canvasH * randFloat())
                    for _ in range(numberOfPoints)
                ]
                R = Robot(R.pos)
    
    canvas.fill((255, 255, 255))

    for pt in recordedPoints:
        pygame.draw.circle(canvas, (0,200,0), (int(pt[0]), int(pt[1])), 4, 0)
    
    R.render()
    
    pygame.display.update()