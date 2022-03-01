
from math import pi, cos, sin
import pygame
from random import randint

totalCol, totalRow = 20, 30
canvasW, canvasH = 500, 500

newW = canvasW * (totalCol / totalRow)
newH = canvasH * (totalRow / totalCol)

if newW < newH: canvasW = newW
else: canvasH = newH

cellW = canvasW / totalCol
cellH = canvasH / totalRow

canvasW, canvasH = int(canvasW), int(canvasH)
canvas = pygame.display.set_mode((canvasW, canvasH))

def sign(val_):
    if val_ > 0:
        return 1
    
    if val_ < 0:
        return -1
    
    return 0

class Cell:
    def __init__(self, col_, row_, occupied_=False):
        self.col = col_
        self.row = row_
        self.occupied = occupied_
    def render(self):
        x1 = int(self.col * cellW)
        y1 = int(self.row * cellH)
        x2 = x1 + int(cellW)
        y2 = y1 + int(cellH)
        pygame.draw.polygon(
            canvas, (255, 255, 255),
            (
                (x1, y1), (x2, y1), (x2, y2), (x1, y2)
            ), 1
        )
Grid = [[Cell(c, r) for c in range(totalCol)] for r in range(totalRow)]

class Snake:
    def __init__(self):
        x = randint(0, totalCol-1)
        y = randint(0, totalRow-1)
        self.headLocation = [x, y]
        self.bodyLocation = []
        self.direction = 0
        self.thickness = int(cellW * 0.8 * 0.5)
    def move(self):
        
        angle = (-pi / 2) + ((pi / 2) * self.direction)
        xAdd = sign(round(cos(angle), 2))
        yAdd = sign(round(sin(angle), 2))
        
        previousHeadLocation = self.headLocation
        
        self.headLocation = [
            (self.headLocation[0] + totalCol + xAdd) % totalCol,
            (self.headLocation[1] + totalRow + yAdd) % totalRow
        ]

        if len(self.bodyLocation) == 0:
            return

        for c in range(len(self.bodyLocation)-1, -1, -1): # 3, 2, 1, 0
            if c > 0:
                self.bodyLocation[c] = self.bodyLocation[c-1]
            else:
                self.bodyLocation[c] = previousHeadLocation


            
    def render(self):
        
        # Draw the body before the head:
        for loc in self.bodyLocation:
            x3 = int(cellW * (loc[0] + 0.5))
            y3 = int(cellH * (loc[1] + 0.5))
            pygame.draw.circle(
                canvas, (0, 200, 0),
                (x3, y3), int(self.thickness*0.9), 0
            )
        
        # Draw the head:
        x1 = int(cellW * (self.headLocation[0] + 0.5))
        y1 = int(cellH * (self.headLocation[1] + 0.5))
        pygame.draw.circle(
            canvas, (0, 200, 0),
            (x1, y1), self.thickness, 0
        )
        # Draw the direction:
        dirAngle = (-pi/2) + (self.direction*pi/2)
        x2 = x1 + (cos(dirAngle) * self.thickness)
        y2 = y1 + (sin(dirAngle) * self.thickness)
        pygame.draw.line(
            canvas, (200, 0, 0),
            (x1, y1), (x2, y2),
            1
        )

snek = Snake()

foodLocation = [totalCol-1-snek.headLocation[0], totalRow-1-snek.headLocation[1]]
# print(f"foodLocation:{foodLocation}")

frameStep = 50# 1000
frame = 0
turned = False
cheatMode = False
while True:
    
    frame += 1
    if frame % frameStep == 0:

        if cheatMode:
            foodDx = foodLocation[0] - snek.headLocation[0]
            foodDy = foodLocation[1] - snek.headLocation[1]
            if foodDx != 0:
                snek.direction = (4 + sign(foodDx)) % 4
            else:
                snek.direction = (1 + sign(foodDy)) % 4
            
            nextPosition = [
                snek.headLocation[0] + sign(foodDx), 
                snek.headLocation[1] + sign(foodDy)
            ]
            # print(snek.bodyLocation)
            # input(nextPosition)
            if nextPosition in snek.bodyLocation:
                snek.direction = (snek.direction + 1) % 4

        snek.move()
        turned = False
        if snek.headLocation == foodLocation:
            # print("Snake eaten the food.")
            snek.bodyLocation.append(snek.headLocation)
            while foodLocation in snek.bodyLocation:
                foodLocation = [randint(0, totalCol-1), randint(0, totalRow-1)]
            frameStep = max(50, frameStep - 50)

        frame = 0
    
    canvas.fill((0, 0, 0))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.KEYUP:
            if turned == True: continue

            if ev.key == pygame.K_a:
                snek.direction = (snek.direction + 3) % 4
                turned = True
            if ev.key == pygame.K_d:
                snek.direction = (snek.direction + 1) % 4
                turned = True
            if ev.key == pygame.K_w:
                snek.move()
            
            if ev.key == pygame.K_c:
                cheatMode ^= True
                # print(cheatMode)
        
        if ev.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            mc = int(mx / (canvasW / totalCol))
            mr = int(my / (canvasH / totalRow))
            foodLocation = [mc, mr]
    
    # for row in Grid:
    #     for C in row:
    #         C.render()

    snek.render()
    
    foodX = int((foodLocation[0] + 0.5) * cellW)
    foodY = int((foodLocation[1] + 0.5) * cellH)
    pygame.draw.circle(
        canvas, (255, 50, 50),
        (foodX, foodY),
        int(snek.thickness * 0.8), 0
    )
    

    pygame.display.flip()