
# from math import pi, cos, sin, atan2

import pygame
canvasW, canvasH = 700, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# import LukeLibrary as LL
from LukeLibrary import Wall

# terrainPoints = __import__("terrain").createTerrain(700, 500)

terrainLength = 50
terrainPoints = __import__("terrain").createTerrain(terrainLength, xScale_=canvasW, yScale_=canvasH)
# print(terrainPoints)
terrainMovementSpeed = 0.1 # How fast the terrain moves across the screen

armMovementSpeed = terrainMovementSpeed**2 # 1 / (terrainMovementSpeed * 0.3)

baseX = canvasW // 2
baseY = canvasH // 4.5
segmentCount = 3
segmentLength= ((canvasH/2) - baseY)*1.5 / segmentCount

# Arm(segmentCount_=3, segmentLength_=50, basePosition_=None, armSpeed_=1.0, targetSeekAngle_=pi*0.25)
robotArm = __import__("arm").Arm(
    segmentCount,
    segmentLength,
    [baseX, baseY],
    armMovementSpeed
)

def robotArm_findNewTargetPosition():
    wallList = []
    for c in range(terrainLength-1):
        x1, y1 = terrainPoints[c]
        x2, y2 = terrainPoints[c + 1]

        wallList.append( Wall(x1, y1, x2, y2) )

    robotArm.findNewTargetPosition(wallList)
# print(f"BEFORE: {robotArm.targetPosition}")
# robotArm_findNewTargetPosition()
# print(f"AFTER:  {robotArm.targetPosition}")



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # if event.type == pygame.MOUSEMOTION:
        #     mouseX, mouseY = pygame.mouse.get_pos()

    canvas.fill((255, 255, 255))

    # Draw the terrain: 
    for c in range(terrainLength - 1):
        n = c + 1
        pygame.draw.line(
            canvas, 
            (0,200,0), 
            terrainPoints[c], 
            terrainPoints[n], 
            2
        )
    
    # Move the terrain:
    for c in range(terrainLength):
        terrainPoints[c][0] -= terrainMovementSpeed
    
    # Loop the terrain back around once it leaves the canvas:
    if terrainPoints[0][0] <= -(canvasW / terrainLength):
        terrainPoints[0][0] = canvasW + (canvasW / terrainLength)
        terrainPoints = terrainPoints[1:] + [terrainPoints[0]]


    if robotArm.reachedTargetPosition == False:
        robotArm_findNewTargetPosition()
    else:
        # Move the target position along with the terrain:
        robotArm.targetPosition[0] -= terrainMovementSpeed

    # If the target has gone past where the arm can reach, 
    # find a new target ahead of the robot body:
    if robotArm.targetPositionOutOfReach():
        robotArm.reachedTargetPosition = False
        robotArm_findNewTargetPosition()
        # print(robotArm.targetPosition)

    
    robotArm.reachForTarget()
    
    # render(renderLocation_, renderColour_, showReach_=False, showTarget_=False)
    robotArm.render(canvas, (0,0,0))


    pygame.display.flip()