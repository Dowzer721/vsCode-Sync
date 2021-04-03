

# Add this to beginning of file if not in same branch as this file:
# import sys
# sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# import LukeLibrary as LL


import math

import pygame
# pygame.init()
pygame.display.init()

import random
import time

class Vector:
    # --- Initialisation:
    def __init__(self, x_=0.0, y_=0.0, z_=None):
        self.x = x_
        self.y = y_
        self.z = z_
        # if z_ != None:
        #     self.z = z_

    # --- Return Vector:
    @staticmethod
    def fromAngle(angle):
        x = math.cos(angle)
        y = math.sin(angle)
        return Vector(x, y)
        
    def copy(self):
        return Vector(self.x, self.y)

    # --- Manipulate current Vector:
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
    def sub(self, vec):
        self.x -= vec.x
        self.y -= vec.y
    def mult(self, val):
        self.x *= val
        self.y *= val
    def limit(self, min_ = 0.0, max_ = 1.0):
        # newMag = max(min_, min(self.getMag(), max_))
        # self.setMag(newMag)

        self.setMag( max(min_, min(self.getMag(), max_)) )

    def limitX(self, min_ = 0.0, max_ = 1.0):
        self.x = max(min_, min(self.x, max_))
    def limitY(self, min_ = 0.0, max_ = 1.0):
        self.y = max(min_, min(self.y, max_))
    def setMag(self, newMag):
        dir = self.heading()
        self.x = math.cos(dir) * newMag
        self.y = math.sin(dir) * newMag
    def normalise(self, scale=1.0):
        dir = self.heading()
        self.x = math.cos(dir) * scale
        self.y = math.sin(dir) * scale
    def rotateToAngle(self, newAngle):
        mag = self.getMag()
        self.x = math.cos(newAngle) * mag
        self.y = math.sin(newAngle) * mag
    def set(self, newX, newY, newZ=None):
        self.x = newX
        self.y = newY
        if (self.z != None) and (newZ != None):
            self.z = newZ
    # def set(self, newVec):
    #     self.x = newVec.x
    #     self.y = newVec.y
    #     if self.z != None:
    #         self.z = newVec.z

    # --- Return scalar:
    def distance(self, vec):
        dx = self.x - vec.x
        dy = self.y - vec.y
        return math.sqrt((dx**2) + (dy**2))
    def angleBetween(self, vec):
        # These have been swapped so previous calls of this function may return opposite angles.
        dx = vec.x - self.x
        dy = vec.y - self.y
        return math.atan2(dy, dx)
    def heading(self):
        return math.atan2(self.y, self.x)
    def getMag(self):
        return math.sqrt((self.x**2) + (self.y**2))
    def dot(self, vec):
        xProduct = self.x * vec.x
        yProduct = self.y * vec.y
        zProduct = self.z * vec.z if (self.z != None and vec.z != None) else 0.0
        return xProduct + yProduct + zProduct

class Sensor:
    def __init__(self):
        self.position = Vector()
        self.direction = 0.0
        self.measuredDistance = -1.0 #pygame.Surface.get_width() * pygame.Surface.get_height()
    def update(self, pos, dir):
        self.position.set(pos.x, pos.y)
        self.direction = dir
    def measure(self, screen, wallList):
        cIPD = screen.get_width() * screen.get_height()
        
        x1 = self.position.x
        y1 = self.position.y
        x2 = self.position.x + math.cos(self.direction)
        y2 = self.position.y + math.sin(self.direction)

        for wall in wallList:
            x3 = wall.start.x
            y3 = wall.start.y
            x4 = wall.end.x
            y4 = wall.end.y

            denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
            if denominator == 0.0:
                continue
            
            t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
            u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

            if (t > 0.0) and (u > 0.0) and (u < 1.0):
                x = x1 + (t * (x2-x1))
                y = y1 + (t * (y2-y1))
                dist = self.position.distance(Vector(x, y))
                cIPD = min(cIPD, dist)
        
        if cIPD == screen.get_width() * screen.get_height():
            self.measuredDistance = -1
        else:
            self.measuredDistance = cIPD
        
        return self.measuredDistance
    def display(self, screen, colour=(255, 100, 100), thickness=1):
        # This function may not work, as it requires a pygame.Surface to be provided, and this may cause looping errors.
        
        x1 = int(self.position.x)
        y1 = int(self.position.y)
        pygame.draw.circle(
            screen, colour, 
            (x1, y1), thickness + 1,
            0
        )

        if self.measuredDistance < 0.0:
            # If the sensor does not 'see' a wall, then return.
            return
        
        x2 = x1 + int(math.cos(self.direction) * self.measuredDistance)
        y2 = y1 + int(math.sin(self.direction) * self.measuredDistance)

        pygame.draw.line(
            screen, colour,
            (x1, y1), (x2, y2),
            thickness
        )

