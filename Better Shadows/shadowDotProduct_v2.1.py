
import pygame
pygame.init()

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))
pygame.display.set_caption("shadowDotProduct_v2.1")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font("freesansbold.ttf", 16)

vectorRenderLength = 50

vertices = [
    [canvasW * 0.3, canvasH * 0.3],
    [canvasW * 0.7, canvasH * 0.3],
    [canvasW * 0.7, canvasH * 0.7],
    [canvasW * 0.3, canvasH * 0.7]
]

# vertices = [
#     [canvasW * 0.36, canvasH * 0.10],
#     [canvasW * 0.70, canvasH * 0.36],
#     [canvasW * 0.62, canvasH * 0.62],
#     [canvasW * 0.10, canvasH * 0.90]
# ]
vertexCount = len(vertices)

def drawShape(COLOUR):
    for c in range(vertexCount):
        pygame.draw.line(canvas, COLOUR, vertices[c], vertices[(c+1)%vertexCount], 1)

def calculateNormal(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    return [-dy/h, dx/h]

normals = [calculateNormal(vertices[c], vertices[(c+1)%vertexCount]) for c in range(vertexCount)]
# print(normals)

def vectorFromTo(from_, to_):
    dx = to_[0] - from_[0]
    dy = to_[1] - from_[1]
    h = ((dx**2) + (dy**2)) ** 0.5
    return [dx/h, dy/h]

def dot(A, B):
    return sum([A[i] * B[i] for i in range(len(A))])

def textLocation(line, startOrEnd, distanceFromVertexMultiplier=0.75):
    # line -> int (0 - vertexCount)
    # startOrEnd -> int (0 / 1):(start / end)
    startX, startY = vertices[line]
    endX, endY = vertices[(line+1)%vertexCount]

    dx = endX - startX
    dy = endY - startY

    lineXAddition = dx * startOrEnd
    lineYAddition = dy * startOrEnd

    lineNormal = normals[line] # calculateNormal((startX, startY), (endX, endY))
    normalXAddition = lineNormal[0] * vectorRenderLength * distanceFromVertexMultiplier
    normalYAddition = lineNormal[1] * vectorRenderLength * distanceFromVertexMultiplier

    return (startX + lineXAddition + normalXAddition, startY + lineYAddition + normalYAddition)

textSurfaces = [font.render("-100", True, BLUE) for _ in range(vertexCount*2)]
textSurfaceCenters = []
for v in range(vertexCount):
    textSurfaceCenters.append(textLocation(v, 0))
    textSurfaceCenters.append(textLocation(v, 1))

def showText(textToShow, COLOUR=BLUE):

    for c in range(vertexCount):
        # Draw dot() text:
        # textSurfaces[c*2]     = font.render(f"{round(STM_NORM, 1)}", True, COLOUR)
        textSurfaces[c*2]     = font.render(textToShow[c*2], True, COLOUR)
        textRect = textSurfaces[c*2].get_rect()
        textRect.center = textSurfaceCenters[c*2] # (midX, midY)
        canvas.blit(textSurfaces[c*2], textRect)
        pygame.draw.line(canvas, COLOUR, vertices[c], textRect.center, 1)

        # textSurfaces[(c*2)+1] = font.render(f"{round(ETM_NORM, 1)}", True, COLOUR)
        textSurfaces[(c*2)+1] = font.render(textToShow[(c*2)+1], True, COLOUR)
        textRect = textSurfaces[(c*2)+1].get_rect()
        textRect.center = textSurfaceCenters[(c*2)+1]
        canvas.blit(textSurfaces[(c*2)+1], textRect)
        pygame.draw.line(canvas, COLOUR, vertices[(c+1)%vertexCount], textRect.center, 1)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    mx, my = pygame.mouse.get_pos()
    VTM = [
        vectorFromTo(vertex, (mx, my))
        for vertex in vertices
    ]
    
    canvas.fill(WHITE)
    drawShape(GREY)

    showText([str(c) for c in range(vertexCount * 2)])
    # txt = []
    # for c in range(vertexCount * 2):
    #     n = 1.23 * ((c%2)*2-1)
    #     txt.append(str(n))
    # showText(txt)

    for c in range(vertexCount):
        x1, y1 = vertices[c]
        x2 = x1 + (VTM[c][0] * vectorRenderLength)
        y2 = y1 + (VTM[c][1] * vectorRenderLength)
        pygame.draw.line(canvas, GREEN, (x1, y1), (x2, y2), 1)
    
    pygame.display.update()