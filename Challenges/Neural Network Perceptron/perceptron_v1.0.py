
"""
    This perceptron is supposed to find the values for m and b in the "y=mx+b" equation, 
    to find the line of best fit between two sets of points.
"""

import numpy as np
import pygame
from random import randint

screenW, screenH = (400, 400)
screen = pygame.display.set_mode((screenW, screenH))

def randomFloat(min_, max_, dec_ = 2):
    rng = float(max_ - min_)
    pct = randint(0, 10**dec_) / float(10**dec_)
    return round(min_ + (rng*pct), dec_)

"""
Equation = y = m(x - c) + b, where:
m = line gradient
c = x-adjustment
b = y-adjustment
"""

m = randomFloat(-5, 5)
c = int(screenW * randomFloat(0.2, 0.8))
b = int(screenH * randomFloat(0.2, 0.8))

radius = int(min(screenW, screenH) * 0.018)

class Point:
    def __init__(self, x_, y_):
        self.position = (x_, y_)
        self.group = self.setGroup()
    
    def setGroup(self):
        if self.position[0] <= ((self.position[1] - b) / m) + c:
            return 'o'
        else:
            return 'x'
    
    def render(self):
        if self.group == 'o':
            pygame.draw.circle(
                screen, (0, 0, 0),
                self.position,
                radius,
                1
            )
        else:
            # Draw the diagonal line \
            pygame.draw.line(
                screen, (0, 0, 0),
                (
                    self.position[0] - radius,
                    self.position[1] - radius
                ),
                (
                    self.position[0] + radius,
                    self.position[1] + radius
                ),
                2
            )

            # Draw the diagonal line /
            pygame.draw.line(
                screen, (0, 0, 0),
                (
                    self.position[0] + radius,
                    self.position[1] - radius
                ),
                (
                    self.position[0] - radius,
                    self.position[1] + radius
                ),
                2
            )
pointCount = 16


# 3x inputs  (x, y, group)
# 3x outputs (m, c, b)
layerNeuronCount = (3, 4, 3)
class NeuralNetwork:
    def __init__(self):
        self.weights = [
            np.random.standard_normal((x, y)) for x, y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])
        ]
        self.biases = [
            np.random.standard_normal() for _ in range(len(layerNeuronCount)-1)
        ]


# Left of line is a nought, right is a cross
noughts = []
crosses = []
def createPoints():
    noughts.clear()
    crosses.clear()
    for _ in range(pointCount):
        x = randint(radius * 2, screenW - (radius * 2))
        y = randint(radius * 2, screenH - (radius * 2))

        newPoint = Point(x, y)
        
        if newPoint.group == 'o':
            noughts.append(newPoint)
        else:
            crosses.append(newPoint)
createPoints()

while(True):
    screen.fill((255, 255, 255))

    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONUP:
            m = randomFloat(0.01, 5) * ((randint(0, 1) * 2) - 1)
            c = int(screenW * randomFloat(0.2, 0.8))
            b = int(screenH * randomFloat(0.2, 0.8))
            createPoints()
            # n = NeuralNetwork()

    pygame.draw.line(
        screen, (255, 150, 150),
        ((-b / m) + c, 0),
        (((screenH - b) / m) + c, screenH), 
        4
    )

    for pt in noughts:
        pt.render()
    for pt in crosses:
        pt.render()
    
    pygame.display.flip()