def randomFloat(min_ = 0.0, max_ = 1.0, precision = 3):
    min_ = min(min_, max_)
    max_ = max(min_, max_)
    
    rng = max_ - min_
    random.seed(time.time())
    pct = random.randint(0, 10**precision) / float(10**precision)
    return float(round(min_ + (rng * pct), precision))

def mapToRange(input, inputMin=-1.0, inputMax=1.0, outputMin=0.0, outputMax=1.0):
    # mapToRange(40, -10, 90, 0, 10)
    inputRange = inputMax - inputMin # 90 - -10 = 100
    inputPercentage = (input-inputMin) / inputRange # (40-(-10)) / 100 = 0.5

    outputRange = outputMax - outputMin # 10 - 0 = 10
    return outputMin + (inputPercentage * outputRange) # 0 + (0.5 * 10) = 5

    # region "Examples"
        # mapToRange(20, 0, 100, 20, 70) -> 30
        # inputRange = 100 - 0 = 100
        # inputPercentage = (20-0) / 100 = 0.2
        # outputRange = 70 - 20 = 50
        # outputMin + (inputPercentage * outputRange) -> 20 + (0.2 * 50) = 30
# print(mapToRange(20, 0, 100, 20, 70))

        # mapToRange(40, -10, 90, 0, 10) -> 5
        # inputRange = 90 - (-10) = 100
        # inputPercentage = (40-(-10)) / 100 = 0.5
        # outputRange = 10 - 0 = 10
        # outputMin + (inputPercentage * outputRange) -> 0 + (0.5 * 10) = 5
# print(mapToRange(40, -10, 90, 0, 10))

        # mapToRange(0, -1, 1, 0, 4) -> 2
        # inputRange = 1 - (-1) = 2
        # inputPercentage = (0-(-1)) / 2 = 0.5
        # outputRange = 4 - 0 = 4
        # outputMin + (inputPercentage * outputRange) -> 0 + (0.5 * 4) = 2
# print(mapToRange(0, -1, 1, 0, 4))

# print(mapToRange(-50, 0, 100, 0, 10))
    # endregion

def isBetween(val, min_, max_):
    return (min_ < val) and (val < max_)

def radiansToDegrees(r):
    # 1Rad × 180/π
    return r * (180.0 / math.pi)

def degreesToRadians(d):
    # 1Deg × π/180
    return d * (math.pi / 180.0)

def sign(val):
    if val == 0:
        return 0
    if val < 0:
        return -1
    
    return 1

def listTrim(list, startIndex, endIndex):
    return list[startIndex:endIndex]
    # startIndex = max(0, startIndex) # Prevents negative startIndex
    
    # if endIndex == -1: 
    #     endIndex = len(list) - 1 # -1 is shorthand for end of a list
    
    # if startIndex > endIndex: # If startIndex is greater than endIndex, this flips them around
    #     tempStart = startIndex
    #     startIndex = endIndex
    #     endIndex = tempStart

    # trimmedList = [list[i] for i in range(startIndex, endIndex)]
    
    # return trimmedList

