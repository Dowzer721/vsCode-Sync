
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import math
import pygame

class Path:
    def __init__(self, nodeCount_, smoothCount_, screenW_, screenH_):
        self.nodeCount = nodeCount_
        
        self.noise = Luke.generate1DNoise(nodeCount_, smoothCount=smoothCount_)
        self.nodes = []
        self.pathWidth = 50
        self.generateNodePositions(screenW_, screenH_)
    
    def generateNodePositions(self, screenW=-1, screenH=-1):
        self.nodes.clear()
        
        centerPos = []
        outerPos = []
        innerPos = []

        for c in range(self.nodeCount):
            theta = (math.pi * 2.0 / self.nodeCount) * c
            
            pathCenterRadiusX = (self.noise[c] * screenW * 0.6)
            pathCenterRadiusY = (self.noise[c] * screenH * 0.6)
            pathCenterX = (screenW / 2) + (math.cos(theta) * pathCenterRadiusX)
            pathCenterY = (screenH / 2) + (math.sin(theta) * pathCenterRadiusY)
            centerPos.append(Luke.Vector(pathCenterX, pathCenterY))

            pathOuterRadiusX = pathCenterRadiusX + (self.pathWidth/2)
            pathOuterRadiusY = pathCenterRadiusY + (self.pathWidth/2)
            pathOuterX = (screenW / 2) + (math.cos(theta) * pathOuterRadiusX)
            pathOuterY = (screenH / 2) + (math.sin(theta) * pathOuterRadiusY)
            outerPos.append(Luke.Vector(pathOuterX, pathOuterY))

            pathInnerRadiusX = pathCenterRadiusX - (self.pathWidth/2)
            pathInnerRadiusY = pathCenterRadiusY - (self.pathWidth/2)
            pathInnerX = (screenW / 2) + (math.cos(theta) * pathInnerRadiusX)
            pathInnerY = (screenH / 2) + (math.sin(theta) * pathInnerRadiusY)
            innerPos.append(Luke.Vector(pathInnerX, pathInnerY))
        
        # self.nodes.extend(centerPos)
        self.nodes.extend(outerPos)
        self.nodes.extend(innerPos)
    
    def display(self, screen_, colour=(0, 0, 0), thickness=1):
        
        totalNodeCount = len(self.nodes)
        for c in range(0, int(totalNodeCount / 2)):
            n = (c + 1) % int(totalNodeCount / 2)

            x1 = int(self.nodes[c].x)
            y1 = int(self.nodes[c].y)
            x2 = int(self.nodes[n].x)
            y2 = int(self.nodes[n].y)

            pygame.draw.line(
                screen_, colour,
                (x1, y1), (x2, y2),
                thickness
            )

            x3 = int(self.nodes[c+int(totalNodeCount/2)].x)
            y3 = int(self.nodes[c+int(totalNodeCount/2)].y)
            x4 = int(self.nodes[n+int(totalNodeCount/2)].x)
            y4 = int(self.nodes[n+int(totalNodeCount/2)].y)

            pygame.draw.line(
                screen_, colour,
                (x3, y3), (x4, y4),
                thickness
            )


