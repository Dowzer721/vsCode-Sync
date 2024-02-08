
import pygame

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
from LukeLibrary import colours, closestPointOnShape, dxdyh

from math import atan2, cos, sin

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

WHITE = colours["WHITE"]
BLACK = colours["BLACK"]
RED = colours["RED"]

edgeDistance = 0
edgeVertices = [
    (canvasW * edgeDistance,        canvasH * edgeDistance),
    (canvasW * (1-edgeDistance),    canvasH * edgeDistance),
    (canvasW * (1-edgeDistance),    canvasH * (1-edgeDistance)),
    (canvasW * edgeDistance,        canvasH * (1-edgeDistance))
]
def renderEdges(renderColour=RED):
    for c in range(4):
        n = (c+1)%4
        start = ( int(edgeVertices[c][0]), int(edgeVertices[c][1]) )
        end = ( int(edgeVertices[n][0]), int(edgeVertices[n][1]) )
        pygame.draw.line(canvas, renderColour, start, end, 4)

vehicleCount = 1
vehicleRadius = 20
Vehicles = []
class Vehicle:
    def __init__(self, id_):
        self.id = id_
        self.position = [canvasW * 0.4, canvasH * 0.3]
        self.velocity = [0, 0]
        self.acceleration = [2, 3]
        self.speed = 0
        self.updateSpeed()

        self.maximumSpeed = 0.1

        self.avoidEdgeDistance = vehicleRadius * 2
        self.avoidEdgeForce = 0.01

        self.matchNeighbourVelocityForce = 0.1
    
    def updateSpeed(self):
        self.speed = ((self.velocity[0] ** 2) + (self.velocity[1] ** 2)) ** 0.5
    
    def update(self):
        # self.velocity[0] *= 0.99
        # self.velocity[1] *= 0.99
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.updateSpeed()

        if self.speed > self.maximumSpeed:
            heading = atan2(self.velocity[1], self.velocity[0])
            self.velocity[0] = cos(heading) * self.maximumSpeed
            self.velocity[1] = sin(heading) * self.maximumSpeed
        
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] < vehicleRadius:
            self.position[0] = vehicleRadius
        elif self.position[0] > canvasW - vehicleRadius:
            self.position[0] = canvasW - vehicleRadius

        if self.position[1] < vehicleRadius:
            self.position[1] = vehicleRadius
        elif self.position[1] > canvasH - vehicleRadius:
            self.position[1] = canvasH - vehicleRadius
        
        self.matchNeighbourVelocity()
        self.avoidNeighbourCollision()
        self.avoidEdges()
        self.render()
    
    def matchNeighbourVelocity(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy, _ = dxdyh(self.position, (mx, my))
        self.acceleration[0] += (dx * self.matchNeighbourVelocityForce)
        self.acceleration[1] += (dy * self.matchNeighbourVelocityForce)

    def avoidNeighbourCollision(self):
        pass

    def avoidEdges(self):
        
        closestEdgePoint = closestPointOnShape(edgeVertices, self.position)
        
        dx, dy, dist = dxdyh(self.position, closestEdgePoint)

        if dist <= self.avoidEdgeDistance:
            self.acceleration[0] -= (dx * self.avoidEdgeForce)
            self.acceleration[1] -= (dy * self.avoidEdgeForce)

    def render(self, renderColour=BLACK):
        x1, y1 = int(self.position[0]), int(self.position[1])
        pygame.draw.circle(canvas, renderColour, (x1, y1), vehicleRadius, 1)

        heading = atan2(self.velocity[1], self.velocity[0])
        x2 = int(x1 + (cos(heading) * vehicleRadius))
        y2 = int(y1 + (sin(heading) * vehicleRadius))
        pygame.draw.line(canvas, renderColour, (x1, y1), (x2, y2), 1)
for i in range(vehicleCount): Vehicles.append(Vehicle(i))

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    
    canvas.fill(WHITE)

    # renderEdges(BLACK)
    
    for V in Vehicles:
        V.update()
    
    pygame.display.update()