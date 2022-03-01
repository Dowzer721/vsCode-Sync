
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin, atan2
import pygame

from time import time

roomWidth, roomHeight = 600, 500
canvas = pygame.display.set_mode((roomWidth, roomHeight))

roomCorners = [
    (roomWidth * 0.1, roomHeight * 0.1),
    (roomWidth * 0.3, roomHeight * 0.1),
    (roomWidth * 0.3, roomHeight * 0.2),
    (roomWidth * 0.7, roomHeight * 0.2),
    (roomWidth * 0.7, roomHeight * 0.1),
    (roomWidth * 0.9, roomHeight * 0.1),
    (roomWidth * 0.8, roomHeight * 0.3),
    (roomWidth * 0.8, roomHeight * 0.7),
    (roomWidth * 0.9, roomHeight * 0.9),
    (roomWidth * 0.1, roomHeight * 0.9)
]

class Wall:
    def __init__(self, start_, end_):
        self.start, self.end = start_, end_
    def render(self):
        x1, y1, _ = self.start.toInt()
        x2, y2, _ = self.end.toInt()
        pygame.draw.line(
            canvas, (200, 200, 200),
            (x1, y1), (x2, y2),
            1
        )

Walls = []
for c in range(len(roomCorners)):
    n = (c + 1) % len(roomCorners)
    startX, startY = roomCorners[c]
    endX, endY = roomCorners[n]
    
    Walls.append(Wall(LL.Vector(startX, startY), LL.Vector(endX, endY)) )

mappedPointMinimumDistance = 10
mappedPoints = []
class mappedPoint:
    def __init__(self, x_, y_, id_ = len(mappedPoints)):
        self.position = LL.Vector(x_, y_)
        self.connectedToOtherPoint = False
        self.connectedPointID = id_
        self.id = id_
    
    def render(self):
        x1, y1, _ = self.position.toInt()
        # r = self.id + 4 # 6 if self.id == 0 else 4
        # pygame.draw.circle(
        #     canvas, (150, 150, 255),
        #     (x1, y1), r, 0
        # )

        if self.connectedToOtherPoint:
            x2, y2, _ = mappedPoints[self.connectedPointID].position.toInt()
            pygame.draw.line(
                canvas, (100, 100, 255),
                (x1, y1), (x2, y2), 1
            )

def joinAllMappedPoints(currentID = 0):

    if len(mappedPoints) == 0: return
    
    numberOfUnconnectedPoints = sum( [int(mappedPoints[i].connectedToOtherPoint) for i in range(len(mappedPoints))] )
    if numberOfUnconnectedPoints == len(mappedPoints) - 1: return


    x1, y1, _ = mappedPoints[currentID].position.toInt()
    closestDistance = float("inf")
    closestID = currentID
    
    for otherID in range(len(mappedPoints)):

        # If current and other are the same, skip:
        if currentID == otherID: continue

        # If other is already connected elsewhere, skip:
        if mappedPoints[otherID].connectedToOtherPoint: continue

        x2, y2, _ = mappedPoints[otherID].position.toInt()
        dx = x2 - x1
        dy = y2 - y1
        dist = ((dx**2) + (dy**2)) ** 0.5
        if dist < closestDistance:
            closestDistance = dist
            closestID = otherID
    
    mappedPoints[currentID].connectedPointID = closestID
    mappedPoints[currentID].connectedToOtherPoint = True

    joinAllMappedPoints(closestID)


