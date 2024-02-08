
import pygame

global vertices
vertices = [
    [0.1, 0.1],
    [0.9, 0.1],
    [0.9, 0.9],
    [0.1, 0.9]
]
global vertexCount
vertexCount = len(vertices)

global normals
normals = []
for c in range(vertexCount):
    n = (c+1) % vertexCount
    x1, y1 = vertices[c]
    x2, y2 = vertices[n]
    dx = x2 - x1
    dy = y2 - y1
    h = 1 # ((dx**2) + (dy**2)) ** 0.5
    normals.append([-dy/h, dx/h])

def setVertices(canvas):
    global vertices
    canvasW, canvasH = canvas.get_size()
    for c in range(vertexCount):
        vertices[c][0] *= canvasW
        vertices[c][1] *= canvasH

def renderPath(canvas, pathColour, cornerColour, pathWidth):
    for c in range(vertexCount):
        vx = int(vertices[c][0])
        vy = int(vertices[c][1])
        pygame.draw.circle(canvas, pathColour, (vx, vy), pathWidth, 0)
        pygame.draw.circle(canvas, cornerColour, (vx, vy), pathWidth, 2)
    
    for c in range(vertexCount):
        vx = int(vertices[c][0])
        vy = int(vertices[c][1])

        n = (c + 1) % vertexCount
        nx = int(vertices[n][0])
        ny = int(vertices[n][1])

        # dx = nx - vx
        # dy = ny - vy
        normal = normals[c]
        segmentVertices = [
            (vx + (normal[0] * pathWidth), vy + (normal[1] * pathWidth)),
            (nx + (normal[0] * pathWidth), ny + (normal[1] * pathWidth)),
            (nx - (normal[0] * pathWidth), ny - (normal[1] * pathWidth)),
            (vx - (normal[0] * pathWidth), vy - (normal[1] * pathWidth))
        ]
        pygame.draw.polygon(canvas, pathColour, segmentVertices, 0)


