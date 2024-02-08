# Really useful geometry drawing tool
# https://www.math10.com/en/geometry/geogebra/geogebra.html

# TODO: Change mapped point locations to be relative to mapped position (and facing?)

# Left side is real location (render), right side is mapped location (calculated).

from math import cos, sin, pi, atan2
import pygame

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW*2, canvasH))

realWallColour = (200, 200, 200)
mappedWallColour = (255, 0, 0)

realVehicleColour = (100, 100, 100)
calculatedVehicleColour = (255, 100, 100)

class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.posInt = (int(_x), int(_y))
    def render(self, _renderColour=realWallColour):
        pygame.draw.circle(canvas, _renderColour, self.posInt, 4, 0)

class Wall:
    def __init__(self, _start, _end):
        self.start = _start
        self.end = _end
    def render(self, _renderColour=realWallColour):
        self.start.render(_renderColour)
        pygame.draw.line(canvas, _renderColour, self.start.posInt, self.end.posInt, 1)

def LineLineIntersection(lineAStart, lineAEnd, lineBStart, lineBEnd):
    x1, y1 = lineAStart.x, lineAStart.y
    x2, y2 = lineAEnd.x, lineAEnd.y
    x3, y3 = lineBStart.x, lineBStart.y
    x4, y4 = lineBEnd.x, lineBEnd.y
    denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
    if denominator == 0: return False

    t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
    if t<0 or t>1: return False
    
    u = ( ((x1-x3)*(y1-y2)) - ((y1-y3)*(x1-x2)) ) / denominator
    if u<0 or u>1: return False

    return Point(
        x1 + (t * (x2 - x1)),
        y1 + (t * (y2 - y1))
    )

outerWallPoints = [
    Point(canvasW*0.1, canvasH*0.1),
    Point(canvasW*0.9, canvasH*0.1),
    
    Point(canvasW*0.9, canvasH*0.45),
    Point(canvasW*0.85, canvasH*0.45),
    Point(canvasW*0.85, canvasH*0.55),
    Point(canvasW*0.9, canvasH*0.55),

    Point(canvasW*0.9, canvasH*0.9),
    
    Point(canvasW*0.3, canvasH*0.9),
    Point(canvasW*0.3, canvasH*0.7),
    Point(canvasW*0.1, canvasH*0.7)
]
numberOfOuterWallPoints = len(outerWallPoints)

innerWallPoints = [
    Point(canvasW*0.4, canvasH*0.4),
    Point(canvasW*0.6, canvasH*0.4),
    Point(canvasW*0.6, canvasH*0.6),
    Point(canvasW*0.4, canvasH*0.6)
]
numberOfInnerWallPoints = len(innerWallPoints)

realWalls = []
mappedWalls = []

for c in range(numberOfOuterWallPoints):
    n = (c + 1) % numberOfOuterWallPoints
    
    # render:
    realWalls.append(Wall(outerWallPoints[c], outerWallPoints[n]))
    
    # # calculated:
    # calculatedStartX = outerWallPoints[c].x + canvasW
    # calculatedStartY = outerWallPoints[c].y
    # calculatedStart = Point(calculatedStartX, calculatedStartY)

    # calculatedEndX = outerWallPoints[n].x + canvasW
    # calculatedEndY = outerWallPoints[n].y
    # calculatedEnd = Point(calculatedEndX, calculatedEndY)

    # mappedWalls.append(Wall(calculatedStart, calculatedEnd))


    # Walls.append(Wall(outerWallPoints[c] + canvasW, out))

for c in range(numberOfInnerWallPoints):
    n = (c + 1) % numberOfInnerWallPoints
    
    # render:
    realWalls.append(Wall(innerWallPoints[c], innerWallPoints[n]))

    # # calculated:
    # calculatedStartX = innerWallPoints[c].x + canvasW
    # calculatedStartY = innerWallPoints[c].y
    # calculatedStart = Point(calculatedStartX, calculatedStartY)

    # calculatedEndX = innerWallPoints[n].x + canvasW
    # calculatedEndY = innerWallPoints[n].y
    # calculatedEnd = Point(calculatedEndX, calculatedEndY)

    # mappedWalls.append(Wall(calculatedStart, calculatedEnd))

