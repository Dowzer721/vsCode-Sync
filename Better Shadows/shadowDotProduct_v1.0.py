
from math import atan2, cos, sin

import pygame 

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("shadowDotProduct_v1.0")
vectorRenderSize = 25

def calculateLineNormals(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    normals = [
        [-dy,  dx],
        [ dy, -dx]
    ]

    hyp = [
        (normals[0][0]**2 + normals[0][1]**2) ** 0.5,
        (normals[1][0]**2 + normals[1][1]**2) ** 0.5
    ]

    for n in range(2):
        # normals[n][0] = (normals[n][0] / hyp[n])
        # normals[n][1] = (normals[n][1] / hyp[n])
        normals[n][0] /= hyp[n]
        normals[n][1] /= hyp[n]
    
    return normals

def calculateVectorToTarget(start, target):
    
    dx = target[0] - start[0]
    dy = target[1] - start[1]

    angle = atan2(dy, dx)
    return [cos(angle), sin(angle)]

def dot(A, B):
    # magA = A[0] * A[1]
    # magB = B[0] * B[1]
    # angleA = atan2(A[1], A[0])
    # angleB = atan2(B[1], B[0])
    # dAngle = angleB - angleA
    # return magA * magB * cos(dAngle)

    return (A[0] * B[0]) + (A[1] * B[1])

    # return (A[0]*A[1]) * (B[0]*B[1]) * cos(atan2(B[1], B[0]) - atan2(A[1], A[0]))

vertices = [
    [canvasW*0.1, canvasH*0.1],
    [canvasW*0.8, canvasH*0.3],
    [canvasW*0.6, canvasH*0.9],
    #[canvasW*0.3, canvasH*0.6]
]
vertexCount = len(vertices)

normals = [calculateLineNormals(vertices[c], vertices[(c+1)%vertexCount]) for c in range(vertexCount)] + [calculateLineNormals(vertices[(c+1)%vertexCount], vertices[c]) for c in range(vertexCount)]
# raise Exception(normals)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
    mx, my = pygame.mouse.get_pos()

    canvas.fill((255,255,255))

    for lineIndex in range(vertexCount):# * 2):
        nextLineIndex = (lineIndex + 1) % vertexCount
        lineStartX, lineStartY = vertices[lineIndex]
        lineEndX, lineEndY = vertices[nextLineIndex]
        pygame.draw.line(canvas, (0,0,0), (lineStartX, lineStartY), (lineEndX, lineEndY), 1)

        toMouseVector = calculateVectorToTarget(vertices[lineIndex], (mx,my))
        tMV_renderX = lineStartX + (toMouseVector[0] * vectorRenderSize)
        tMV_renderY = lineStartY + (toMouseVector[1] * vectorRenderSize)
        pygame.draw.line(canvas, (0,0,200), (lineStartX, lineStartY), (tMV_renderX, tMV_renderY), 1)

        

        lineStartNormals = normals[lineIndex]
        lSN_0 = lineStartNormals[0]
        lSN_0_dot = dot(lSN_0, toMouseVector)
        pygame.draw.line(canvas,(200,0,0),
            (lineStartX, lineStartY),
            (lineStartX + (lSN_0[0] * lSN_0_dot * vectorRenderSize), lineStartY + (lSN_0[1] * lSN_0_dot * vectorRenderSize)),
        1)

        # lineEndNormals = normals[lineIndex + vertexCount]
        # lEN_0 = lineEndNormals[0]
        # lEN_0_dot = dot(lEN_0, toMouseVector)
        # lEN_1 = lineEndNormals[1]
        # lEN_1_dot = dot(lEN_1, toMouseVector)
        # pygame.draw.line(canvas,(200,0,0),
        #     (lineEndX, lineEndY),
        #     (lineEndX + (lEN_0[0] * lEN_0_dot * vectorRenderSize), lineEndY + (lEN_0[1] * lEN_0_dot * vectorRenderSize)),
        # 1)

        # # for normalIndex in range(vertexCount):
        #     lineStartNormals = normals[lineIndex][normalIndex]
        #     # lineEndNormals = normals[lineIndex][normalIndex + vertexCount]

        #     lSN_x1 = lineStartX + (lineStartNormals[0] * vectorRenderSize)
        #     lSN_y1 = lineStartY + (lineStartNormals[1] * vectorRenderSize)

        # normalStartX, normalStartY = vertices[lineIndex % vertexCount]
        # for normalIndex in range(0, len(normals[lineIndex])//2, 2):
        #     normal_0_EndX = normalStartX + (normals[lineIndex][normalIndex  ][0] * vectorRenderSize)
        #     normal_0_EndY = normalStartY + (normals[lineIndex][normalIndex  ][1] * vectorRenderSize)
        #     normal_1_EndX = normalStartX + (normals[lineIndex][normalIndex+1][0] * vectorRenderSize)
        #     normal_1_EndY = normalStartY + (normals[lineIndex][normalIndex+1][1] * vectorRenderSize)
            
        #     # pygame.draw.line(canvas, (200,0,0), (normalStartX, normalStartY), (normal_0_EndX, normal_0_EndY), 1)
        #     # pygame.draw.line(canvas, (200,0,0), (normalStartX, normalStartY), (normal_1_EndX, normal_1_EndY), 1)
        #     pygame.draw.line(canvas, (200,0,0), (normal_0_EndX, normal_0_EndY), (normal_1_EndX, normal_1_EndY), 1)
        #     # pygame.draw.line(canvas,(200,0,0), normals[lineIndex][normalIndex], normals[lineIndex][normalIndex+1], 1)

    pygame.draw.circle(canvas, (0,0,0), (mx, my), 4, 0)
    
    pygame.display.update()