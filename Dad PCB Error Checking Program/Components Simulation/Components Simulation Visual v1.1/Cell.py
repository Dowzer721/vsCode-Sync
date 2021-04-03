
from Component import Component

from math import atan2, cos, sin, pi
import pygame

class Cell(Component):
    def __init__(self, ID_, Voltage_, nodePositions_=[[-1,-1], [-1,-1]]):
        Component.__init__(self, ID_, 2)
        self.ID = ID_
        self.Voltage = Voltage_
        
        self.Nodes[0].position = nodePositions_[0]
        self.Nodes[1].position = nodePositions_[1]
    
    def render(self, display_, renderColour=(0, 0, 0)):

        # Draw Node0
        self.Nodes[0].render(display_)

        x1 = int(self.Nodes[0].position[0])
        y1 = int(self.Nodes[0].position[1])
        x2 = int(self.Nodes[1].position[0])
        y2 = int(self.Nodes[1].position[1])

        startEndDx = x2 - x1
        startEndDy = y2 - y1
        startEndDist = ((startEndDx ** 2) + (startEndDy ** 2)) ** 0.5
        startEndTheta = atan2(startEndDy, startEndDx)

        # Line from Node0 to symbol mid
        pygame.draw.line(
            display_, renderColour,
            (x1, y1),
            (
                x1 + int(cos(startEndTheta) * startEndDist * 0.45),
                y1 + int(sin(startEndTheta) * startEndDist * 0.45)
            ), 1
        )

        # Line from symbol mid to Node1
        pygame.draw.line(
            display_, renderColour,
            (x2, y2),
            (
                x2 - int(cos(startEndTheta) * startEndDist * 0.45),
                y2 - int(sin(startEndTheta) * startEndDist * 0.45)
            ), 1
        )

        # Draw Node1
        self.Nodes[1].render(display_)
