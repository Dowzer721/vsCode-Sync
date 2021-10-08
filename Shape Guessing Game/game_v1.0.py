
from math import pi, cos, sin, atan2
from random import randint
import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

def randintF(min_, max_):
    """Allows the use of random.randint(a: float, b: float)."""
    return randint( int(min_), int(max_) )

def randfloat(min_ = 0.0, max_ = 1.0, dP_ = 3):
    rng = max_ - min_
    pct = randint(0, 10 ** dP_) / float(10 ** dP_)
    return round(min_ + (rng * pct), dP_)

def createNewShape(print_ = False):
    
    minX, maxX = canvasW * 0.4, canvasW * 0.6
    minY, maxY = canvasH * 0.4, canvasH * 0.6
    newX, newY = randintF(minX, maxX), randintF(minY, maxY)

    # minW, maxW = 10, min(newX, canvasW-newX)
    # minH, maxH = 10, min(newY, canvasH-newY)
    # newW, newH = randintF(minW, maxW), randintF(minH, maxH)

    newW = min(newX, canvasW - newX)
    newW -= randint(0, newW//4)
    
    newH = min(newY, canvasH - newY)
    newH -= randint(0, newH//4)

    newV = randint(3, 8)

    newA = randfloat(0.0, pi * 2.0)

    newC = randint(0, 100) < 25
    if newC:
        newW = min(newW, newH)
        newH = newW
        newA = 0

    
    
    newData = {
        "midX": newX, # X: Middle x
        "midY": newY, # Y: Middle y
        "width": newW, # W: Width of shape
        "height": newH, # H: Height of shape
        "circle": newC, # C: Is circle?
        "vertices": newV, # V: Number of vertices
        "angle": newA  # A: Starting angle
    }

    if print_:
        for key, value in newData.items():
            print(key, ':', value)
    
    return newData

shapeCount = 5
shapes = [
    createNewShape() for _ in range(shapeCount)
]

def drawShapeOnCanvas(canvas_, shapeData, outlineColour=(0,0,0), outlineThickness=2):

    middleX, middleY = shapeData["midX"], shapeData["midY"]
    shapeW, shapeH = shapeData["width"], shapeData["height"]
    isCircle = shapeData["circle"]
    vertexCount = shapeData["vertices"]
    startingAngle = shapeData["angle"]

    if isCircle:
        pygame.draw.circle(
            canvas_, outlineColour,
            (int(middleX), int(middleY)),
            shapeW, outlineThickness
        )
        return

    
    for c in range(vertexCount):
        n = (c + 1) % vertexCount

        cTheta = startingAngle + ( (pi * 2.0 * c) / vertexCount )
        x1 = int(middleX + (cos(cTheta) * shapeW) )
        y1 = int(middleY + (sin(cTheta) * shapeH) )

        nTheta = startingAngle + ( (pi * 2.0 * n) / vertexCount )
        x2 = int(middleX + (cos(nTheta) * shapeW) )
        y2 = int(middleY + (sin(nTheta) * shapeH) )

        pygame.draw.line(
            canvas_, outlineColour,
            (x1, y1), (x2, y2),
            outlineThickness
        )

while True:
    canvas.fill((255, 255, 255))

    for shape in shapes:
        drawShapeOnCanvas(canvas, shape)

    pygame.display.flip()