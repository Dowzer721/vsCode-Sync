
from math import floor
import pygame

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

gameGridScale = 16
gameGridZoom = 1
gameGridPosition = [(canvasW//2) - (gameGridScale//2), (canvasH//2) - (gameGridScale//2)]

def update_gameGridColRowCount():
    newColCount = int((canvasW/(gameGridScale*gameGridZoom)) + 2)
    newRowCount = int((canvasH/(gameGridScale*gameGridZoom)) + 2)

    newColCount += int(newColCount % 2)
    newRowCount += int(newRowCount % 2)

    # print((newColCount, newRowCount))

    return (newColCount, newRowCount)
gameGridColumnCount, gameGridRowCount = update_gameGridColRowCount()

class Entity:
    def __init__(self, globalGridPosition, entitySize):
        self.globalGridPosition = globalGridPosition
        self.size = entitySize

class ConveyorBelt(Entity):
    def __init__(self, globalGridPosition, facingDirection, speed):
        super().__init__(globalGridPosition, (1,1))
        self.facingDirection = facingDirection
        self.speed = speed

        self.speedColour = (200, 0, 0)
        if (self.speed == 1):
            self.speedColour = (0, 200, 0)
        elif (self.speedColour == 2):
            self.speedColour = (0, 0, 200)
        
    def render(self):
        pass

selectedCell = (0, 0)

gameRunning = True
while gameRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            mx, my = ev.pos
            gridDx = mx - gameGridPosition[0]
            gridDy = my - gameGridPosition[1]
            selectedCol = floor(gridDx / (gameGridScale * gameGridZoom)) + 1
            selectedRow = floor(gridDy / (gameGridScale * gameGridZoom)) + 1
            print(f"({selectedCol}, {selectedRow})")

    # Get the state of the keyboard every loop:
    allKeys = pygame.key.get_pressed()
    
    # Move the game grid around:
    if allKeys[pygame.K_w]: gameGridPosition[1] -= 1
    if allKeys[pygame.K_a]: gameGridPosition[0] -= 1
    if allKeys[pygame.K_s]: gameGridPosition[1] += 1
    if allKeys[pygame.K_d]: gameGridPosition[0] += 1

    # Zoom the game grid in and out:
    if allKeys[pygame.K_KP_PLUS]: 
        gameGridZoom = min(gameGridZoom + 0.01, 4.0)
        gameGridColumnCount, gameGridRowCount = update_gameGridColRowCount()
    if allKeys[pygame.K_KP_MINUS]: 
        gameGridZoom = max(gameGridZoom - 0.01, 0.5)
        gameGridColumnCount, gameGridRowCount = update_gameGridColRowCount()


    
    canvas.fill((255, 255, 255))

    pygame.draw.circle(canvas, (255,0,0), gameGridPosition, 8, 0)

    for gameGridRow in range(gameGridRowCount):
        y1 = gameGridPosition[1] - (gameGridScale * gameGridZoom * gameGridRowCount / 2) + (gameGridRow * gameGridScale * gameGridZoom)
        y2 = y1 + (gameGridScale * gameGridZoom)
        for gameGridCol in range(gameGridColumnCount):
            x1 = gameGridPosition[0] - (gameGridScale * gameGridZoom * gameGridColumnCount / 2) + (gameGridCol * gameGridScale * gameGridZoom)
            x2 = x1 + (gameGridScale * gameGridZoom)
            pygame.draw.polygon(canvas, (0,0,0), [(x1, y1), (x2, y1), (x2, y2), (x1, y2)], 1)

    pygame.display.update()


