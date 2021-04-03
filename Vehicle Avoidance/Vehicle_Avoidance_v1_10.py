
# This is a refactor and update to 'Vehicle_Avoidance_v1_00.py'

import os
position = 50, 50
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

import pygame
pygame.display.init()

screenW = 800
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

import math
import random

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python")
import LukeLibrary as Luke

simulationRunning = True

class Boundary:
    def __init__(self, startX, startY, endX, endY):
        self.start = Luke.Vector(startX, startY)
        self.end = Luke.Vector(endX, endY)
    def display(self, colour = (255, 150, 150), thickness = 1):
        pygame.draw.line(
            screen, colour,
            (self.start.x, self.start.y), 
            (self.end.x, self.end.y),
            thickness
        )

class Obstacle:
    def __init__(self, startList = [], endList = []):
        startListLen = len(startList)
        endListLen = len(endList)
        if startListLen == 0 and endListLen == 0:
            print("Object startList and endList length == 0")
            return
        
        if startListLen != endListLen:
            print("Object requires len(startList) == len(endList), provided S%d x E%d." %(startListLen, endListLen))
            return

        self.Boundaries = []
        self.boundaryCount = startListLen
        for i in range(self.boundaryCount):
            self.Boundaries.append(
                Boundary(startList[i][0], startList[i][1], endList[i][0], endList[i][1])
            )
    
    def display(self, colour = (255, 150, 150), thickness = 1):
        for i in range(self.boundaryCount):
            self.Boundaries[i].display(colour, thickness)
Obstacles = []
#region OBSTACLES CREATION
randomObjectCount = 3
for _ in range(randomObjectCount):
    mx = int(Luke.randomFloat(screenW * 0.1, screenW * 0.9))
    my = int(Luke.randomFloat(screenH * 0.1, screenH * 0.9))
    radW = int(Luke.randomFloat(screenW * 0.1, screenW * 0.2))
    radH = int(Luke.randomFloat(screenH * 0.1, screenH * 0.2))
    vertexCount = random.randint(3, 16)
    startList = []
    endList = []

    for c in range(vertexCount):
        n = (c + 1) % vertexCount

        cAngle = (math.pi * 2.0 / vertexCount) * c
        nAngle = (math.pi * 2.0 / vertexCount) * n

        startX = mx + (math.cos(cAngle) * radW)
        startY = my + (math.sin(cAngle) * radH)
        endX = mx + (math.cos(nAngle) * radW)
        endY = my + (math.sin(nAngle) * radH)

        startList.append([startX, startY])
        endList.append([endX, endY])
    
    # Obstacles.append(Obstacle(startList, endList))

# Corridor outer walls
outerBorderSizeW = int(screenW * 0.05) # 0.05
outerBorderSizeH = int(screenH * 0.05) # 0.05
borderVertexList = [
    [outerBorderSizeW, outerBorderSizeH],
    [screenW - outerBorderSizeW, outerBorderSizeH],
    [screenW - outerBorderSizeW, screenH - outerBorderSizeH],
    [outerBorderSizeW, screenH - outerBorderSizeH]
]
Obstacles.append(Obstacle(borderVertexList, [borderVertexList[i%4] for i in range(1, 5)]))

# Corridor inner walls
innerBorderSizeW = int(screenW * 0.3) # 0.4
innerBorderSizeH = int(screenH * 0.3) # 0.4
borderVertexList = [
    [innerBorderSizeW, innerBorderSizeH],
    [screenW - innerBorderSizeW, innerBorderSizeH],
    [screenW - innerBorderSizeW, screenH - innerBorderSizeH],
    [innerBorderSizeW, screenH - innerBorderSizeH]
]
Obstacles.append(Obstacle(borderVertexList, [borderVertexList[i%4] for i in range(1, 5)]))

#endregion

Vehicles = [] # Has to be here because Sensor class requires list to already exist.
avoidNeighbours = False # Whether or not the Vehicles steer away from collisions with one another.

