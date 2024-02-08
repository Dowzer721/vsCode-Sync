
from math import cos, sin
import numpy as np
import pygame

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

class Line:
    def __init__(self, start_, end_):
        self.start = start_
        self.end = end_
        
        self.renderPoints = [
            int(self.start[0]),
            int(self.start[1]),
            int(self.end[0]),
            int(self.end[1])]
    def render(self, renderColour=(200,200,200), renderThickness=1):
        x1, y1, x2, y2 = self.renderPoints
        pygame.draw.line(canvas, renderColour, (x1,y1), (x2, y2), renderThickness)

class Shape:
    def __init__(self, lines_):
        self.lines = lines_
        self.vertices = [line[0] for line in lines_]
        self.vertexCount = len(lines_)

        # self.vertices = [v.location for v in vertices_]
        # self.vertexCount = len(vertices_)
        # self.vertexNormals = []
        # for vc in range(self.vertexCount):
        #     vp = (vc + self.vertexCount - 1) % self.vertexCount
        #     vn = (vc + 1) % self.vertexCount

        #     vertexPX = self.vertices[vp][0]
        #     vertexPY = self.vertices[vp][1]
        #     vertexCX = self.vertices[vc][0]
        #     vertexCY = self.vertices[vc][1]
        #     vertexNX = self.vertices[vn][0]
        #     vertexNY = self.vertices[vn][1]

        #     vertexCP_dx = (vertexPX - vertexCX) * 0.1
        #     vertexCP_dy = (vertexPY - vertexCY) * 0.1
        #     vertexCN_dx = (vertexPX - vertexNX) * 0.1
        #     vertexCN_dy = (vertexPY - vertexNY) * 0.1

        #     normalCP = [(-vertexCP_dy, vertexCP_dx), (vertexCP_dy, -vertexCP_dx)]
        #     normalCN = [(-vertexCN_dy, vertexCN_dx), (vertexCN_dy, -vertexCN_dx)]

        #     self.vertexNormals.append(normalCP)
        #     self.vertexNormals.append(normalCN)

    def updateShadow(self, lightX, lightY):
        # Setting origin point as the light source
        lightSource = np.array([0,0])
        lightToVertexVectors = []
        
        



        
        # for vertexX, vertexY in self.vertices:
        #     dx = vertexX - lightX
        #     dy = vertexY - lightY
        #     lightToVertex = np.array([dx, dy])

        
        # lightSource = np.array([lightX, lightY])
        # vertexVectors = []
        # for vx,vy in self.vertices:
        #     vertexVec = np.array([vx - lightX, vy - lightY])
        #     vectorToLight = np.dot(vertexVec, lightSource)
        #     # vectorToLight = np.array([lightX-vx, lightY-vy])
        #     vertexVectors.append(vectorToLight)
        # return vertexVectors
            

    def render(self, renderColour=(150,150,150)):
        pygame.draw.polygon(canvas, renderColour, self.vertices, 0)

boxVertices = [
    (int(canvasW*0.4), int(canvasH*0.4)),
    (int(canvasW*0.6), int(canvasH*0.4)),
    (int(canvasW*0.6), int(canvasH*0.6)),
    (int(canvasW*0.4), int(canvasH*0.6))
]

boxLines = [
    Line(boxVertices[c], boxVertices[(c+1)%4])
    for c in range(4)
]

box = Shape(boxLines)

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    mx, my = pygame.mouse.get_pos()
    
    canvas.fill((255,255,255))

    pygame.draw.circle(canvas,(255,0,0),(mx,my),8,0)

    for box in boxes:
        # for shadow in box.updateShadow(mx, my):
        #     x1 = shadow[0]
        #     y1 = shadow[1]
            
        #     angle = np.angle(shadow)[0]
        #     x2 = x1 + (cos(angle) * 500)
        #     y2 = y1 + (sin(angle) * 500)
        #     pygame.draw.line(canvas, (0,0,0),
        #         (int(x1), int(y1)),
        #         (int(x2), int(y2)),
                
        #     )

        # boxNormals = box.vertexNormals
        # for normX, normY in boxNormals:
        for v in range(box.vertexCount):
            x1, y1 = box.vertices[v]
            for normX, normY in box.vertexNormals[v]:
                pygame.draw.line(canvas,(0,0,0),
                    (x1, y1),
                    (int(normX), int(normY)),
                    1
                )

        box.render()
    
    pygame.display.flip()