class Robot:
    def __init__(self):
        x = LL.randint(int(roomWidth * 0.4), int(roomWidth * 0.6))
        y = LL.randint(int(roomHeight * 0.4), int(roomHeight * 0.6))
        self.position = LL.Vector(x, y)
        self.velocity = LL.Vector().fromAngle( LL.randomFloat(0.0, 2.0 * pi) )
        self.velocity.mult(0.1)

        self.waypoint = self.position
        self.reachedWaypoint = True
        
        self.sensorCount = 32
        self.sensors = [LL.Sensor() for _ in range(self.sensorCount)]

        self.radius = 8

        self.senseRoom()
    
    def senseRoom(self):

        for j in range(len(mappedPoints)):
            mappedPoints[j].connectedToOtherPoint = False

        for s in range(self.sensorCount):
            angle = pi * 2.0 * s / self.sensorCount
            self.sensors[s].update(self.position, angle)
            d = self.sensors[s].measure(Walls)
            if d == -1: continue
            x = self.position.x + int(cos(angle) * d)
            y = self.position.y + int(sin(angle) * d)

            newPositionValid = True
            for existingPoint in mappedPoints:
                # print(existingPoint)
                if existingPoint.position.distance(LL.Vector(x, y)) <= mappedPointMinimumDistance:
                    newPositionValid = False

            if newPositionValid:
                mappedPoints.append(mappedPoint(x, y, len(mappedPoints)))
        
        joinAllMappedPoints()

    def update(self):

        if self.reachedWaypoint == False:
            self.position.add(self.velocity)
            self.position.limitX(self.radius, roomWidth - self.radius)
            self.position.limitY(self.radius, roomHeight- self.radius)

            dx = self.waypoint.x - self.position.x
            dy = self.waypoint.y - self.position.y
            dist = ((dx**2) + (dy**2)) ** 0.5
            if dist <= self.radius:
                # print(f"Robot reached waypoint @ {time()}")
                self.reachedWaypoint = True
        
        else:
            self.senseRoom()
            
            furthestApartDistance = -1
            furthestApartIDs = (0, 0)
            
            for currentID in range(len(mappedPoints)):
                x1, y1, _ = mappedPoints[currentID].position.toInt()

                otherID = mappedPoints[currentID].connectedPointID
                x2, y2, _ = mappedPoints[otherID].position.toInt()

                dx = x2 - x1
                dy = y2 - y1
                dist = ((dx**2) + (dy**2)) ** 0.5
                if dist > furthestApartDistance:
                    furthestApartDistance = dist
                    furthestApartIDs = (currentID, otherID)
            
            # for i in range(len(mappedPoints)):
            #     x1, y1, _ = mappedPoints[i].position.toInt()
            #     for j in range(len(mappedPoints)):
            #         if i == j: continue
            #         x2, y2, _ = mappedPoints[j].position.toInt()

            #         dx = x2 - x1
            #         dy = y2 - y1

            #         dist = ((dx**2) + (dy**2)) ** 0.5
            #         if dist > furthestApartDistance:
            #             furthestApartDistance = dist
            #             furthestApartIDs = (i, j)
            
            x3, y3, _ = mappedPoints[furthestApartIDs[0]].position.toInt()
            x4, y4, _ = mappedPoints[furthestApartIDs[1]].position.toInt()
            mx = (x3 + x4) / 2
            my = (y3 + y4) / 2

            # angleToMid = atan2(my - self.position.y, mx - self.position.x)
            # distToMid = (((self.position.x - mx) ** 2) + ((self.position.y - my) ** 2)) ** 0.5
            # wx = self.position.x + (cos(angleToMid) * distToMid * 0.8)
            # wy = self.position.y + (sin(angleToMid) * distToMid * 0.8)
            # self.waypoint = LL.Vector(wx, wy)

            self.waypoint = LL.Vector(mx, my)
            self.reachedWaypoint = False

            dx = self.waypoint.x - self.position.x
            dy = self.waypoint.y - self.position.y
            self.velocity.rotateToAngle(atan2(dy, dx))
    
    def render(self):
        x1, y1, _ = self.position.toInt()
        pygame.draw.circle(
            canvas, (100, 100, 100),
            (x1, y1), self.radius, 1
        )

        hdg = self.velocity.heading()
        x2 = x1 + int(cos(hdg) * self.radius)
        y2 = y1 + int(sin(hdg) * self.radius)
        pygame.draw.line(
            canvas, (150, 150, 150),
            (x1, y1), (x2, y2), 1
        )

        wx, wy, _ = self.waypoint.toInt()
        pygame.draw.circle(
            canvas, (0, 200, 0),
            (wx, wy), self.radius, 0
        )

robot = Robot()



# Keeping track of the simulation frame instead of simulation time:
simulationFrame = 0
while True:

    # Handle events:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        
        if event.type == pygame.KEYUP:
            pass
        
        if event.type == pygame.MOUSEBUTTONUP:
            pass
            # mx, my = pygame.mouse.get_pos()
            # generateMoreMappedPoints(mx, my)
            # joinAllMappedPoints()
            # robot.senseRoom()

        
        


    # Fill the canvas with white:
    canvas.fill((255, 255, 255))

    # Draw the walls:
    for W in Walls:
        W.render()
    
    for pt in mappedPoints:
        pt.render()
    
    robot.update()
    robot.render()

    
    # Flip the display once all drawing has been done:
    pygame.display.flip()

    # Increase the simulation frame as the final operation in the simulation loop:
    simulationFrame += 1