class Vehicle:
    def __init__(self, _startingPosition, _startingFacingDirection, _maxSpeed=1):
        self.position = _startingPosition
        self.calculatedPosition = Point(_startingPosition.x + canvasW, _startingPosition.y)

        self.facing = _startingFacingDirection
        self.currentSpeed = 0
        self.maxSpeed = _maxSpeed

        self.sensorCount = 3
        self.sensorCoverageAngle = pi
        self.sensorArrayRadius = 16
        self.sensors = [Wall(Point(0,0), Point(0,0)) for _ in range(self.sensorCount)]
        self.sensorStartingDistance = canvasW * canvasH
        self.updateSensors()
        self.renderSensorsBool = self.sensorCount <= 6
        self.sensorRenderColour = (100, 255, 100)
        
        self.recordedPoints = []
        
        self.renderRadius = 16
        self.renderPolygonAngles = (0, pi*0.8, 0, pi*1.2)
        self.renderPolygonRadii = (self.renderRadius, self.renderRadius*0.5, 0, self.renderRadius*0.5)
        
        self.renderPolygonVertexCount = len(self.renderPolygonRadii)
        self.renderPolygon = []
        self.calculatedPositionPolygon = []
        
        self.renderPolygon = self.updateRenderPolygon(self.position)
        self.realPolygon = self.updateRenderPolygon(self.calculatedPosition)
    
    def updateSpeed(self, speedAddition):
        self.currentSpeed = max(0, min(self.currentSpeed + speedAddition, self.maxSpeed))

    def updatePosition(self):
        nextPositionX = self.position.x + (cos(self.facing) * self.currentSpeed)
        nextPositionY = self.position.y + (sin(self.facing) * self.currentSpeed)
        self.position = Point(nextPositionX, nextPositionY)
        self.updateSensors()
        self.renderPolygon = self.updateRenderPolygon(self.position)
        self.realPolygon = self.updateRenderPolygon(self.calculatedPosition)
    
    def updateSensors(self):
        
        sensorArcStartingAngle = self.facing
        sensorArcStepAngle = 0
        if self.sensorCount > 1:
            sensorArcStartingAngle = self.facing - (self.sensorCoverageAngle / 2)
            sensorArcStepAngle = self.sensorCoverageAngle / (self.sensorCount - 1)
        for i in range(self.sensorCount):
            sensorAngle = sensorArcStartingAngle + (sensorArcStepAngle * i)
            self.sensors[i].start = Point(
                self.position.x + (cos(sensorAngle) * self.sensorArrayRadius),
                self.position.y + (sin(sensorAngle) * self.sensorArrayRadius)
            )
            self.sensors[i].end = Point(
                self.position.x + (cos(sensorAngle) * canvasW * canvasH),
                self.position.y + (sin(sensorAngle) * canvasW * canvasH)
            )
            
    def blipSensors(self):
        sensorPoints = []
        for S in self.sensors:
            sensorStart = S.start
            sensorEnd = S.end
            sensorDx = sensorEnd.x - sensorStart.x
            sensorDy = sensorEnd.y - sensorStart.y
            sensorAngle = atan2(sensorDy, sensorDx)
            
            closestPoint_Distance = self.sensorStartingDistance
            closestPoint_Angle = 0

            for W in realWalls:
                wallStart = W.start
                wallEnd = W.end
                intersectionPoint = LineLineIntersection(sensorStart, sensorEnd, wallStart, wallEnd)
                if intersectionPoint == False: continue
                dx = intersectionPoint.x - sensorStart.x
                dy = intersectionPoint.y - sensorStart.y
                dist = ((dx**2)+(dy**2))**0.5
                if dist < closestPoint_Distance:
                    closestPoint_Distance = dist
                    closestPoint_Angle = sensorAngle
            
            if closestPoint_Distance < self.sensorStartingDistance:
                sensorPoints.append((closestPoint_Angle, closestPoint_Distance + self.sensorArrayRadius))

        self.recordedPoints.append(sensorPoints)
    
    def updateRenderPolygon(self, _centerPosition):
        return [
            (
                _centerPosition.x + (cos(self.facing + self.renderPolygonAngles[c]) * self.renderPolygonRadii[c]),
                _centerPosition.y + (sin(self.facing + self.renderPolygonAngles[c]) * self.renderPolygonRadii[c])
            )
            for c in range(self.renderPolygonVertexCount)
        ]
    
    def render(self):
        pygame.draw.polygon(canvas, realVehicleColour, self.renderPolygon, 0)
        pygame.draw.polygon(canvas, calculatedVehicleColour, self.realPolygon, 0)
        if self.renderSensorsBool:
            self.renderSensors()
        
    def renderSensors(self):
        for S in self.sensors:
            S.render(self.sensorRenderColour)
    
    def renderMappedWalls(self, renderAsPolygon_=False):
        if renderAsPolygon_:
            pass
        else:
            for recordGroup in self.recordedPoints:
                for angle, dist in recordGroup:
                    pointX = int(self.calculatedPosition.x + (cos(angle) * dist))
                    pointY = int(self.calculatedPosition.y + (sin(angle) * dist))
                    pygame.draw.circle(canvas, mappedWallColour, (pointX, pointY), 3, 0)
            

Robot = Vehicle(Point(canvasW*0.2, canvasH*0.2), 0)

def quit():
    pygame.quit()
    exit(0)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            quit()

        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_w:
                Robot.updateSpeed(0.01)
            elif ev.key == pygame.K_s:
                Robot.currentSpeed = 0
            elif ev.key == pygame.K_SPACE:
                Robot.blipSensors()
                Robot.renderSensors()
                # print("Sensors Flashed")
            elif ev.key == pygame.K_ESCAPE:
                quit()
        
            # print(Robot.facing)
    
    turningKeys = pygame.key.get_pressed()
    if turningKeys[pygame.K_d]:# == pygame.K_d:
        Robot.facing += 0.001
    elif turningKeys[pygame.K_a]:# == pygame.K_a: 
        Robot.facing -= 0.001
    
    canvas.fill((255, 255, 255))

    # realWalls = []
    # mappedWalls = []

    for realW in realWalls:
        realW.render(realWallColour)
    # for mappedW in mappedWalls:
    #     mappedW.render(mappedWallColour)
    
    Robot.updatePosition()
    Robot.render()
    Robot.renderMappedWalls()
    
    pygame.display.update()