
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "4, 32"

import math
import pygame
# import random

screenW = 800
screenH = 500
screenD = math.sqrt((screenW**2.0)+(screenH**2.0))
screen = pygame.display.set_mode((screenW, screenH))

pathNodeCount = 64
pathTurnCount = 5 # Frequency of sin wave
pathTurnSize  = (screenD / 8) # Amplitude of sin wave
pathAngle = math.atan2(screenW, screenH)
pathAngleVector = Luke.Vector().fromAngle(pathAngle)
pathWidth = 35

pathTheta = 0.0
class Path:
    def __init__(self):
        self.leftWallNodes  = [Luke.Vector() for _ in range(pathNodeCount)]
        self.rightWallNodes = [Luke.Vector() for _ in range(pathNodeCount)]
        self.centerNodes = [Luke.Vector() for _ in range(pathNodeCount)]
        self.generateNodePositions()
    def generateNodePositions(self, startingTheta_=None):
        
        for c in range(pathNodeCount):
            theta = ((math.pi * pathTurnCount) / pathNodeCount) * c
            if startingTheta_ != None:
                theta += startingTheta_
            
            # Original Point
            # x = (screenW / pathNodeCount) * c
            x = (screenW / 2) + ((screenW / pathNodeCount) * (c - (pathNodeCount/2)) )
            y = (screenH/2) + (math.sin(theta) * pathTurnSize)

            # Translated Point to rotation origin
            tX = x - (screenW / 2)
            tY = y - (screenH / 2)

            # Rotated Point around origin
            # sin / cos are swapped, as the scene origin in top left corner, and positive x is right, positive y in down.
            rX = (math.sin(pathAngle) * tX) - (math.cos(pathAngle) * tY)
            rY = (math.cos(pathAngle) * tX) + (math.sin(pathAngle) * tY)

            # # Point translated back to rotation origin
            rX += (screenW / 2)
            rY += (screenH / 2)

            self.centerNodes[c].x = rX
            self.centerNodes[c].y = rY
            # self.nodes[c].x = rX
            # self.nodes[c].y = rY
        
        prevTheta = 0.0
        for c in range(pathNodeCount):
            n = (c + 1)
            
            # Center nodes:
            Cx1 = self.centerNodes[c].x
            Cy1 = self.centerNodes[c].y
            
            Ctheta = 0.0
            if n == pathNodeCount:
                Ctheta = prevTheta
            else:
                Cx2 = self.centerNodes[n].x
                Cy2 = self.centerNodes[n].y
                Ctheta = math.atan2(Cy2 - Cy1, Cx2 - Cx1)
                prevTheta = Ctheta

            # Left wall first:
            self.leftWallNodes[c].x = Cx1 + (math.cos(Ctheta - (math.pi / 2)) * (pathWidth / 2))
            self.leftWallNodes[c].y = Cy1 + (math.sin(Ctheta - (math.pi / 2)) * (pathWidth / 2))

            # And the right:
            self.rightWallNodes[c].x = Cx1 + (math.cos(Ctheta + (math.pi / 2)) * (pathWidth / 2))
            self.rightWallNodes[c].y = Cy1 + (math.sin(Ctheta + (math.pi / 2)) * (pathWidth / 2))


    def display(self):
        for c in range(pathNodeCount-1):
            n = (c + 1)
            
            # Center line:
            pygame.draw.line(
                screen, (100, 100, 100),
                (self.centerNodes[c].x, self.centerNodes[c].y), 
                (self.centerNodes[n].x, self.centerNodes[n].y),
                2
            )

            # Left wall:
            pygame.draw.line(
                screen, (200, 0, 0),
                (self.leftWallNodes[c].x, self.leftWallNodes[c].y),
                (self.leftWallNodes[n].x, self.leftWallNodes[n].y),
                4
            )

            # Right wall:
            pygame.draw.line(
                screen, (200, 0, 0),
                (self.rightWallNodes[c].x, self.rightWallNodes[c].y),
                (self.rightWallNodes[n].x, self.rightWallNodes[n].y),
                4
            )



path = Path()

vehicleRadius = int(pathWidth * 0.4)
class Vehicle:
    def __init__(self):
        x = screenW * 0.2
        y = screenH * 0.1
        self.position = Luke.Vector(x, y)
        self.velocity = Luke.Vector().fromAngle(Luke.randomFloat(math.pi * 0.1, math.pi * 0.4))

        self.radius = int(pathWidth * 0.4)

        self.kP = 0.01
        self.kI = 0.1
        self.kD = 0.05

        self.P = self.I = self.D = 0.0

    def runPID(self):
        pass
        # e = (leftSensor.dist - rightSensor.dist) # ???
        # P = kP * e
        # I = I + (e * iteration_time)
        # D = (e - e_prior) / iteration_time
        # output = (kP * e) + (kI * I) + (kD * D)

    def display(self):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, (0, 0, 0),
            (x1, y1), 
            self.radius, 1
        )
        
        dir = self.velocity.heading()
        x2 = x1 + int(math.cos(dir) * self.radius)
        y2 = y1 + int(math.sin(dir) * self.radius)
        pygame.draw.line(
            screen, (0, 0, 0),
            (x1, y1), (x2, y2),
            1
        )

    class Sensor:
        def __init__(self):
            self.pos = Luke.Vector()
            self.dir = 0.0
            self.measuredDistance = -1.0
        def measure(self):
            pass
Mouse = Vehicle()


def restart():
    global Mouse, path
    Mouse = Vehicle()
    path = Path()
restart()

frameCount = 0
simRunning = True
while simRunning:
    screen.fill((255, 255, 255))

    frameCountTheta = ((math.pi * pathTurnCount) / pathNodeCount) * frameCount * 0.01

    path.display()
    Mouse.display()

    # mouseVelocityInPathDirection = Mouse.velocity.dot(pathAngleVector)
    # path.generateNodePositions(mouseVelocityInPathDirection)

    angleDiff = math.pi - (pathAngle - Mouse.velocity.heading())
    # path.generateNodePositions(angleDiff)

    path.generateNodePositions(angleDiff)
    

    pygame.draw.line(
        screen, (100, 100, 100),
        (0, 0), 
        (math.sin(pathAngle) * screenD * 0.9, math.cos(pathAngle) * screenD * 0.9),
        1
    )

    mouseDir = Mouse.velocity.heading()
    pygame.draw.line(
        screen, (100, 255, 100),
        (0, 0),
        (math.cos(mouseDir) * 250, math.sin(mouseDir) * 250),
        2
    )

    pygame.display.flip()

    frameCount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # path = Path(nodeCount)
                restart()
                continue

            if event.key == pygame.K_a:
                dir = Mouse.velocity.heading()
                Mouse.velocity.rotateToAngle(dir - 0.1)
            if event.key == pygame.K_d:
                dir = Mouse.velocity.heading()
                Mouse.velocity.rotateToAngle(dir + 0.1)
            

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                simRunning = False
    
    a = 1