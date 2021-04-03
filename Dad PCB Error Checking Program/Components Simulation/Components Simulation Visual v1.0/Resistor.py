
from Component import Component

from math import atan2, sqrt, pi, cos, sin
import pygame

class Resistor(Component):
    def __init__(self, ID_, internalResistance_, startPosition_=(0, 0), endPosition_=(100, 50)):
        Component.__init__(self, ID_)

        self.internalResistance = int(internalResistance_[:-1])
        if internalResistance_[-1] == 'k': # Kilo Ohm
            self.internalResistance *= 1000
        elif internalResistance_[-1] == 'M': # Mega Ohm
            self.internalResistance *= 1000000
        elif internalResistance_[-1] == 'G': # Giga Ohm
            self.internalResistance *= 1000000000
        # print(f"{self.ID}: {self.internalResistance} Ohm")

        self.nodePositions = [
            [int(startPosition_[0]), int(startPosition_[1])],
            [int(endPosition_[0]), int(endPosition_[1])]
        ]

        self.polygonRenderPositions = []
        
        self.updateNodePositions()

    def updateNodePositions(self):
        
        startEnd_dX = self.nodePositions[1][0] - self.nodePositions[0][0]
        startEnd_dY = self.nodePositions[1][1] - self.nodePositions[0][1]
        startEnd_theta = atan2(startEnd_dY, startEnd_dX)
        startEnd_dist  = sqrt((startEnd_dX**2) + (startEnd_dY**2))
        
        cornerOffsetX = (cos(startEnd_theta + (pi / 2)) * startEnd_dist * 0.05)
        cornerOffsetY = (sin(startEnd_theta + (pi / 2)) * startEnd_dist * 0.05)
        self.polygonRenderPositions = [
            (
                self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.25) - cornerOffsetX,
                self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.25) - cornerOffsetY
            ),
            (
                self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.75) - cornerOffsetX,
                self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.75) - cornerOffsetY
            ),
            (
                self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.75) + cornerOffsetX,
                self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.75) + cornerOffsetY
            ),
            (
                self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.25) + cornerOffsetX,
                self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.25) + cornerOffsetY
            )
        ]

        

    
    def render(self, display_, fillColour_=(187, 143, 102), renderThickness_=1):

        pygame.draw.line(
            display_, (0, 0, 0),
            self.nodePositions[0],
            self.nodePositions[1],
            renderThickness_
        )
        node1Col = 255 * int(self.nodeMoving[0])
        pygame.draw.circle(
            display_, (node1Col, node1Col, node1Col),
            self.nodePositions[0],
            int(renderThickness_ * 4)
        )
        node2Col = 255 * int(self.nodeMoving[1])
        pygame.draw.circle(
            display_, (node2Col, node2Col, node2Col),
            self.nodePositions[1],
            int(renderThickness_ * 4)
        )

        pygame.draw.polygon(
            display_, fillColour_,
            self.polygonRenderPositions, 0
        )