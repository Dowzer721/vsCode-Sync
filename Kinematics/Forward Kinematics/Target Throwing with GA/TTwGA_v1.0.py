
import pygame
from arm import Arm
from GA import GA

canvasW, canvasH = 700, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

targetPosition = (canvasW//8, canvasH//3)
targetRadius = 16

armBasePosition = (3*canvasW//4, 3*canvasH//4)

# __init__(self, basePosition_, segmentCount_=2, segmentLength_=50)
robotArm = Arm(armBasePosition, renderLocation_=canvas)

frame = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            robotArm = Arm(armBasePosition, renderLocation_=canvas)         
    
    canvas.fill((255, 255, 255))

    pygame.draw.circle(
        canvas,
        (100, 255, 100),
        targetPosition,
        targetRadius,
        0
    )

    pygame.draw.circle(
        canvas,
        (0,0,0),
        armBasePosition,
        targetRadius//2,
        0
    )

    robotArm.rotateJoints(showVelocity_=True)
    robotArm.render()

    pygame.display.flip()

    frame += 1