
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
from LukeLibrary import randomFloat

from math import pi, cos, sin, atan2

from pygame import draw

class Arm:
    def __init__(self, basePosition_, segmentCount_=2, segmentLength_=50, renderLocation_=None):

        self.basePosition, self.segmentCount, self.segmentLength = basePosition_, segmentCount_, segmentLength_
        
        self.starts = [[0,0] for _ in range(segmentCount_)]
        self.ends = [[0,0] for _ in range(segmentCount_)]

        self.startingAngles = [
            pi * 1.75,
            pi * 1.25,
            pi * 1.5
        ]
        self.currentAngles = [
            self.startingAngles[a]
            for a in range(segmentCount_)
        ]
        self.finalAngles = [
            pi * randomFloat(0.0, 2.0)
            for _ in range(segmentCount_)
        ]
        # self.finalAngles = [
        #     pi * 1.74,
        #     pi * 1.24,
        #     pi * 2.49
        # ]
        # self.finalAngles = [
        #     pi * 0.75,
        #     pi * 0.25,
        #     pi * 0.5
        # ]

        # print(self.startingAngles)
        # print(self.finalAngles)

        self.movementMultiplier = randomFloat(0.0, 0.01, 4)

        self.setStartEnds()

        self.renderLocation = renderLocation_
    
    def setStartEnds(self):
        self.starts[0] = self.basePosition
        for i in range(self.segmentCount):
            self.ends[i] = [
                self.starts[i][0] + (cos(self.currentAngles[i]) * self.segmentLength),
                self.starts[i][1] + (sin(self.currentAngles[i]) * self.segmentLength)
            ]
            if i < self.segmentCount-1:
                self.starts[i+1] = self.ends[i]
        
        # print(self.ends[-1])
    
    def rotateJoints(self, showVelocity_=False):
        x1, y1 = self.ends[-1]
        for a in range(self.segmentCount):
            deltaAngle = self.finalAngles[a] - self.currentAngles[a]
            self.currentAngles[a] += (deltaAngle * self.movementMultiplier)
        
        self.setStartEnds()
        
        if showVelocity_:
            x2, y2 = self.ends[-1]
            dx = x2 - x1
            dy = y2 - y1
            angle = atan2(dy, dx)

            mag = sum([
                abs(self.startingAngles[a] - self.finalAngles[a])
                for a in range(self.segmentCount)
            ])
            # print(mag)

            velX1, velY1 = x2, y2
            velX2 = x2 + int(cos(angle) * self.segmentLength * mag)
            velY2 = y2 + int(sin(angle) * self.segmentLength * mag)

            draw.line(
                self.renderLocation,
                (0, 200, 0),
                (velX1, velY1),
                (velX2, velY2),
                1
            )

    
    def render(self, renderColour_=(0,0,0)):
        for start, end, t in zip(self.starts, self.ends, list(range(self.segmentCount))):
            x1 = int(start[0])
            y1 = int(start[1])
            x2 = int(end[0])
            y2 = int(end[1])
            draw.line(self.renderLocation, renderColour_, (x1,y1), (x2,y2), self.segmentCount-t)

# (basePosition_, segmentCount_=2, segmentLength_=50, renderLocation_=None)
# a = Arm([100, 100])
# a.rotateJoints(showVelocity_=True)
