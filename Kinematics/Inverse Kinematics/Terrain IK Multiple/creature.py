
from leg import Leg

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
from LukeLibrary import Wall, randomFloat

from math import pi

from pygame import draw

class Creature:
    def __init__(self, position_=[50, 50], numberOfLegs_=2, numberOfSegmentsPerLeg_=2, lengthOfEachLegSegment_=100, legsOffset_=0, bodyWidth_=250, bodyHeight_=100):

        self.position = position_
        self.bodyWidth = bodyWidth_
        self.bodyHeight = bodyHeight_

        legPositions = [
            (
                position_[0] + legsOffset_ + (((self.bodyWidth-(legsOffset_*2)) / (numberOfLegs_-1)) * i),
                position_[1] + self.bodyHeight
            )
            for i in range(numberOfLegs_)
        ]
        # print(legPositions)

        legSeekAngles = [
            pi * randomFloat(0.25, 0.4)
            for _ in range(numberOfLegs_)
        ]

        # (segmentCount_=3, segmentLength_=50, maximumReachDistanceMultiplier_=1.0, basePosition_=None, legMovementSpeed_=0.01, targetSeekAngle_=pi*0.25)
        self.legs = [
            Leg(numberOfSegmentsPerLeg_, lengthOfEachLegSegment_, 0.9, legPositions[leg], targetSeekAngle_=legSeekAngles[leg])
            # for legPos in legPositions
            for leg in range(numberOfLegs_)
        ]

        # for L in self.legs:
        #     print(f"L.basePos:{L.basePosition}")
    
    def updateLegs(self, terrainPoints_, terrainMovementSpeed_):

        wallList = []
        terrainLength = len(terrainPoints_)
        for c in range(terrainLength-1):
            x1, y1 = terrainPoints_[c]
            x2, y2 = terrainPoints_[c + 1]

            wallList.append( Wall(x1, y1, x2, y2) )
        
        for L in self.legs:

            if L.reachedTargetPosition == False:
                L.findNewTargetPosition(wallList)

            else:
                # Move the target position along with the terrain:
                L.targetPosition[0] -= terrainMovementSpeed_
            
            # If the target has gone past where the arm can reach, 
            # find a new target ahead of the robot body:
            if L.targetPositionOutOfReach():
                L.reachedTargetPosition = False
                L.findNewTargetPosition(wallList)
            
            L.reachForTarget()

    def render(self, renderLocation_, renderColour_=(0,0,0), legRenderColour_=(100,100,100)):
        
        bodyCorners = [
            self.position,
            [self.position[0] + self.bodyWidth, self.position[1]],
            [self.position[0] + (self.bodyWidth*1.1), self.position[1] + (self.bodyHeight/2)],
            [self.position[0] + self.bodyWidth, self.position[1] + self.bodyHeight],
            [self.position[0], self.position[1] + self.bodyHeight],
            [self.position[0] + (self.bodyWidth*0.1), self.position[1] + (self.bodyHeight/2)],
        ]

        draw.polygon(renderLocation_, renderColour_, bodyCorners, 0)
        for L in self.legs:
            # (renderLocation_, renderColour_, showTarget_=False)
            L.render(renderLocation_, legRenderColour_)


# c = Creature([0,0], 3, 10)