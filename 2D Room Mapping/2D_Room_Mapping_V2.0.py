
"""
28/01/2022

This is currently working quite well, though there are some performance issues. 
I believe this is because there are a lot of mathematical operations happening on repeat, which is not required. 
I need to separate the action of collecting points with the action of building the image of the mapped area. 
This is not too difficult, but it might aid me to rewrite from scratch, to clean up the code and rewrite some confusing code better. 

I also want to figure out a better way of connecting the points in the drawing of the image of the mapped area. 
Because the points do not get added in a known order, it isn't as simple as going through the list and just joining to the following point. 
I have attempted in this version to have each point find the closest point to it, and connect to it. 
But this has led to clusters of points not connecting to others, as their closest point is the one already connected to it. 

Maybe I could create a class of "mappedPoint", which holds a variable of whether or not it has been connected to by another, and if so which, 
and doesn't allow itself to connect to this one. This sounds feasible, but I am concerned that the system may get spread out and then lead to 
crossing lines in the mapped area image. 
What I mean is I am concerned that the mapped area image may contain huge diagonal lines where points that are nowhere near one another are 
connected, because they are at the end of the list of checked points, and when they check, all other points have been marked as un-joinable. 

I am not sure of any better way to join the points together. 
I'm sure there are some, but I also have to consider the hardware I'm working with (my laptop being relatively slow and underpowered).

Idea:
Expand a circle from the center of the room (or the average position of the mapped points) and then as the circle overlaps with a point, 
only run a search through 

Starting with point A, expand a circle until another point B is inside that circle. 
Then connect the two points with a line, and start the cycle again, starting from point B, and not including point A within the search. 
I believe this will work to connect all of the points to their closest points, without any overlap.

"""



import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin, atan2
import pygame
# from random import randint

canvasW, canvasH = (600, 400)
canvas = pygame.display.set_mode((canvasW, canvasH))

class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def render(self, colour=(200,200,200), thickness=1):
        x1, y1, _ = self.start.toInt()
        x2, y2, _ = self.end.toInt()
        pygame.draw.line(
            canvas, colour,
            (x1, y1), (x2, y2),
            thickness
        )

roomCorners = [
    (canvasW * 0.1, canvasH * 0.1), # Top left corner

    (canvasW * 0.4, canvasH * 0.1), # Top left top-alcove corner
    (canvasW * 0.4, canvasH * 0.2), # Bottom left top-alcove corner
    (canvasW * 0.6, canvasH * 0.2), # Bottom right top-alcove corner
    (canvasW * 0.6, canvasH * 0.1), # Top right top-alcove corner
    
    (canvasW * 0.9, canvasH * 0.1), # Top right corner
    (canvasW * 0.9, canvasH * 0.9), # Bottom right corner
    (canvasW * 0.1, canvasH * 0.9)  # Bottom left corner
]
cornerCount = len(roomCorners)

Walls = []
for c in range(cornerCount):
    n = (c+1) % cornerCount
    start = LL.Vector(roomCorners[c][0], roomCorners[c][1])
    end = LL.Vector(roomCorners[n][0], roomCorners[n][1])

    Walls.append(Wall(start, end))

mapFrame = 500
mappedPointMinimumDistance = 10
mappedPoints = []

def linkMappedPoints():
    if len(mappedPoints) == 0: return

    for c in range(0, len(mappedPoints) - 1):
        x1, y1 = mappedPoints[c]
        cPD = float("inf")
        cPI = 0
        for n in range(0, len(mappedPoints) - 1):
            if c == n: continue
            x2, y2 = mappedPoints[n]
            
            dx = x2 - x1
            dy = y2 - y1
            dist = ((dx**2) + (dy**2)) ** 0.5
            if dist < cPD:
                cPD = dist
                cPI = n
    
        pygame.draw.line(
            canvas, (0, 0, 255),
            (int(mappedPoints[c][0]), int(mappedPoints[c][1]) ),
            (int(mappedPoints[cPI][0]), int(mappedPoints[cPI][1]) ),
            1
        )
        