def smooth1DNoise(noiseArr, noiseScale=0.1, edgeLoop=True):
    noiseLength = len(noiseArr)
    for curr in range(noiseLength):
        if edgeLoop:
            prev = (curr + noiseLength - 1) % noiseLength
            next = (curr + 1) % noiseLength
        else:
            prev = max(0, curr - 1)
            next = min(curr + 1, noiseLength-1)
        prevDiff = noiseArr[prev] - noiseArr[curr]
        nextDiff = noiseArr[next] - noiseArr[curr]
        diffSum  = prevDiff + nextDiff
        noiseArr[curr] += (diffSum * noiseScale)
    
    # minNoise = min(noiseArr)
    # maxNoise = max(noiseArr)
    # maxMinDiff = maxNoise - minNoise
    # for c in range(noiseLength):
    #     noiseArr[c] = (noiseArr[c] - minNoise) / maxMinDiff

def generate1DNoise(noiseLength, noiseScale=0.1, precisionDP=3, smooth=True, smoothCount=-1, edgeLoop=True):

    if smoothCount==-1:
        smoothCount = int(noiseLength * 1.5)

    noise = [randomFloat(precision=precisionDP) for _ in range(noiseLength)]
    
    if smooth:
        for _ in range(smoothCount):
            smooth1DNoise(noise, noiseScale, edgeLoop)
    
    return noise

def smooth2DNoise(noiseArr, noiseScale=0.1, neighbourLayerCount=1, edgeLoop=False):
    
    noiseWidth = len(noiseArr[0])
    noiseHeight= len(noiseArr)

    for y in range(noiseHeight):
        for x in range(noiseWidth):
            if (neighbourLayerCount == 1):
                if edgeLoop:
                    xPrev = (x + noiseWidth  - 1) % noiseWidth
                    yPrev = (y + noiseHeight - 1) % noiseHeight
                    xNext = (x + 1) % noiseWidth
                    yNext = (y + 1) % noiseHeight
                else:
                    xPrev = max(0, x-1)
                    yPrev = max(0, y-1)
                    xNext = min(x+1, noiseWidth -1)
                    yNext = min(y+1, noiseHeight-1)
                
                neighbours = [
                    noiseArr[yPrev][xPrev], noiseArr[yPrev][x], noiseArr[yPrev][xNext],
                    noiseArr[y][xPrev], noiseArr[y][xNext],
                    noiseArr[yNext][xPrev], noiseArr[yNext][x], noiseArr[yNext][xNext]
                ]

                neighbourDifference = [
                    (neighbours[i] - noiseArr[y][x]) for i in range(8)
                ]

                neighbourDifferenceSum = sum(neighbourDifference)
                neighbourDifferenceSum /= 8.0
                # neighbourDifferenceSum /= max(len([i for i in neighbourDifference if i > 0]), 1)

                noiseArr[y][x] += (neighbourDifferenceSum * noiseScale)

def generate2DNoise(noiseWidth, noiseHeight, noiseScale=0.1, precisionDP=3, smooth=True, smoothCount=-1, smoothEdgeLoop=False):


    if smoothCount==-1:
        noiseHyp = math.sqrt((noiseWidth**2)+(noiseHeight**2))
        smoothCount = int(noiseHyp * 1.5)
    
    noise = [
        [randomFloat(precision=precisionDP) for _ in range(noiseWidth)]
        for _ in range(noiseHeight)
    ]

    if smooth:
        for _ in range(smoothCount):
            smooth2DNoise(noise, noiseScale, edgeLoop=smoothEdgeLoop)
    
    return noise

def LineLineIntersection(lineAStart, lineAEnd, lineBStart, lineBEnd):
    x1 = lineAStart[0]
    y1 = lineAStart[1]
    x2 = lineAEnd[0]
    y2 = lineAEnd[1]

    x3 = lineBStart[0]
    y3 = lineBStart[1]
    x4 = lineBEnd[0]
    y4 = lineBEnd[1]

    denominator = ((x1-x2)*(y3-y4)) - ((y1-y2)*(x3-x4))
    if denominator == 0.0:
        return -1

    t = ( ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4)) ) / denominator
    u =-( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)) ) / denominator

    if (t > 0.0) and (t < 1.0) and (u > 0.0) and (u < 1.0):

        x = x1 + (t * (x2 - x1))
        y = y1 + (t * (y2 - y1))

        return (x, y)
    
    return -1