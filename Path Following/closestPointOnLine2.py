
import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

start = [canvasW * 0.2, canvasH * 0.2]
end = [canvasW * 0.8, canvasH * 0.6]
dx = end[0] - start[0]
dy = end[1] - start[1]
lineLength = ((dx ** 2) + (dy ** 2)) ** 0.5

def vectorFromTo(from_, to_, normalise_=1):
    dx = to_[0] - from_[0]
    dy = to_[1] - from_[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    if normalise_ == 0:
        h = 1
    return [dx/h, dy/h]

def dot(A, B):
    return (A[0] * B[0]) + (A[1] * B[1])

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    canvas.fill(WHITE)
    pygame.draw.line(canvas, BLACK, start, end, 1)
    
    lineVector = vectorFromTo(start, end)
    mx, my = pygame.mouse.get_pos()
    mouseVector = vectorFromTo(start, (mx, my), 0)
    lmDot = dot(lineVector, mouseVector)
    # print(lmDot)
    lmDot = max(0, min(lmDot, lineLength))

    cpX = start[0] + (lineVector[0] * lmDot)
    cpY = start[1] + (lineVector[1] * lmDot)
    pygame.draw.line(canvas, BLUE, (mx, my), (cpX, cpY), 1)

    # mdx = cpX - mx
    # mdy = cpY - my
    # r = int( ((mdx**2) + (mdy**2)) ** 0.5 ) + 1
    # pygame.draw.circle(canvas, BLUE, (mx, my), r, 1)

    pygame.display.update()