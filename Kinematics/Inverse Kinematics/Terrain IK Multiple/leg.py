
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, atan2, cos, sin

from pygame import draw

class Leg:
    def __init__(self, segmentCount_=3, segmentLength_=50, maximumReachDistanceMultiplier_=1.0, basePosition_=None, legMovementSpeed_=0.01, targetSeekAngle_=pi*0.25):
        self.segmentCount = segmentCount_
        self.segmentLength = segmentLength_
        self.basePosition = basePosition_
        self.legMovementSpeed = legMovementSpeed_

        self.starts = [[0,0] for _ in range(segmentCount_)]
        self.ends = [[0,0] for _ in range(segmentCount_)]

        self.targetPosition = [0, 0]
        self.reachedTargetPosition = False

        self.targetSeekAngle = targetSeekAngle_
        self.maximumReachDistance = segmentCount_ * segmentLength_ * maximumReachDistanceMultiplier_
    
    def targetPositionOutOfReach(self):
        dx = self.targetPosition[0] - self.basePosition[0]
        dy = self.targetPosition[1] - self.basePosition[1]
        distanceToTarget = ((dx**2) + (dy**2)) ** 0.5
        return distanceToTarget > self.maximumReachDistance

    def findNewTargetPosition(self, sensorWallList_, Surface_=None):

        rayStartingPosition = LL.Vector(
            self.basePosition[0] + (cos(self.targetSeekAngle) * self.maximumReachDistance * 0.9),
            self.basePosition[1]
        )

        if Surface_ != None:
            pass # draw.circle
        
        ray = LL.Sensor()
        ray.update(rayStartingPosition, pi * 0.5)
        measuredDistance = ray.measure(sensorWallList_)

        if measuredDistance == -1:
            return False
        
        self.targetPosition = [
            rayStartingPosition.x,
            rayStartingPosition.y + measuredDistance
        ]
    
    def reachForTarget(self, lockToBase_=True):

        for s in range(self.segmentCount):
            if s == 0:
                if self.reachedTargetPosition:
                    x1, y1 = self.targetPosition
                else:
                    tgtDx = self.targetPosition[0] - self.ends[0][0]
                    tgtDy = self.targetPosition[1] - self.ends[0][1]
                    angle = atan2(tgtDy, tgtDx)
                    dist = ((tgtDx**2) + (tgtDy**2)) ** 0.5
                    if dist <= 8:
                        self.reachedTargetPosition = True
                        return
                    
                    x1 = self.ends[0][0] + (cos(angle) * dist * self.legMovementSpeed)
                    y1 = self.ends[0][1] + (sin(angle) * dist * self.legMovementSpeed)
            else:
                x1, y1 = self.starts[s-1]
            
            dx = self.starts[s][0] - x1
            dy = self.starts[s][1] - y1
            angle = atan2(dy, dx)

            self.starts[s] = [
                x1 + (cos(angle) * self.segmentLength),
                y1 + (sin(angle) * self.segmentLength)
            ]
            self.ends[s] = [x1, y1]
        
        if lockToBase_:
            # Lock the arm to the base position:
            totalDx = self.starts[-1][0] - self.basePosition[0]
            totalDy = self.starts[-1][1] - self.basePosition[1]

            for s in range(self.segmentCount):
                self.starts[s][0] -= totalDx
                self.starts[s][1] -= totalDy
                self.ends[s][0] -= totalDx
                self.ends[s][1] -= totalDy
        
    def render(self, renderLocation_, renderColour_, showTarget_=False):

        for s in range(self.segmentCount):

            x1 = int( self.starts[s][0] )
            y1 = int( self.starts[s][1] )
            x2 = int( self.ends[s][0] )
            y2 = int( self.ends[s][1] )

            renderThickness = (s + 1) * 2

            draw.line(
                renderLocation_,
                renderColour_,
                (x1, y1), (x2, y2),
                renderThickness
            )

        if showTarget_:
            draw.circle(
                renderLocation_,
                (150, 200, 150),
                (
                    int( self.targetPosition[0] ),
                    int( self.targetPosition[1] )
                ),
                4, 0
            )