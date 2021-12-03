
from math import pi, cos, sin, atan2
import pygame
from random import randint

def rF(min_=0.0, max_=1.0, dp_=2):
    rng = max_ - min_
    pct = randint(0, 10 ** dp_) / float(10 ** dp_)
    return min_ + (rng * pct)

canvasW, canvasH = 900, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

global ballX, ballY, ballVelX, ballVelY
def randomiseBall():
    global ballX, ballY, ballVelX, ballVelY
    ballX = rF() * canvasW
    ballY = rF() * canvasH
    ballVelX = rF(-0.1, 0.1)
    ballVelY = rF(-0.1, 0.1)
randomiseBall()

ellipseW = canvasW * 0.4
ellipseH = canvasH * 0.4

while True:
    canvas.fill((255, 255, 255))

    pygame.draw.circle(canvas, (0,0,0), (canvasW//2,canvasH//2), 4, 0)
    N = 64
    for i in range(N):
        angleC = (2. * pi * i) / N
        x1 = (canvasW//2) + int(cos(angleC) * ellipseW)
        y1 = (canvasH//2) + int(sin(angleC) * ellipseH)
        # pygame.draw.circle(canvas, (0,0,0), (x1,y1), 4, 0)

        angleN = (2. * pi * (i+1)) / N
        x2 = (canvasW//2) + int(cos(angleN) * ellipseW)
        y2 = (canvasH//2) + int(sin(angleN) * ellipseH)
        pygame.draw.line(canvas, (100, 100, 100), (x1,y1), (x2,y2), 2)
    
    if ballX < 0 or ballX > canvasW: ballVelX *= -1
    if ballY < 0 or ballY > canvasH: ballVelY *= -1
    ballX += ballVelX
    ballY += ballVelY
    pygame.draw.circle(canvas, (0, 100, 0), (int(ballX), int(ballY)), 4, 0)


    x1 = (canvasW//2)
    y1 = (canvasH//2)
    dx = ballX - x1
    dy = ballY - y1
    angleToBall = atan2(dy, dx)
    x2 = int(x1 + (cos(angleToBall) * ellipseW))
    y2 = int(y1 + (sin(angleToBall) * ellipseH))
    pygame.draw.line(canvas, (0, 100, 0), (x1,y1), (x2,y2), 1)


    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP: randomiseBall()
    pygame.display.flip()

