
import pygame
from pygame import font
pygame.init()

canvasW, canvasH = 600, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

availableColours = {
    "WHITE": (255,255,255),
    "GREY":  (200,200,200),
    "BLACK": (0, 0, 0),
    "RED":   (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE":  (0, 0, 255)
}


canvas.fill((200,200,200))

# surfaceWidth = int(canvasW / 2)
# surfaceHeight= canvasH

# shapeCellSize = int(min(surfaceWidth, surfaceHeight) * 0.08)
# gridSize = (int(surfaceWidth / shapeCellSize), int(surfaceHeight / shapeCellSize))

shapeCellSize = 16
gridSize = (10, 20)

surfaceWidth = gridSize[0] * shapeCellSize
surfaceHeight= gridSize[1] * shapeCellSize

surfaceCountX = 2
surfaceCountY = 1

surfaceXOffset = (canvasW - (surfaceWidth *surfaceCountX)) / (surfaceCountX+1)
surfaceYOffset = (canvasH - (surfaceHeight*surfaceCountY)) / (surfaceCountY+1)

# surfacePosition = [
#     (surfaceXOffset*(i+1) + surfaceWidth*i, surfaceYOffset)
#     for i in range(surfaceCountX)
# ]
surfacePosition = []
for r in range(surfaceCountY):
    y = (surfaceYOffset * (r+1)) + (surfaceHeight * r)
    for c in range(surfaceCountX):
        x = (surfaceXOffset*(c+1)) + (surfaceWidth * c)
        surfacePosition.append((x,y))


Surfaces = {
    "main": (pygame.Surface((surfaceWidth, surfaceHeight)), surfacePosition[0]),
    "make": (pygame.Surface((surfaceWidth, surfaceHeight)), surfacePosition[1])
}

for surf, _ in list(Surfaces.values()):
    surf.fill((255,255,255))

def drawGrid(targetSurfaceName_):
    for row in range(gridSize[1]+1):
        y = row * shapeCellSize
        pygame.draw.line(Surfaces[targetSurfaceName_][0], (0,0,0), (0, y), (canvasW, y), 1)
    
    for col in range(gridSize[0]+1):
        x = col * shapeCellSize
        pygame.draw.line(Surfaces[targetSurfaceName_][0], (0,0,0), (x, 0), (x, canvasH), 1)

global newShapeCol, newShapeRow
global newShapeColourIndex
global newShapeColour

newShapeCol, newShapeRow = [0, 0]
newShapeColourIndex = -1
newShapeColour = list(availableColours.values())[newShapeColourIndex]

def incrementChosenColour():
    global newShapeColourIndex, newShapeColour
    newShapeColourIndex = (newShapeColourIndex + 1) % len(availableColours)
    newShapeColour = list(availableColours.values())[newShapeColourIndex]
    # print(newShapeColour)
    # print(newShapeColourIndex)
    # return list(availableColours.values())[newShapeColourIndex]
    # newShapeColourIndex


# newShapeColour = list(availableColours.values())[newShapeColourIndex]

class Button:
    def __init__(self, canvasPosition_, size_, text_, font_, function_=lambda:print("No function passed to button")):
        self.globalPosition = canvasPosition_
        self.size = size_
        font = pygame.font.Font("freesansbold.ttf", size_[1])
        textWidth, _ = font.size(text_)
        adjustedHeight = (size_[0] / textWidth) * size_[1] * 0.9
        font = pygame.font.Font("freesansbold.ttf", int(adjustedHeight))
        # input(textWidth)
        self.text = font_.render(text_, True, availableColours["BLACK"])
        self.textRect = self.text.get_rect()
        self.textRect.center = (
            self.globalPosition[0] + (self.size[0]/2), 
            self.globalPosition[1] + (self.size[1]/2)
        )
        #self.renderSurface = pygame.Surface()
        self.functionToCall = function_
    def mouseClick(self, mousePosition_):
        x1, y1 = self.globalPosition
        x2 = x1 + self.size[0]
        y2 = y1 + self.size[1]

        if (
            (mousePosition_[0] > x1) and 
            (mousePosition_[0] < x2) and 
            (mousePosition_[1] > y1) and 
            (mousePosition_[1] < y2)):
            self.functionToCall()
    def render(self):
        global newShapeColour

        x1, y1 = self.globalPosition
        x2 = x1 + self.size[0]
        y2 = y1 + self.size[1]
        
        pygame.draw.polygon(canvas, availableColours["BLACK"], [(x1-1, y1-1), (x2+1, y1-1), (x2+1, y2+1), (x1-1, y2+1)], 1)
        pygame.draw.polygon(canvas, (100,100,100), [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 0)
        canvas.blit(self.text, self.textRect)

buttonSize = (int(surfaceWidth/4)-1, 10)

buttonPositions = [
    (
        Surfaces["make"][1][0]+1 + (buttonSize[0]*i),
        Surfaces["make"][1][1]-buttonSize[1]
    ) for i in range(4)
]

buttonTexts = ["COLOUR", "COLUMN", "ROW", "SIZE"]

font = pygame.font.Font("freesansbold.ttf", buttonSize[1])

# minTextHeight = 100
# for t in buttonTexts:
    # minTextHeight = min(minTextHeight, t)

textWidth, _ = font.size(buttonTexts[0])
adjustedHeight = (buttonSize[0] / textWidth) * buttonSize[1] * 0.9
font = pygame.font.Font("freesansbold.ttf", int(adjustedHeight))

Buttons = [
    Button(buttonPositions[0], buttonSize, buttonTexts[0], font, incrementChosenColour),
    Button(buttonPositions[1], buttonSize, buttonTexts[1], font),
    Button(buttonPositions[2], buttonSize, buttonTexts[2], font),
    Button(buttonPositions[3], buttonSize, buttonTexts[3], font)
]



class Shape:
    def __init__(self, location_, shape_):
        pass

mx = my = 0

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if ev.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            for B in Buttons:
                B.mouseClick((mx,my))
    
    for B in Buttons:
        B.render()   

    drawGrid("main")
    drawGrid("make")

    # for surf, pos in list(Surfaces.values()):
    #     canvas.blit
    canvas.blits(list(Surfaces.values()))

    pygame.display.update()