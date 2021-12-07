
# I am going to create a start and end point for a road, and maybe an intermediate point for the road 
# to pass through, and then have a vehicle drive up and down this road. 
# 
# I am not too bothered about the actual visuals at this time; a green rectangle for the car 
# will suffice. Graphics and proper animations are something which I will work on much later on. 

# I am using pygame for the graphics. 
# There are likely much better libraries for this project, which I may discover at a later date, 
# but for now this works. I am also used to pygame and how it works, so I am comfortable setting 
# it up and working with it, meaning I can focus on the base scope of this portion of work, 
# instead of diagnosing graphical issues.
import pygame
canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

# Using some basic trigonometry functions from "math".
from math import cos, sin, atan2, pi

# I am creating a "Vector" class here, because I will need to handle position, velocity and acceleration 
# for the vehicle, and I am going to attempt to use as little external libraries as possible. 
# Yes I have used "pygame" and "math", but that is because they are covering tasks which are not within 
# the scope of this portion of the project.
class Vector:
    def __init__(self, x_=0.0, y_=0.0):
        self.x, self.y = x_, y_
    
    @staticmethod
    def fromAngle(angle):
        return Vector(cos(angle), sin(angle))
    
    def heading(self):
        return atan2(self.y, self.x)
    
    # def copy(self):
    #     x = self.x
    #     y = self.y
    #     return Vector(x, y)

# Where the road starts, travels through and ends on the canvas:
roadStartingPosition = Vector(
    int(canvasW * 0.1),
    int(canvasH * 0.1)
)
roadIntermediatePositions = [
    Vector(canvasW * 0.6, canvasH * 0.3)
]
roadEndingPosition = Vector(
    int(canvasW * 0.9),
    int(canvasH * 0.9)
)

# The width of the road:
roadWidth = 16

class Vehicle:
    def __init__(self):
        self.position = roadStartingPosition
        self.velocity = Vector(0,0)
        self.acceleration = Vector(0,0)

        self.vehicleWidth = roadWidth * 0.4
        self.vehicleLength= roadWidth * 0.8

        # I am trying to find the angle between the centre of the vehicle to any one of the corners. 
        # I think I need to use atan2 along with the width and length of the vehicle, but I am not 100% yet.
        cornerDx = self.position.x - 

    def render(self):
        
        vehicleDirection = self.velocity.heading()
        for i in range(4):
            angle = vehicleDirection - (pi * )

        pygame.draw.polygon(
            canvas, 
            (100, 255, 100), 
            pointlist, 
            0
        )
        