class Sensor:
    def __init__(self):
        self.position = Luke.Vector()
        self.direction = Luke.Vector()

        self.measuredDistance = screenW * screenH
    def updatePosition(self, newPos, newDir):
        Px = newPos.x
        Py = newPos.y
        self.position.set(Px, Py)

        self.direction.x = math.cos(newDir)
        self.direction.y = math.sin(newDir)

    def measure(self, currentVehicleID):
        
        cIPD = screenW * screenH

        x1 = self.position.x
        y1 = self.position.y
        x2 = self.position.x + self.direction.x
        y2 = self.position.y + self.direction.y


        boundaryList = []
        if len(Obstacles) > 0:
            for Obs in Obstacles:
                for B in Obs.Boundaries:
                    boundaryList.append(B)
        
        if avoidNeighbours:
            for Veh in Vehicles:
                if Veh.id == currentVehicleID: continue

                Veh.updateBodyBoundaries()
                for B in Veh.bodyBoundaries:
                    boundaryList.append(B)

        for B in boundaryList:
            x3 = B.start.x
            y3 = B.start.y
            x4 = B.end.x
            y4 = B.end.y

            denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
            if denominator == 0:
                continue

            t = ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4))
            t /= denominator

            u = ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3))
            u *= -1 / denominator

            if (t > 0) and (u > 0) and (u < 1):
                x = x1 + (t*(x2-x1))
                y = y1 + (t*(y2-y1))
                intersectPoint = Luke.Vector(x, y)
                cIPD = min(cIPD, self.position.distance(intersectPoint) )
        
        if cIPD == (screenW * screenH):
            self.measuredDistance = -1
        else:
            self.measuredDistance = cIPD
        
        return self.measuredDistance

    def display(self, colour = (255, 150, 150), thickness = 1):
        if self.measuredDistance < 0: return

        dir = self.direction.heading()

        sX = int(self.position.x)
        sY = int(self.position.y)
        eX = int(sX + (math.cos(dir) * self.measuredDistance) )
        eY = int(sY + (math.sin(dir) * self.measuredDistance) )

        pygame.draw.line(
            screen, colour,
            (sX, sY), (eX, eY),
            thickness
        )

        pygame.draw.circle(
            screen, colour,
            (eX, eY), thickness + 2, 
            0
        )

