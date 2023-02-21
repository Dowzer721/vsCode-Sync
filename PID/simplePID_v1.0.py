
import pygame
from random import randint

canvasW, canvasH = 900, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

targetX = int(canvasW // 2)
currentX = 0
velocityX = 0

kP = 0.1
kI = 0.01
kD = 0.0#02

def error(): return (targetX - currentX)
allError = []#error()]

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    canvas.fill((255, 255, 255))

    pygame.draw.circle(
        canvas, (100, 255, 100),
        (targetX, canvasH//2),
        16
    )

    pygame.draw.circle(
        canvas, (100, 100, 100),
        (int(currentX), canvasH//2),
        12
    )

    currentError = error()
    allError.append(currentError)

    t = len(allError)

    pTerm = (kP * currentError)
    iTerm = kI * sum([err * (t-i) for err,i in enumerate(allError)]) # (kI * sum(allError))
    dTerm = 0

    velocityX += pTerm + iTerm + dTerm
    currentX += velocityX

    pygame.display.flip()