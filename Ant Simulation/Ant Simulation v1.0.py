
from math import pi, cos, sin, atan2

import pygame
screenW, screenH = (600, 500)
screen = pygame.display.set_mode((screenW, screenH))

from random import randint, seed
seed(0)

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

foodLocations = [
    (screenW*0.5, screenH * 0.1),
    (screenW*0.9, screenH * 0.6),
    (screenW*0.2, screenH * 0.2),
    (screenW*0.4, screenH * 0.8)
]
foodAmounts = [100 for _ in range(len(foodLocations))]

class Marker:
    def __init__(self, x_, y_, dir_, type_):
        self.position = LL.Vector(x_, y_)
        self.direction = dir_
        self.type = type_ # "home" || "food"
        self.strength = 100
    def render(self):
        x, y, _ = self.position.toInt()
        
        renderColour = (255, 255, 255)

        if self.type == "home":
            renderColour = (0, 0, self.strength * 2)
        elif self.type == "food":
            renderColour = (0, self.strength * 2, 0)
        
        pygame.draw.circle(
            screen, renderColour,
            (x, y), 1, 1
        )
markers = []
        

class Ant:
    def __init__(self, x_=int(screenW/2), y_=int(screenH/2)):
        
        self.position = LL.Vector(x_, y_)

        direction = LL.randomFloat(0.0, 2.0 * pi)
        self.velocity = LL.Vector.fromAngle(direction)
        # self.velocity.mult(0.1)

        self.state = "hunting"

        self.radius = 2

    def update(self, dropFrame_):
        self.stateSteer()
        self.move()
        self.detectFood()
        
        if dropFrame_:
            self.dropMarker()
        
        self.edgeLoop()
        self.render()
    
    def stateSteer(self):
        if self.state == "hunting":

            for m in markers:
                if m.type == "home": continue

                dist = self.position.distance(m.position)
                if dist <= self.radius:
                    self.velocity.rotateToAngle(m.direction + pi)



        elif self.state == "returning":
            pass

    def move(self):
        self.velocity.randomRotation(1)
        self.position.add(self.velocity)
    
    def detectFood(self):
        for f in range(len(foodLocations)):
            foodX = foodLocations[f][0]
            foodY = foodLocations[f][1]
            foodR = int(foodAmounts[f] / 10)
            dx = self.position.x - foodX
            dy = self.position.y - foodY
            dist = ((dx**2) + (dy**2)) ** 0.5
            if dist <= foodR:
                self.state = "returning"
    
    def dropMarker(self):
        x, y, _ = self.position.toInt()
        hdg = self.velocity.heading()
        markerType = ""
        if self.state == "hunting":
            markerType = "home"
        elif self.state == "returning":
            markerType = "food"

        markers.append(Marker(x, y, hdg, markerType))

    def edgeLoop(self):
        if self.position.x < 0:
            self.position.x = screenW
        elif self.position.x > screenW:
            self.position.x = 0
        
        if self.position.y < 0:
            self.position.y = screenH
        elif self.position.y > screenH:
            self.position.y = 0
    
    def render(self, renderColour=(255, 0, 0)):
        x, y, _ = self.position.toInt()
        pygame.draw.circle(
            screen, renderColour,
            (x, y),
            self.radius, 0
        )

numberOfAnts = 250
ants = [Ant() for _ in range(numberOfAnts)]

frame = 0
while(True):
    screen.fill((0, 0, 0))

    pygame.draw.circle(
        screen, (0, 0, 200),
        (int(screenW/2), int(screenH/2)),
        16, 0
    )

    for f in range(len(foodLocations)):
        if foodAmounts[f] <= 0: continue
        
        x = int(foodLocations[f][0])
        y = int(foodLocations[f][1])
        r = int(foodAmounts[f] / 10)
        pygame.draw.circle(
            screen, (0, 200, 0),
            (x, y),
            r, 0
        )
    
    for m in markers:
        m.strength -= 0.1
        if m.strength <= 0.0:
            markers.remove(m)
            continue

        m.render()

    dropMarker = (frame % 25 == 0)
    for a in ants:
        a.update(dropMarker)

    pygame.display.flip()

    frame += 1