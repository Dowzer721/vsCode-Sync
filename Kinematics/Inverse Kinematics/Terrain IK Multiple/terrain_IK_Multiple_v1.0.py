
import pygame
canvasW, canvasH = 700, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

from creature import Creature

# def __init__(self, position_=[50, 50], numberOfLegs_=2, numberOfSegmentsPerLeg=2, legsOffset_=0, bodyWidth_=250, bodyHeight_=100)
bW, bH = canvasW//3, canvasH//4
bX = (canvasW // 2) - (bW // 2)
bY = (bH // 4)

segmentCount = 2
segmentLength = (((canvasH/2) - (bY+bH)) / segmentCount) * 1.5
bug = Creature(position_ = [bX, bY], bodyWidth_ = bW, bodyHeight_ = bH, numberOfLegs_=4, numberOfSegmentsPerLeg_=segmentCount, lengthOfEachLegSegment_=segmentLength)

from terrain import createTerrain
terrainLength = 20
global terrain
terrain = createTerrain(terrainLength, xScale_ = canvasW, yScale_ = canvasH)
terrainMovementSpeed = 0.1

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
from LukeLibrary import Wall

def createNewTerrain():
    global terrain
    terrain = createTerrain(terrainLength, xScale_ = canvasW, yScale_ = canvasH)
    wallList = []
    for c in range(terrainLength-1):
        x1, y1 = terrain[c]
        x2, y2 = terrain[c + 1]

        wallList.append( Wall(x1, y1, x2, y2) )
    
    for L in bug.legs:
        L.reachedTargetPosition = False
        L.findNewTargetPosition(wallList)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            createNewTerrain()
            # terrain = createTerrain(terrainLength, xScale_ = canvasW, yScale_ = canvasH)
            # bug.updateLegs(terrain, terrainMovementSpeed)
            # # for L in bug.legs:
            # #     L.findNewTargetPosition(terrain)
    
    canvas.fill((255, 255, 255))

    # Draw the terrain: 
    for c in range(terrainLength - 1):
        n = c + 1
        pygame.draw.line(
            canvas, 
            (0,200,0), 
            terrain[c], 
            terrain[n], 
            2
        )
    
    # Move the terrain:
    for c in range(terrainLength):
        terrain[c][0] -= terrainMovementSpeed
    
    # Loop the terrain back around once it leaves the canvas:
    if terrain[0][0] <= -(canvasW / terrainLength):
        terrain[0][0] = canvasW + (canvasW / terrainLength)
        terrain = terrain[1:] + [terrain[0]]

    #def updateLegs(self, terrainPoints_, terrainMovementSpeed_)
    bug.updateLegs(terrain, terrainMovementSpeed)

    # def render(self, renderLocation_, renderColour_=(0,0,0), legRenderColour_=(100,100,100))
    bug.render(canvas)
    
    pygame.display.flip()