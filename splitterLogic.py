
import pygame

canvasW, canvasH = 640, 480
canvas = pygame.display.set_mode((canvasW, canvasH))

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
    
    canvas.fill((255, 200, 200))

    mX, mY = pygame.mouse.get_pos()
    pygame.draw.circle(canvas, (0,0,0), (int(mX), int(mY)), 8, 0)

    pygame.display.flip()