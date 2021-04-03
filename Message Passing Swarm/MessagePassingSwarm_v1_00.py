
# from LukeLibrary import *
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as Luke

import math
import pygame
import time

pygame.display.init()
screenW = 500
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

def delay(seconds_):
    startTime = time.time()
    while time.time() < (startTime + seconds_):
        pass

class Vehicle:
    def __init__(self):
        x = int(Luke.randomFloat(screenW*0.1, screenW*0.9))
        y = int(Luke.randomFloat(screenH*0.1, screenH*0.9))
        self.position = Luke.Vector(x, y)

        dir = Luke.randomFloat(0.0, math.pi * 2.0)
        self.velocity = Luke.Vector().fromAngle(dir)
        self.velocity.normalise(0.0, 0.1)
        # print(self.velocity.getMag())

        self.radius = 2

    def display(self, circleColour, lineColour):
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        dir = self.velocity.heading()
        pygame.draw.circle(
            screen, circleColour,
            (x1, y1), self.radius,
            2
        )
        x2 = int(x1 + (math.cos(dir) * self.radius) )
        y2 = int(y1 + (math.sin(dir) * self.radius) )
        pygame.draw.line(
            screen, lineColour,
            (x1, y1),
            (x2, y2),
            2
        )
    
    def move(self):
        self.position.add(self.velocity)
        self.position.limitX(screenW*0.1, screenW*0.9)
        self.position.limitY(screenH*0.1, screenH*0.9)

class hubVehicle(Vehicle):
    def __init__(self):
        Vehicle.__init__(self)
        
        self.radius = 20
    
    def sendMessage(self, msgString_, childArray):
        for child in childArray:
            dist = self.position.distance(child.position)
            angle = self.position.angleBetween(child.position)

            x1 = int(self.position.x)
            y1 = int(self.position.y)
            x2 = int( x1 + (math.cos(angle) * dist * 0.75))
            y2 = int( y1 + (math.sin(angle) * dist * 0.75))

            pygame.draw.line(
                screen, (255, 100, 100),
                (x1, y1), (x2, y2),
                2
            )

            try:
                # Attempt to send the message to each child.
                child.receiveMessage(msgString_)
            except:
                # If an error occurs, print error child and quit the function with False value.
                print("Error sending message to child[%d]" %child.id)
                return False

        # After no errors, quit the function with True value.
        return True
    
    def update(self):
        # self.move()
        self.display((0, 0, 200), (200, 200, 100))
    
Parent = hubVehicle()

class swarmVehicle(Vehicle):
    def __init__(self, id_):
        Vehicle.__init__(self)

        self.id = id_

        self.radius = 10

        self.messageQueue = [
            "EMPTY"
        ]
    
    def receiveMessage(self, msgString_):
        self.messageQueue.append(msgString_)
    
    def readMessages(self):
        for m in range(len(self.messageQueue)-1, -1, -1):
            
            # If there are no more messages, quit this function.
            if (self.messageQueue[m] == "EMPTY"): 
                if self.id == 0:
                    print("MESSAGE QUEUE EMPTY")
                return
            
            # Otherwise respond to the message.
            msg = self.messageQueue[m]

            if msg.startswith('TURN'):
                dir = self.velocity.heading()
                if msg[4]=='L':
                    self.velocity.rotateToAngle(dir - 0.01)
                else:
                    self.velocity.rotateToAngle(dir + 0.01)
    
    def update(self):
        self.readMessages()

        self.move()
        self.display((0, 0, 0), (0, 0, 0))
Population = [swarmVehicle(i) for i in range(10)]

startTime = time.time()
while time.time() < (startTime + 10.0):
    screen.fill((255, 255, 255))

    Parent.update()
    for veh in Population:
        veh.update()

    pygame.display.flip()