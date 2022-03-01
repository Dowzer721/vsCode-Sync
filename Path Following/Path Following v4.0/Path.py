
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin
from pygame import draw

class PathSection:
    def __init__(self, start_, end_, pathWidth_ =20):

        self.start = start_
        self.end = end_

        # Line coefficients: 
        # self.a, self.b, self.c = LL.LineCoefficientsFromTwoPoints(start_, end_)

        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        self.startToEndVector = LL.Vector(dx, dy)

        self.pathWidth = pathWidth_

        pathHeading = self.startToEndVector.heading()
        self.pathRenderCorners = [
            (
                self.start[0] + (cos(pathHeading - (pi/2)) * pathWidth_ / 2),
                self.start[1] + (sin(pathHeading - (pi/2)) * pathWidth_ / 2)
            ),
            (
                self.end[0] + (cos(pathHeading - (pi/2)) * pathWidth_ / 2),
                self.end[1] + (sin(pathHeading - (pi/2)) * pathWidth_ / 2)
            ),
            (
                self.end[0] + (cos(pathHeading + (pi/2)) * pathWidth_ / 2),
                self.end[1] + (sin(pathHeading + (pi/2)) * pathWidth_ / 2)
            ),
            (
                self.start[0] + (cos(pathHeading + (pi/2)) * pathWidth_ / 2),
                self.start[1] + (sin(pathHeading + (pi/2)) * pathWidth_ / 2)
            )
        ]
    
    def render(self, canvas_, colour_=(150, 150, 150), renderMid=False):
        if not renderMid:
            draw.polygon(canvas_, colour_, self.pathRenderCorners, 0)
            draw.circle(canvas_, colour_, self.start, self.pathWidth//2, 0)
        else:
            draw.line(canvas_, (0,0,0), self.start, self.end, 4)