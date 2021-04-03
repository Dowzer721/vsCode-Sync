
from Component import Component

from math import atan2, sqrt, cos, sin
import pygame

class Wire(Component):
    def __init__(self, nodeCount_=2, newNodePositions_=[(0, 0), (50, 50)]):
        Component.__init__(self, "", nodeCount_)

        self.nodeCount = nodeCount_

        if nodeCount_ == 2:
            self.nodePositions = newNodePositions_
        else:
            startEnd_dX = newNodePositions_[-1][0] - newNodePositions_[0][0]
            startEnd_dY = newNodePositions_[-1][1] - newNodePositions_[0][1]
            startEnd_theta = atan2(startEnd_dY, startEnd_dX)
            segmentLength  = sqrt((startEnd_dX**2) + (startEnd_dY**2)) / float(nodeCount_ - 1)
            # print(f"s: {startPosition}, e: {endPosition}, n: {nodeCount_}, L: {segmentLength}")

            for node in range(nodeCount_):
                x = round( newNodePositions_[0][0] + (cos(startEnd_theta) * segmentLength * node) )
                y = round( newNodePositions_[0][1] + (sin(startEnd_theta) * segmentLength * node) )
                self.nodePositions.append([x, y])
            # print(self.nodePositions)

        self.nodeMoving = [False for _ in range(nodeCount_)]

    
    def addNode(self):
        self.__init__(self.nodeCount + 1, self.nodePositions)



    def render(self, display_, renderColour_=(0, 0, 0), renderThickness_=1):
        
        for c in range(self.nodeCount):
            
            x1 = int(self.nodePositions[c][0])
            y1 = int(self.nodePositions[c][1])

            node1Col = 255 * int(self.nodeMoving[c])
            pygame.draw.circle(
                display_, (node1Col, node1Col, node1Col),
                (x1, y1), int(renderThickness_ * 4),
                0
            )

            if c < self.nodeCount-1:
                x2 = int(self.nodePositions[c+1][0])
                y2 = int(self.nodePositions[c+1][1])
                # print(f"({x1}, {y1}) -> ({x2}, {y2})")
                
                node2Col = 255 * int(self.nodeMoving[c+1])
                pygame.draw.circle(
                    display_, (node2Col, node2Col, node2Col),
                    (x2, y2), int(renderThickness_ * 4),
                    0
                )
                
                pygame.draw.line(
                    display_, renderColour_,
                    (x1, y1), (x2, y2),
                    renderThickness_
                )

                


# w = Wire(2)
# w.addNode()
# w.render(pygame.display.set_mode((500, 500)))
