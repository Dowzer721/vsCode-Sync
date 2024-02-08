
from math import pi, cos, sin, atan2
import pygame

gameGridSize = 2 ** 4
targetCanvasHeight = 500
aspectRatio = 16/9
gameZoom = 1.0

canvasH = int((targetCanvasHeight//gameGridSize) * gameGridSize)

canvasW = int((canvasH * aspectRatio // gameGridSize) * gameGridSize)

# print(f"{canvasW} x {canvasH}")
# print(f"{canvasW//gameGridSize} x {canvasH//gameGridSize}")

canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("Factory Game")


class Entity:
    def __init__(self, globalGridPosition, entitySize, inputItem=None):
        self.globalGridPosition = globalGridPosition
        self.size = entitySize
        # self.inputLocations = inputLocations
        # self.outputLocations = outputLocations
        self.inputItem = inputItem
        self.outputItem = None
    def mapMove(self, NS_Addition, EW_Addition):
        self.globalGridPosition[0] += EW_Addition
        self.globalGridPosition[1] += NS_Addition
    def mapZoom(self, zoomAmount):
        if zoomAmount == 0: return
        midX = canvasW / 2
        midY = canvasH / 2
        dx = midX - self.globalGridPosition[0]
        dy = midY - self.globalGridPosition[1]
        angleFromCenter = atan2(dy, dx)
        distanceFromCenter = ((dx**2) + (dy**2)) ** 0.5

        newCenterDistance = distanceFromCenter * (1.0 + zoomAmount)
        self.globalGridPosition[0] = midX + (cos(angleFromCenter) * newCenterDistance)
        self.globalGridPosition[1] = midY + (sin(angleFromCenter) * newCenterDistance)
        

Entities = []

class ConveyorBelt(Entity):
    def __init__(self, globalGridPosition, facingDirection, speed):
        super().__init__(globalGridPosition, (1,1))
        self.facingDirection = facingDirection
        self.speed = speed

        # speed = 1 / 2 / 3
        self.speedColour = [0, 0, 0]
        self.speedColour[speed-1] = 200

        self.renderArrowsVertices = []
        self.gridPositionChanged(globalGridPosition)
        
    def gridPositionChanged(self, newGridPosition):

        forwardAngle = self.facingDirection * pi / 2
        forwardVector = (cos(forwardAngle), sin(forwardAngle))

        rightAngle = ((self.facingDirection + 1) % 4) * pi / 2
        rightVector = (cos(rightAngle), sin(rightAngle))

        x1, y1 = newGridPosition
        x2 = x1 + gameGridSize
        y2 = y1 + gameGridSize
        
        midX = (x1 + x2) / 2
        midY = (y1 + y2) / 2

        self.renderArrowsVertices = [
            # Rear Arrow
            (
                midX - (forwardVector[0] * gameGridSize * 0.4) - (rightVector[0] * gameGridSize * 0.4),
                midY - (forwardVector[1] * gameGridSize * 0.4) - (rightVector[1] * gameGridSize * 0.4)
            ),
            (
                midX - (forwardVector[0] * gameGridSize * 0.1),
                midY - (forwardVector[1] * gameGridSize * 0.1)
            ),
            (
                midX - (forwardVector[0] * gameGridSize * 0.4) + (rightVector[0] * gameGridSize * 0.4),
                midY - (forwardVector[1] * gameGridSize * 0.4) + (rightVector[1] * gameGridSize * 0.4)
            ),
            # Fore Arrow
            (
                midX + (forwardVector[0] * gameGridSize * 0.1) - (rightVector[0] * gameGridSize * 0.4),
                midY + (forwardVector[1] * gameGridSize * 0.1) - (rightVector[1] * gameGridSize * 0.4)
            ),
            (
                midX + (forwardVector[0] * gameGridSize * 0.4),
                midY + (forwardVector[1] * gameGridSize * 0.4)
            ),
            (
                midX + (forwardVector[0] * gameGridSize * 0.1) + (rightVector[0] * gameGridSize * 0.4),
                midY + (forwardVector[1] * gameGridSize * 0.1) + (rightVector[1] * gameGridSize * 0.4)
            )
        ]
    
    def mapMove(self, NS_Addition, EW_Addition):
        super().mapMove(NS_Addition, EW_Addition)
        self.gridPositionChanged(self.globalGridPosition)
    # def mapZoom(self, zoomAmount):
    #     super().mapZoom(zoomAmount)
    #     #self.gridPositionChanged(self.globalGridPosition)-

    def render(self):
        x1, y1 = self.globalGridPosition
        x2 = x1 + gameGridSize
        y2 = y1 + gameGridSize
        pygame.draw.polygon(canvas,(0,0,0),[(x1,y1),(x2,y1),(x2,y2),(x1,y2)], 1)

        pygame.draw.polygon(canvas, self.speedColour, self.renderArrowsVertices[0:3], 1)
        pygame.draw.polygon(canvas, self.speedColour, self.renderArrowsVertices[3:], 1)

Entities.append(ConveyorBelt([canvasW * 0.1, canvasH * 0.2], 0, 1))





while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    # Get the state of the keyboard every loop:
    allKeys = pygame.key.get_pressed()
    
    Player_NS_Addition = 0
    Player_EW_Addition = 0
    # Move the game grid around:
    if allKeys[pygame.K_w]: Player_NS_Addition = 0.1
    if allKeys[pygame.K_a]: Player_EW_Addition = 0.1
    if allKeys[pygame.K_s]: Player_NS_Addition = -0.1
    if allKeys[pygame.K_d]: Player_EW_Addition = -0.1
    if Player_NS_Addition != 0: print(f"NS: {Player_NS_Addition}")
    if Player_EW_Addition != 0: print(f"EW: {Player_EW_Addition}")

    Player_Zoom_Addition = 0
    # Zoom the game grid in and out:
    if allKeys[pygame.K_KP_PLUS]: Player_Zoom_Addition = 0.01
    if allKeys[pygame.K_KP_MINUS]: Player_Zoom_Addition = -0.01
    if Player_Zoom_Addition != 0: print(f"ZOOM: {Player_Zoom_Addition}")
        
    canvas.fill((255, 255, 255))

    pygame.draw.circle(canvas, (200, 200, 200), (canvasW//2, canvasH//2), 8, 0)

    for E in Entities:
        E.mapMove(Player_NS_Addition, Player_EW_Addition)
        E.mapZoom(Player_Zoom_Addition)
        E.render()

    pygame.display.update()