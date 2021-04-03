
from Component import Component

from math import atan2, sqrt, cos, sin, pi
import pygame

class Cell(Component):
    def __init__(self, ID_="", Voltage_=9, startPosition_=(100, 100), endPosition_=(125, 100)):
        Component.__init__(self, ID_, 2)

        self.outputVoltage = Voltage_

        self.nodePositions = [
            [int(startPosition_[0]), int(startPosition_[1])],
            [int(endPosition_[0]), int(endPosition_[1])]
        ]
    
    def render(self, display_, renderColour_=(0, 0, 0), renderThickness_=1):

        startEnd_dX = self.nodePositions[1][0] - self.nodePositions[0][0]
        startEnd_dY = self.nodePositions[1][1] - self.nodePositions[0][1]
        startEnd_theta = atan2(startEnd_dY, startEnd_dX)
        startEnd_dist  = sqrt((startEnd_dX**2) + (startEnd_dY**2))

        negativeTerminalPosition = (
            self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.45),
            self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.45)
        )
        positiveTerminalPosition = (
            self.nodePositions[0][0] + (cos(startEnd_theta) * startEnd_dist * 0.55),
            self.nodePositions[0][1] + (sin(startEnd_theta) * startEnd_dist * 0.55)
        )

        # Drawing the first node:
        node1Col = 255 * int(self.nodeMoving[0])
        pygame.draw.circle(
            display_, (node1Col, node1Col, node1Col),
            self.nodePositions[0],
            int(renderThickness_ * 4),
            0
        )
        
        # Drawing the line from the first node to the negative terminal:
        pygame.draw.line(
            display_, renderColour_,
            self.nodePositions[0],
            negativeTerminalPosition,
            renderThickness_
        )

        # Drawing the negative terminal line:
        pygame.draw.line(
            display_, renderColour_,
            (
                negativeTerminalPosition[0] + (cos(startEnd_theta + (pi/2)) * startEnd_dist * 0.2),
                negativeTerminalPosition[1] + (sin(startEnd_theta + (pi/2)) * startEnd_dist * 0.2)
            ),
            (
                negativeTerminalPosition[0] + (cos(startEnd_theta - (pi/2)) * startEnd_dist * 0.2),
                negativeTerminalPosition[1] + (sin(startEnd_theta - (pi/2)) * startEnd_dist * 0.2)
            ),
            renderThickness_
        )

        # Drawing the negative symbol:
        pygame.draw.line(
            display_, renderColour_, 
            (
                negativeTerminalPosition[0] + (cos(startEnd_theta + (pi*0.75)) * startEnd_dist * 0.2) + (cos(startEnd_theta) * startEnd_dist * 0.05),
                negativeTerminalPosition[1] + (sin(startEnd_theta + (pi*0.75)) * startEnd_dist * 0.2) + (sin(startEnd_theta) * startEnd_dist * 0.05)
            ),
            (
                negativeTerminalPosition[0] + (cos(startEnd_theta + (pi*0.75)) * startEnd_dist * 0.2) - (cos(startEnd_theta) * startEnd_dist * 0.05),
                negativeTerminalPosition[1] + (sin(startEnd_theta + (pi*0.75)) * startEnd_dist * 0.2) - (sin(startEnd_theta) * startEnd_dist * 0.05)
            ),
            1
        )

        # Drawing the positive symbol:
        pygame.draw.line(
            display_, renderColour_,
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) + (cos(startEnd_theta) * startEnd_dist * 0.05),
                positiveTerminalPosition[1] + (sin(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) + (sin(startEnd_theta) * startEnd_dist * 0.05)
            ),
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) - (cos(startEnd_theta) * startEnd_dist * 0.05),
                positiveTerminalPosition[1] + (sin(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) - (sin(startEnd_theta) * startEnd_dist * 0.05)
            ),
            1
        )
        pygame.draw.line(
            display_, renderColour_,
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) + (cos(startEnd_theta + (pi/2)) * startEnd_dist * 0.05),
                positiveTerminalPosition[1] + (sin(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) + (sin(startEnd_theta + (pi/2)) * startEnd_dist * 0.05)
            ),
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) - (cos(startEnd_theta + (pi/2)) * startEnd_dist * 0.05),
                positiveTerminalPosition[1] + (sin(startEnd_theta + (pi*0.25)) * startEnd_dist * 0.2) - (sin(startEnd_theta + (pi/2)) * startEnd_dist * 0.05)
            ),
            1
        )

        # Drawing the positive terminal line:
        pygame.draw.line(
            display_, renderColour_,
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta + (pi/2)) * startEnd_dist * 0.4),
                positiveTerminalPosition[1] + (sin(startEnd_theta + (pi/2)) * startEnd_dist * 0.4)
            ),
            (
                positiveTerminalPosition[0] + (cos(startEnd_theta - (pi/2)) * startEnd_dist * 0.4),
                positiveTerminalPosition[1] + (sin(startEnd_theta - (pi/2)) * startEnd_dist * 0.4)
            ),
            renderThickness_
        )
        
        # Drawing the line from the positive terminal to the first node:
        pygame.draw.line(
            display_, renderColour_,
            positiveTerminalPosition,
            self.nodePositions[1],
            renderThickness_
        )

        # Drawing the second node:
        node2Col = 255 * int(self.nodeMoving[1])
        pygame.draw.circle(
            display_, (node2Col, node2Col, node2Col),
            self.nodePositions[1],
            int(renderThickness_ * 4),
            0
        )