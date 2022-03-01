
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from copy import copy
from math import pi, cos, sin, atan2
from pygame import draw

class Vehicle:
    def __init__(self, pos_, dir_ =0, vel_ =1, rad_=8):
        self.position = pos_
        self.velocity = LL.Vector.fromAngle(dir_)
        self.velocity.mult(vel_)

        self.seekingIndex = 0
        self.seekPoint = (0,0)
        
        self.radius = rad_
    
    def findTarget(self, canvas, currentPath, nextPath, numberOfPathPoints, distanceAhead=100):
        Vx, Vy, _ = self.position.toInt()
        hdg = self.velocity.heading()

        Fx = Vx + (cos(hdg) * distanceAhead)
        Fy = Vy + (sin(hdg) * distanceAhead)

        # draw.circle(
        #     canvas, (255,0,0), (int(Fx), int(Fy)), 16, 0
        # )

        vectorToFuturePoint = LL.Vector(Fx-currentPath.start[0], Fy-currentPath.start[1])
        angleBetweenVectors = vectorToFuturePoint.angleBetween(currentPath.startToEndVector)

        normalisedPathVector = copy(currentPath.startToEndVector)
        normalisedPathVector.normalise()

        # seekX = currentPath.start[0] + (normalisedPathVector.x * cos(angleBetweenVectors))
        # seekY = currentPath.start[1] + (normalisedPathVector.y * cos(angleBetweenVectors))
        seekX = currentPath.start[0] + (cos(angleBetweenVectors) * vectorToFuturePoint.getMag())
        seekY = currentPath.start[1] + (sin(angleBetweenVectors) * vectorToFuturePoint.getMag())
        
        self.seekPoint = (seekX, seekY)

        draw.circle(
            canvas, (0,255,0), (int(seekX), int(seekY)), 16, 0
        )

        # Distance from seekPoint to next path start:
        dx = nextPath.start[0] - seekX
        dy = nextPath.start[1] - seekY
        dist = ((dx**2) + (dy**2)) ** 0.5

        if dist <= nextPath.pathWidth:
            self.seekingIndex = (self.seekingIndex + 1) % numberOfPathPoints

        

    def steerToSeekPoint(self):
        
        angleToSeekPoint = atan2(
            self.seekPoint[1] - self.position.y,
            self.seekPoint[0] - self.position.x
        )

        currentHeading = self.velocity.heading()
        dAngle = angleToSeekPoint - currentHeading

        # self.velocity.addAngle(dAngle * 0.1)

        self.velocity.rotateToAngle(angleToSeekPoint)

        # self.velocity = LL.Vector.fromAngle(angleToSeekPoint)
    
    def move(self):
        self.position.add(self.velocity)

    
    def render(self, canvas, colour=(0,0,0), thickness=1, showSeekPoint=True):
        x1, y1, _ = self.position.toInt()
        hdg = self.velocity.heading()
        draw.polygon(
            canvas, colour,
            [
                (x1 + int(cos(hdg) * self.radius), y1 + int(sin(hdg) * self.radius)),
                (x1 + int(cos(hdg+pi*0.75) * self.radius * 0.75), y1 + int(sin(hdg+pi*0.75) * self.radius * 0.75) ),
                (x1, y1),
                (x1 + int(cos(hdg+pi*1.25) * self.radius * 0.75), y1 + int(sin(hdg+pi*1.25) * self.radius * 0.75) )
            ], thickness
        )

        if showSeekPoint:
            draw.line(
                canvas, (200,0,0),
                (x1, y1), self.seekPoint, thickness*2
            )