
from random import randint
from math import pi, cos, sin

import pygame

screenW, screenH = 600, 500
screen = pygame.display.set_mode((screenW, screenH))

class City:
    def __init__(self, id_, x_, y_):
        self.id = id_

        self.position = (x_, y_)

        self.visited = bool(id_==0)
    
    def render(self, renderColour=(200,0,0), renderRadius=-1):
        r = 4# (self.id+1)*1 if renderRadius == -1 else renderRadius
        pygame.draw.circle(
            screen, renderColour,
            self.position, r,
            0
        )
cities = []
cityCount = 16
for i in range(cityCount):
    x = randint(int(screenW*0.1), int(screenW*0.9))
    y = randint(int(screenH*0.1), int(screenH*0.9))

    # theta = (pi * 2.0 / cityCount) * i
    # radius = randint(300, 500) / 1000 #   0.3 -> 0.5
    # x = int(screenW/2) + int(cos(theta) * screenW * radius)
    # y = int(screenH/2) + int(sin(theta) * screenH * radius)

    cities.append(City(i, x, y))

visitedCities = [cities[0]]
for i in range(cityCount):
    minDistToOtherCity = screenW * screenH
    otherCityId = i
    for j in range(cityCount):
        if i==j: continue
        if visitedCities[i].id == cities[j].id: continue

        if cities[j].visited == True: continue

        dx = visitedCities[i].position[0] - cities[j].position[0]
        dy = visitedCities[i].position[1] - cities[j].position[1]
        dist = ((dx**2) + (dy**2)) ** 0.5

        if dist < minDistToOtherCity:
            minDistToOtherCity = dist
            otherCityId = j
    
    cities[otherCityId].visited = True
    visitedCities.append(cities[otherCityId])

# for c in visitedCities:
    # print(c.id)

screen.fill((255, 255, 255))

for c in cities:
    col = (200, 0, 0) if c.id > 0 else (0, 200, 0)
    c.render(col)

for c in range(cityCount):
    n = (c+1) % cityCount
    x1 = visitedCities[c].position[0]
    y1 = visitedCities[c].position[1]
    x2 = visitedCities[n].position[0]
    y2 = visitedCities[n].position[1]
    pygame.draw.line(
        screen, (0,0,0),
        (x1, y1), (x2, y2),
        1
    )



pygame.display.flip()

input()