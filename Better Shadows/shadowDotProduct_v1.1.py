
import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("shadowDotProduct_v1.1")

def calculateNormal(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    hyp = ((dx**2)+(dy**2))**0.5

    return [-dy/hyp,  dx/hyp]
    # return [ dy/hyp, -dx/hyp]

def calculateVectorToTarget(start, target):
    dx = target[0] - start[0]
    dy = target[1] - start[1]
    hyp = ((dx**2)+(dy**2)) ** 0.5
    return (dx/hyp, dy/hyp)

def dot(A, B):
    return (A[0] * B[0]) + (A[1] * B[1])

# vertices = [
#     [canvasW * 0.36, canvasH * 0.1],
#     [canvasW * 0.9, canvasH * 0.36],
#     #[canvasW * 0.62, canvasH * 0.62],
#     # [280, 170],
#     [canvasW * 0.1, canvasH * 0.9]
# ]

vertices = [
    [canvasW * 0.2, canvasH * 0.2],
    [canvasW * 0.7, canvasH * 0.2],
    [canvasW * 0.8, canvasH * 0.8],
    [canvasW * 0.3, canvasH * 0.8]
]
vertexCount = len(vertices)

normals = [
    calculateNormal(vertices[c], vertices[(c+1)%vertexCount])
    for c in range(vertexCount)
]

#print(normals[0])

vectorRenderLength = 50

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())
    
    # mx, my = 

    # Vertex To Mouse
    VTM = [
        calculateVectorToTarget(pygame.mouse.get_pos(), vertex) #(mx, my))
        for vertex in vertices
    ]
    
    canvas.fill((255, 255, 255))

    for c in range(vertexCount):
        n = (c+1) % vertexCount

        start = vertices[c]
        end = vertices[n]
        pygame.draw.line(canvas, (0,0,0), start, end, 1)

        normal = normals[c]

        pygame.draw.line(canvas, (0,0,200), start,
            (
                (VTM[c][0] * vectorRenderLength) + start[0],
                (VTM[c][1] * vectorRenderLength) + start[1]
            )
        )

        
        sTM_Norm_dot = dot(VTM[c], normal)
        eTM_Norm_dot = dot(VTM[n], normal)

        normalX, normalY = normal
        
        sCol = (0,200,0) if sTM_Norm_dot > 0 else (200,200,200)
        eCol = (0,200,0) if eTM_Norm_dot > 0 else (200,200,200)
        
        pygame.draw.line(canvas, sCol, start,
            (
                (normalX * vectorRenderLength * sTM_Norm_dot) + start[0],
                (normalY * vectorRenderLength * sTM_Norm_dot) + start[1],
            ),
        1)
        pygame.draw.line(canvas, eCol, end,
            (
                (normalX * vectorRenderLength * eTM_Norm_dot) + end[0],
                (normalY * vectorRenderLength * eTM_Norm_dot) + end[1],
            ),
        1)
    
    pygame.display.update()