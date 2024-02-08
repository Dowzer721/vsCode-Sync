
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import numpy as np
import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

ShapeVertices = [
    np.array([canvasW * 0.2, canvasH * 0.2]),
    np.array([canvasW * 0.8, canvasH * 0.5]),
    np.array([canvasW * 0.4, canvasH * 0.8])
]
vertexCount = len(ShapeVertices)

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    canvas.fill((255, 255, 255))

    mx, my = pygame.mouse.get_pos()
    mouseArray = np.array([mx, my])

    pygame.draw.circle(canvas, (100,255,100), (mx, my), 8, 0)

    for c in range(vertexCount):
        n = (c + 1) % vertexCount
        start = ShapeVertices[c]
        end = ShapeVertices[n]

        render_Start = (int(start[0]), int(start[1]))
        render_End = (int(end[0]), int(end[1]))
        pygame.draw.line(canvas, (0,0,0), render_Start, render_End, 1)

        # mouseDx = mx - start[0]
        # mouseDy = my - start[1]
        # vertexToMouse = np.array([mouseDx, mouseDy])

        vectorToMouse = mouseArray - start
        if np.linalg.norm(vectorToMouse) != 0:
            vectorToMouse = vectorToMouse / np.linalg.norm(vectorToMouse)
        # vectorToMouse /= np.linalg.norm(vectorToMouse)
        vectorToMouse *= -50

        render_VectorToMouse = (int(start[0] + vectorToMouse[0]), int(start[1] + vectorToMouse[1]))
        pygame.draw.line(canvas, (100,100,255), render_Start, render_VectorToMouse, 1)

        LineNormals = LL.LineNormals(start, end, normalise=True)
        for norm in LineNormals:
            normDotMouse = np.dot(norm, vectorToMouse)
            norm *= normDotMouse
            norm += start
            render_norm = (int(norm[0]), int(norm[1]))
            pygame.draw.line(canvas, (255,100,100), start, render_norm, 1)

        # LineNormals = LL.LineNormals(end, start, normalise=True)
        # for norm in LineNormals:
        #     normDotMouse = np.dot(vectorToMouse, norm)
        #     norm *= normDotMouse
        #     norm += end
        #     render_norm = (int(norm[0]), int(norm[1]))
        #     pygame.draw.line(canvas, (255,100,100), end, render_norm, 1)
        
        
    
    pygame.display.flip()