#region class Vehicle : Vehicles[] population
class Vehicle:
    def __init__(self, id_):
        self.id = id_ # Used to identify self within list of Vehicles.
        
        x = (outerBorderSizeW + innerBorderSizeW) / 2
        y = (outerBorderSizeH + innerBorderSizeH) / 2
        self.position = Luke.Vector(x, y)
        self.velocity = Luke.Vector() # Starting velocity at 0.
        self.topSpeed = 1.0 * (self.id + 1) # 0.7 + (self.id * 0.3) # Increases the top speed the more Vehicles are present.

        self.radius = random.randint(5, 20) # 10

        # The higher this number, the better the Vehicle will be seen by others, but the slower 
        # the simulation will run.
        if avoidNeighbours:
            self.bodyBoundaryCount = 8 
            self.bodyBoundaries = [Boundary(0, 0, 0, 0) for _ in range(self.bodyBoundaryCount)]
            self.updateBodyBoundaries()
        
        # The more sensors, the smoother the adjustments, but the slower the simulation.
        # 3 sensors is the fewest number of sensors needed to work; anything smaller and the Vehicle can't 
        # navigate effectively.
        # Through testing, 16 appears to be the best number of sensors. 
        self.sensorCount = 16
        self.sensorAngle = math.pi / 1.0 # The total angle that the sensors cover.
        self.sensors = [Sensor() for _ in range(self.sensorCount)]
        self.updateSensors()
    
    def move(self):
        self.position.add(self.velocity)

    def updateBodyBoundaries(self): # Update the start and end position of the bodyBounderies.
        dir = self.velocity.heading()
        for c in range(self.bodyBoundaryCount):
            n = (c + 1) % self.bodyBoundaryCount

            cAngle = dir + ( (math.pi * 2.0 / self.bodyBoundaryCount) * c) # Current angle
            nAngle = dir + ( (math.pi * 2.0 / self.bodyBoundaryCount) * n) # Next angle

            cX = self.position.x + (math.cos(cAngle) * self.radius) # Current x
            cY = self.position.y + (math.sin(cAngle) * self.radius) # Current y
            nX = self.position.x + (math.cos(nAngle) * self.radius) # Next x
            nY = self.position.y + (math.sin(nAngle) * self.radius) # Next y

            self.bodyBoundaries[c].start.set(cX, cY)
            self.bodyBoundaries[c].end.set(nX, nY)
    
    def edgeStop(self): # Prevents the Vehicle from running off screen.
        self.position.x = max(self.radius, min(self.position.x, screenW-self.radius))
        self.position.y = max(self.radius, min(self.position.y, screenH-self.radius))
    
    def updateSensors(self): # Update the position and facing direction of the sensors.

        if self.sensorCount < 3:
            print("Vehicle sensorCount cannot be less than 3. ")
            
            # If error present: "Unused variable 'simulationRunning' ", it is incorrect; ignore. 
            simulationRunning = False
            return

        for i in range(self.sensorCount):
            theta = self.velocity.heading() - (self.sensorAngle / 2.0) + ((self.sensorAngle / (self.sensorCount-1)) * i )
            sensorX = self.position.x + (math.cos(theta) * self.radius)
            sensorY = self.position.y + (math.sin(theta) * self.radius)
            sensorPos = Luke.Vector(sensorX, sensorY)

            self.sensors[i].updatePosition(sensorPos, theta)
    
    def moveAccordingToSensors(self):
        # Step through each sensor, and subtract from the current velocity according to the angle of the 
        # sensor and the distance which it has measured. 
        # 
        # The closer the sensor angle is to the current heading, the stronger the effect it has upon the 
        # fleeing of walls.
        # What this means is that the direction of travel is altered to attempt to steer away from the 
        # closest objects and walls, and therefore towards the further ones.
        
        # The following numbers alongside are assuming 'self.sensorCount = 7'.
        for i in range(self.sensorCount): # 0 1 2 3 4 5 6
            forcePercent = abs(i - int(self.sensorCount / 2)) * 0.1 # 0.3 0.2 0.1 0.0 0.1 0.2 0.3
            
            # Inclusion of the following line makes the frontal sensors more effective.
            # Exclusion of the following line makes the frontal sensors less effective.
            # Inclusion tends to produce better results.
            forcePercent = 1.0 - forcePercent # 0.7 0.8 0.9 1.0 0.9 0.8 0.7

            
            # This function both sets the sensor distance, and also returns it, allowing for this function to 
            # only be called once before taking data from it, and also drawing the sensor and laser beam.
            # The id is passed to it to prevent the sensors from seeing this Vehicle.
            distanceFromSensor = self.sensors[i].measure(self.id) 


            forceFromSensor = distanceFromSensor * forcePercent

            # The opposite to the direction the sensor is facing.
            sensorAngle = self.sensors[i].direction.heading() - math.pi

            forceFromSensorVector = Luke.Vector().fromAngle(sensorAngle)
            forceFromSensorVector.mult(forceFromSensor)

            # Take the force from the sensor away from the current velocity vector.
            self.velocity.sub(forceFromSensorVector) 

        
        # Once all the changing of the velocity has finished, limit the velocity.
        self.velocity.limit(max_=self.topSpeed) 

    def neighbourBump(self): # This simply prevents the Vehicles from crossing over one another.
        for Veh in Vehicles:
            if Veh.id == self.id: continue
            
            radSum = self.radius + Veh.radius
            dist = self.position.distance(Veh.position)
            if dist < radSum:
                # The angle from the current position to the neighbour
                angleToNeighbour = self.position.angleBetween(Veh.position)
                # The sum of the velocities of self and the neighbour
                velSum = self.velocity.getMag() + Veh.velocity.getMag()
                # The ratio of radii between the neighbour and self
                radRatio = Veh.radius / self.radius

                self.position.x -= math.cos(angleToNeighbour) * (dist / velSum) * radRatio
                self.position.y -= math.sin(angleToNeighbour) * (dist / velSum) * radRatio

    def display(self, colour = (0, 0, 0), thickness = 1, drawSensors = True):
        x = int(self.position.x)
        y = int(self.position.y)
        dir = self.velocity.heading()

        if avoidNeighbours:
            for b in self.bodyBoundaries:
                b.display(colour, thickness)
        else:
            pygame.draw.circle(
                screen, colour,
                (x, y), self.radius,
                thickness
            )

        pygame.draw.line(
            screen, colour,
            (x, y),
            (
                x + (math.cos(dir) * self.radius),
                y + (math.sin(dir) * self.radius)
            ),
            thickness
        )

        if drawSensors:
            for s in self.sensors:
                if s.measuredDistance > 0:
                    s.display((255, 200, 200), 1)
        
    # One function to call the rest, allowing for easier testing, as one can comment out entire functions 
    # via one line.
    def update(self): 
        self.move()
        self.edgeStop()
        if avoidNeighbours:
            self.updateBodyBoundaries()
        self.updateSensors()
        self.moveAccordingToSensors()
        self.neighbourBump()

        self.display(drawSensors=False)

# Arbitrary choice of number of Vehicles
for i in range(8):
    Vehicles.append(Vehicle(i))

#endregion

# There are exit parameters dotted throughout the code, because certain settings can cause errors, 
# and therefore the error handling prints the error then stops this while loop.
while(simulationRunning):
    
    # Fill the screen with white colour.
    screen.fill((255, 255, 255))

    # Display all the obstacles
    for Obs in Obstacles:
        Obs.display()

    # Call the Vehicle update function.
    for V in Vehicles:
        V.update()

    # Flip the display (as drawing happens on the 'back' of the canvas).
    pygame.display.flip()

# This is here to allow for error debugging / data checks
input()