class Robot:
    def __init__(self):
        x = LL.randint(int(canvasW * 0.25), int(canvasW * 0.75))
        y = LL.randint(int(canvasH * 0.25), int(canvasH * 0.75))
        self.position = LL.Vector(x, y)
        self.velocity = LL.Vector.fromAngle( LL.randomFloat(max_= 2.0 * pi) )
        self.velocity.mult(0.1)

        self.radius = 10

        self.sensorCount = 8
        self.sensors = [LL.Sensor() for _ in range(self.sensorCount)]
    
    def updateSensors(self):
        for i in range(self.sensorCount):
            angle = 2.0 * pi * i / self.sensorCount
            self.sensors[i].update(self.position, angle)
    
    def measureSensors(self):
        measuredPoints = []
        for i in range(self.sensorCount):
            sDst = self.sensors[i].measure(Walls)
            if sDst == -1: continue

            sX, sY = self.sensors[i].position.toScalar()
            sDir = self.sensors[i].direction
            
            ptX = int(sX + (cos(sDir) * sDst))
            ptY = int(sY + (sin(sDir) * sDst))

            measuredPoints.append((ptX, ptY))
        
        return measuredPoints
    
    def move(self):
        self.position.add(self.velocity)
        self.position.limitX(self.radius, canvasW - self.radius)
        self.position.limitY(self.radius, canvasH - self.radius)
    
    def render(self, renderSensors_ = True):
        hdg = self.velocity.heading()
        pygame.draw.polygon(
            canvas, (0, 0, 0),
            [
                (
                    int(self.position.x + (cos(hdg) * self.radius)),
                    int(self.position.y + (sin(hdg) * self.radius))
                ),
                (
                    int(self.position.x + (cos(hdg + pi * 0.8) * self.radius * 0.5)),
                    int(self.position.y + (sin(hdg + pi * 0.8) * self.radius * 0.5))
                ),
                (
                    int(self.position.x), int(self.position.y)
                ),
                (
                    int(self.position.x + (cos(hdg + pi * 1.2) * self.radius * 0.5)),
                    int(self.position.y + (sin(hdg + pi * 1.2) * self.radius * 0.5))
                )
            ], 0
        )

        if renderSensors_:
            for s in self.sensors:
                s.render(canvas)
    
    def update(self):
        self.move()
        self.updateSensors()
        
robot = Robot()

# sensor = LL.Sensor()
# sensorAngleCount = 8

randomMovement = True
frame = 0
while(True):
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a:
                robot.velocity.addAngle(-0.1)
            elif ev.key == pygame.K_d:
                robot.velocity.addAngle(0.1)
            elif ev.key == pygame.K_w:
                robot.velocity.mult(1.2)
            elif ev.key == pygame.K_s:
                robot.velocity.mult(0.8)
            elif ev.key == pygame.K_r:
                randomMovement ^= True
        
        if ev.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()

            if randomMovement:
                robot.position = LL.Vector(mx, my)
            else:
                dx = mx - robot.position.x
                dy = my - robot.position.y
                angle = atan2(dy, dx)
                robot.velocity.rotateToAngle(angle)

        
    if randomMovement: robot.velocity.addAngle(LL.randomFloat(-0.1, 0.1))
    robot.update()

    if frame % mapFrame == 0:
        newPoints = robot.measureSensors()
        if len(mappedPoints) == 0:
            mappedPoints.extend( newPoints )
        
        acceptedPoints = []

        for newPoint in newPoints:
            newPointValid = True
            for mappedPoint in mappedPoints:
                dx = mappedPoint[0] - newPoint[0]
                dy = mappedPoint[1] - newPoint[1]
                dist = ((dx**2) + (dy**2)) ** 0.5
                if dist < mappedPointMinimumDistance:
                    newPointValid = False
                    break
            
            if newPointValid:
                acceptedPoints.append(newPoint)


        mappedPoints.extend( acceptedPoints )
        frame = 0

    
    canvas.fill((255, 255, 255))

    for w in Walls:
        w.render()

    robot.render(renderSensors_ = False)
    
    # for pt in mappedPoints:
    #     pygame.draw.circle(
    #         canvas, (150, 150, 255),
    #         pt,
    #         2, 0
    #     )
    
    linkMappedPoints()
    
    pygame.display.flip()

    frame += 1