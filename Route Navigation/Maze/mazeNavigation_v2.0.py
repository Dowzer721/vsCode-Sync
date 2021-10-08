
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

from math import pi, cos, sin, atan2
from mazeGeneratorMultipleArms import generate
import pygame

generate(
    6, 8, [0,0], [25,30]
)

mazeDataFile = open("C:/Users/Luke/Documents/Learning Python/Route Navigation/Maze/mazeData.txt", 'r')
mazeData = mazeDataFile.readline()
mazeDataFile.close()

wallInformation, mazeInformation = mazeData.split('.')
# print(wallInformation)

def storedValueToWalls(value):
    
    walls = [0, 0, 0, 0]
    for i in range(3, -1, -1):
        if value >= (2 ** i):
            value -= (2 ** i)
            walls[i] = 1
    
    return walls

walls = [
    storedValueToWalls(int(value))
    for value in wallInformation.split(', ')
]

xPosition = mazeInformation.find('x')
startOpenBracket = mazeInformation.find('[')
endOpenBracket = mazeInformation.find('[', startOpenBracket+1)

mazeWidth = int( mazeInformation[0 : xPosition] )
mazeHeight = int( mazeInformation[xPosition + 1 : startOpenBracket] )

startPosition = mazeInformation[startOpenBracket+1:endOpenBracket-1].split(',')
startPosition[0] = int(startPosition[0])
startPosition[1] = int(startPosition[1])

endPosition = mazeInformation[endOpenBracket+1:-1].split(',')
endPosition[0] = int(endPosition[0])
endPosition[1] = int(endPosition[1])

# print(
#     f"w: {mazeWidth}, h: {mazeHeight} \n" +
#     f"s: {startPosition}, e: {endPosition}"
# )


canvasW = 400
canvasH = int(canvasW * (mazeHeight/mazeWidth) )
canvas = pygame.display.set_mode((canvasW, canvasH))

gridW = canvasW / mazeWidth
gridH = canvasH / mazeHeight


Grid = []
class Cell:
    def __init__(self, col_, row_, walls_):
        self.col = col_
        self.row = row_
        self.walls = walls_
        # if col_<3 and row_==0:
        #     print(self.walls)
    
        cornerAdd = 0
        x1 = (self.col * gridW)
        y1 = (self.row * gridH)
        x2 = ((self.col+1) * gridW)
        y2 = ((self.row+1) * gridH)

        self.corners = [
            (x1 + cornerAdd, y1 + cornerAdd),
            (x2 - cornerAdd, y1 + cornerAdd),
            (x2 - cornerAdd, y2 - cornerAdd),
            (x1 + cornerAdd, y2 - cornerAdd)
        ]
    
    def render(self):
        for c in range(4):
            if self.walls[c] == 1:
                n = (c + 1) % 4
                pygame.draw.line(
                    canvas, (0,0,0),
                    self.corners[c],
                    self.corners[n],
                    1
                )
        
        isStart = (self.col == startPosition[0] and self.row == startPosition[1])
        isEnd = (self.col == endPosition[0] and self.row == endPosition[1])
        if isStart or isEnd:
            x = int( (self.col + 0.5) * gridW )
            y = int( (self.row + 0.5) * gridH )
            r = int(gridW * 0.1)
            colour = (0, 200, 0) if isStart else (200, 0, 0)
            pygame.draw.circle(
                canvas, colour,
                (x, y), r, 0
            )
for row in range(mazeHeight):
    for col in range(mazeWidth):
        index = col + (row * mazeWidth)
        Grid.append(Cell(col, row, walls[index]))

robotWallList = []
for cell in Grid:
    for w in range(4):
        if cell.walls[w] == 0: continue
        n = (w + 1) % 4

        x1 = cell.corners[w][0]
        y1 = cell.corners[w][1]
        x2 = cell.corners[n][0]
        y2 = cell.corners[n][1]

        robotWallList.append(LL.Wall(x1, y1, x2, y2))

class Robot:
    def __init__(self):
        x = (startPosition[0]+0.5) * gridW
        y = (startPosition[1]+0.5) * gridH
        
        self.position = LL.Vector(x, y)

        self.facingDirection = LL.randomFloat(0.0, pi*2.0)
        self.speed = 0.0

        self.radius = int(min(gridW, gridH) * 0.25)

        self.sensorCount = 10 # 4
        self.sensorAngle = pi * 1.0 # 0.5 # 1.0
        self.sensors = [
            LL.Sensor() for _ in range(self.sensorCount)
        ]
        self.updateSensors()
    
    def updateSensors(self):
        for s in range(self.sensorCount):
            angle = self.facingDirection - (self.sensorAngle/2) + (self.sensorAngle*s/(self.sensorCount-1))
            pos = LL.Vector(
                self.position.x + (cos(angle) * self.radius),
                self.position.y + (sin(angle) * self.radius)
            )
            self.sensors[s].update(pos, angle)

            self.sensors[s].measure(robotWallList)
    
    def steerAccordingToSensors(self):
        self.updateSensors()
        
        directionVectorList = []
        for s in range(self.sensorCount):
            
            angle = self.facingDirection - (self.sensorAngle / 2) + ( (self.sensorAngle / (self.sensorCount-1)) * s )
            steeringVector = LL.Vector().fromAngle(angle)
            
            sensorDist = self.sensors[s].measuredDistance ** 2
            steeringVector.mult(sensorDist)

            # dDist = dist - (self.radius * 0.25)
            # steeringVector.mult(dDist)
            
            directionVectorList.append(steeringVector)
        
        averageVector = LL.Vector().sum(directionVectorList, True)

        directionDiff = averageVector.heading() - self.facingDirection
        robotTurnRate = 0.005
        self.facingDirection += (directionDiff * robotTurnRate)

    def move(self):
        self.updateSensors()

        if self.sensorCount % 2 == 0:
            # sensorCount is even, so there is no middle sensor:
            middleSensorReadings = [
                self.sensors[int(self.sensorCount/2)].measuredDistance,
                self.sensors[int(self.sensorCount/2)+1].measuredDistance,
            ]
            sensorReading = sum(middleSensorReadings) / 2.0
        else:
            sensorReading = self.sensors[int(self.sensorCount/2)].measuredDistance
        
        forwardTargetDistance = self.radius * 2.0

        dDist = sensorReading - forwardTargetDistance

        # self.speed += (dDist / 10.0)
        self.speed += (dDist / self.radius)
        self.speed = max(0, min(self.speed, 0.1))

        facingDirectionVec = LL.Vector.fromAngle(self.facingDirection)
        facingDirectionVec.mult(self.speed)
        self.position.add(facingDirectionVec)
    
    def render(self):
        x1, y1, _ = self.position.toInt()
        pygame.draw.circle(
            canvas, (0, 0, 0),
            (x1, y1), self.radius,
            1
        )

        x2 = int( x1 + (cos(self.facingDirection) * self.radius) )
        y2 = int( y1 + (sin(self.facingDirection) * self.radius) )
        pygame.draw.line(
            canvas, (0, 0, 0),
            (x1, y1), (x2, y2), 
            1
        )

        for sen in self.sensors:
            sen.render(canvas)
robot = Robot()

while True:
    canvas.fill((255, 255, 255))

    for cell in Grid:
        cell.render()
    
    robot.steerAccordingToSensors()
    robot.move()
    robot.render()
    
    pygame.display.flip()