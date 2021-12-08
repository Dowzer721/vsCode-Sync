
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

# Using the "randint" function just to test versatility of the vehicle starting position:
from random import randint

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
    
    def toTuple(self):
        return (self.x, self.y)
    
    def toInt(self):
        return (int(self.x), int(self.y))
    
    # def copy(self):
    #     x = self.x
    #     y = self.y
    #     return Vector(x, y)

# Where the road starts, travels through and ends on the canvas:
roadPoints = [
    Vector(canvasW * 0.3, canvasH * 0.1),
    Vector(canvasW * 0.4, canvasH * 0.6),
    Vector(canvasW * 0.7, canvasH * 0.3),
    Vector(canvasW * 0.9, canvasH * 0.9),
    Vector(canvasW * 0.2, canvasH * 0.9),
    Vector(canvasW * 0.1, canvasH * 0.1)
]
# Creating this to save on calling the "len" method repeatedly:
roadPointsLen = len(roadPoints)

# The width of the road:
roadWidth = 16

# The colour of the road:
roadColour = (100, 100, 100)

# Draw the road to the canvas:
def renderRoad():
    for i in range(roadPointsLen):

        x1, y1 = roadPoints[i].toTuple()

        # pygame.draw.circle(
        #     canvas, 
        #     roadColour, 
        #     roadPoints[i].toInt(),
        #     roadWidth, 
        #     0
        # )
        # if i == roadPointsLen - 1: break


        x2, y2 = roadPoints[(i + 1) % roadPointsLen].toTuple()
        dx = x2 - x1
        dy = y2 - y1
        angle = atan2(dy, dx)
        pygame.draw.polygon(
            canvas, 
            roadColour, 
            [
                ( x1 + (cos(angle - (pi/2)) * roadWidth), y1 + (sin(angle - (pi/2)) * roadWidth) ),
                ( x2 + (cos(angle - (pi/2)) * roadWidth), y2 + (sin(angle - (pi/2)) * roadWidth) ),
                ( x2 + (cos(angle + (pi/2)) * roadWidth), y2 + (sin(angle + (pi/2)) * roadWidth) ),
                ( x1 + (cos(angle + (pi/2)) * roadWidth), y1 + (sin(angle + (pi/2)) * roadWidth) )
            ], 
            0
        )

    for i in range(roadPointsLen):
        pygame.draw.line(
            canvas, 
            (255,255,255), 
            roadPoints[i].toTuple(), 
            roadPoints[(i+1)%roadPointsLen].toTuple(), 
            1
        )

class Vehicle:
    def __init__(self):

        roadStartingIndex = randint(0, roadPointsLen - 1)
        previousIndex = (roadStartingIndex + roadPointsLen - 1) % roadPointsLen
        nextIndex = (roadStartingIndex + 1) % roadPointsLen

        # print(f"{previousIndex} : {roadStartingIndex} : {nextIndex}")

        previousRoadPoint = roadPoints[previousIndex]
        startingRoadPoint = roadPoints[roadStartingIndex]
        nextRoadPoint = roadPoints[nextIndex]

        anglesAwayFromStart = [
            atan2(startingRoadPoint.y - previousRoadPoint.y, startingRoadPoint.x - previousRoadPoint.x) + (2*pi),
            atan2(startingRoadPoint.y - nextRoadPoint.y, startingRoadPoint.x - nextRoadPoint.x) + (2*pi)
        ]

        angleMid = (anglesAwayFromStart[0] - anglesAwayFromStart[1]) / 2
        self.position = Vector(
            startingRoadPoint.x + (cos(angleMid) * roadWidth),
            startingRoadPoint.y + (sin(angleMid) * roadWidth)
        )

        # angleToStart = atan2(startingRoadPoint.y - previousRoadPoint.y, startingRoadPoint.x - previousRoadPoint.x) + (2 * pi)
        # angleFromStart=atan2(nextRoadPoint.y - startingRoadPoint.y, nextRoadPoint.x - startingRoadPoint.x) + (2 * pi)

        # angleToStart %= (2 * pi)
        # angleFromStart %= (2 * pi)
        
        # print(f"TO: {round(angleToStart,2)}, FROM: {round(angleFromStart,2)}")

        # angleHalved = angleToStart - angleFromStart
        # self.position = Vector(
        #     startingRoadPoint.x + (cos(angleHalved) * roadWidth),
        #     startingRoadPoint.y + (sin(angleHalved) * roadWidth)
        # )

        # startingRoadPoint = roadPoints[roadStartingIndex]
        # nextRoadPoint = roadPoints[(roadStartingIndex + 1) % roadPointsLen]

        # dx = nextRoadPoint.x - startingRoadPoint.x
        # dy = nextRoadPoint.y - startingRoadPoint.y
        # angleToNextRoadPoint = atan2(dy, dx)

        # startX = startingRoadPoint.x + (cos(angleToNextRoadPoint - (pi/2)) * roadWidth * 0.5 )
        # startY = startingRoadPoint.y + (sin(angleToNextRoadPoint - (pi/2)) * roadWidth * 0.5 )

        # self.position = Vector(startX, startY)
        # self.velocity = Vector.fromAngle(angleToNextRoadPoint)
        self.velocity = Vector.fromAngle(anglesAwayFromStart[1])
        self.acceleration = Vector(0,0)

        self.vehicleWidth = roadWidth * 0.4
        self.vehicleLength= roadWidth * 0.6

        # I am trying to find the angle between the centre of the vehicle to any one of the corners. 
        # I think I need to use atan2 along with the width and length of the vehicle, but I am not 100% yet.
        # cornerDx = self.position.x - 
        # self.centreToCornerAngle = atan2(1, 2) 
        self.centreToCornerAngle = atan2(self.vehicleWidth, self.vehicleLength)

    def render(self):
        
        vehicleDirection = self.velocity.heading()
        
        vehicleCornerLocations = [
            (
                self.position.x + (cos(vehicleDirection - self.centreToCornerAngle) * self.vehicleLength),
                self.position.y + (sin(vehicleDirection - self.centreToCornerAngle) * self.vehicleWidth)
            ),
            (
                self.position.x + (cos(vehicleDirection + self.centreToCornerAngle) * self.vehicleLength),
                self.position.y + (sin(vehicleDirection + self.centreToCornerAngle) * self.vehicleWidth)
            ),
            (
                self.position.x + (cos(vehicleDirection + pi - self.centreToCornerAngle) * self.vehicleLength),
                self.position.y + (sin(vehicleDirection + pi - self.centreToCornerAngle) * self.vehicleWidth)
            ),
            (
                self.position.x + (cos(vehicleDirection + pi + self.centreToCornerAngle) * self.vehicleLength),
                self.position.y + (sin(vehicleDirection + pi + self.centreToCornerAngle) * self.vehicleWidth)
            )
        ]

        pygame.draw.polygon(
            canvas, 
            (50, 200, 50), 
            vehicleCornerLocations, 
            0
        )
car = Vehicle()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONUP:
            car = Vehicle()

    canvas.fill((255, 255, 255))

    renderRoad()
    
    car.render()

    pygame.display.flip()