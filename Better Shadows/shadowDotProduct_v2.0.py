
import pygame
pygame.init()

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("shadowDotProduct_v2.0")

WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GREY    = (200, 200, 200)
RED     = (255, 0,   0)
GREEN   = (0,   255, 0)
BLUE    = (0,   0,   255)

font = pygame.font.Font("freesansbold.ttf", 16)

def calculateNormal(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    return [-dy/h, dx/h]

def calculateVectorToTarget(start, target):
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    return [dx/h, dy/h]

def dot(A, B):
    return (A[0] * B[0]) + (A[1] * B[1])

vertices = [
    [canvasW * 0.36, canvasH * 0.10],
    [canvasW * 0.70, canvasH * 0.36],
    [canvasW * 0.62, canvasH * 0.62],
    [canvasW * 0.10, canvasH * 0.90]
]
vertexCount = len(vertices)
shapeCenter = (
    sum([v[0] for v in vertices]) / vertexCount,
    sum([v[1] for v in vertices]) / vertexCount
)

normals = [
    calculateNormal(vertices[c], vertices[(c+1)%vertexCount])
    for c in range(vertexCount)
]
normalRenderLength = 50

textSurfaces = [font.render("-100", True, BLUE) for _ in range(vertexCount*2)]
textSurfaceCenters = []
for v in range(vertexCount):
    # dx = vx - shapeCenter[0]
    # dy = vy - shapeCenter[1]
    # dist = ((dx**2) + (dy**2)) ** 0.5
    centerToVertexNormal = calculateNormal(shapeCenter, vertices[v])
    vx, vy = vertices[v]
    textSurfaceCenters.append((
        vx + (centerToVertexNormal[0] * normalRenderLength / 2),
        vy + (centerToVertexNormal[1] * normalRenderLength / 2)
    ))
    textSurfaceCenters.append((
        vx - (centerToVertexNormal[0] * normalRenderLength / 2),
        vy - (centerToVertexNormal[1] * normalRenderLength / 2)
    ))
# print(textSurfaceCenters)
# exit(0)
    

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    mx, my = pygame.mouse.get_pos()
    # verticesToMouseVectors
    VTM = [
        # calculateVectorToTarget(vertex, (mx, my))
        calculateVectorToTarget((mx, my), vertex)
        for vertex in vertices
    ]

    canvas.fill(WHITE)

    pygame.draw.circle(canvas, GREY, (int(shapeCenter[0]), int(shapeCenter[1])), 8, 0)

    for c in range(vertexCount):
        n = (c + 1) % vertexCount

        start = vertices[c]
        end = vertices[n]
        
        # Draw edge:
        pygame.draw.line(canvas, GREY, start, end, 1)

        vectorToMouse = VTM[c]
        pygame.draw.line(canvas, BLUE, start, 
            (start[0] + (vectorToMouse[0] * normalRenderLength),
            start[1] + (vectorToMouse[1] * normalRenderLength)), 1)

        
        normal = normals[c]

        pygame.draw.line(canvas, RED,
            (start[0] - (normal[0] * normalRenderLength), 
             start[1] - (normal[1] * normalRenderLength)),
            (start[0] + (normal[0] * normalRenderLength), 
             start[1] + (normal[1] * normalRenderLength)), 1)
        
        pygame.draw.line(canvas, RED,
            (end[0] - (normal[0] * normalRenderLength), 
             end[1] - (normal[1] * normalRenderLength)),
            (end[0] + (normal[0] * normalRenderLength), 
             end[1] + (normal[1] * normalRenderLength)), 1)

        # START TO MOUSE / END TO MOUSE
        STM = VTM[c]
        ETM = VTM[n]

        STM_NORM = dot(STM, normal)
        ETM_NORM = dot(ETM, normal)

        STM_NORM_X = start[0] + (normal[0] * STM_NORM * normalRenderLength)
        STM_NORM_Y = start[1] + (normal[1] * STM_NORM * normalRenderLength)
        pygame.draw.circle(canvas, RED, (int(STM_NORM_X), int(STM_NORM_Y)), 4, 0)
        
        ETM_NORM_X = end[0]   + (normal[0] * ETM_NORM * normalRenderLength)
        ETM_NORM_Y = end[1]   + (normal[1] * ETM_NORM * normalRenderLength)
        pygame.draw.circle(canvas, RED, (int(ETM_NORM_X), int(ETM_NORM_Y)), 4, 0)
        
        # Draw dot() text:
        textSurfaces[c*2]     = font.render(f"{round(STM_NORM, 1)}", True, BLUE)
        textRect = textSurfaces[c*2].get_rect()
        textRect.center = textSurfaceCenters[c*2] # (midX, midY)
        canvas.blit(textSurfaces[c*2], textRect)

        textSurfaces[(c*2)+1] = font.render(f"{round(ETM_NORM, 1)}", True, BLUE)
        textRect = textSurfaces[(c*2)+1].get_rect()
        textRect.center = textSurfaceCenters[(c*2)+1]
        canvas.blit(textSurfaces[(c*2)+1], textRect)
        

    pygame.display.update()