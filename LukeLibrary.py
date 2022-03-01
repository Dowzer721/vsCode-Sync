
"""
# Add this to beginning of file if not in same branch as this file:
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL


Fold all sections:
Ctrl+K, Ctrl+ZERO
Unfold all sections:
Ctrl+K, Ctrl+J

"""

from copy import copy

import math

import pygame
# pygame.init()
pygame.display.init()

import progressbar

# import random
from random import seed, randint
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

    @staticmethod
    def sum(vectorList, findAverage=False):
        returnVector = Vector(0, 0, 0)
        for vec in vectorList:
            returnVector.x += vec.x
            returnVector.y += vec.y
            if vec.z != None:
                returnVector.z += vec.z

        if findAverage:
            returnVector.x /= len(vectorList)
            returnVector.y /= len(vectorList)
            returnVector.z /= len(vectorList)

        return returnVector
    
    @staticmethod
    def fromTuple(tuple_):
        if len(tuple_) == 2:
            x, y = tuple_
            return Vector(x, y)
        elif len(tuple_) == 3:
            x, y, z = tuple_
            return Vector(x, y, z)

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
    def div(self, val):
        self.x /= val
        self.y /= val
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
    def randomRotation(self, amount=0.1):
        hdg = self.heading()
        newHdg = hdg + randomFloat(-amount, amount)
        self.rotateToAngle(newHdg)
    def addAngle(self, angle):
        newHeading = self.heading() + angle
        mag = self.getMag()
        self.x = math.cos(newHeading) * mag
        self.y = math.sin(newHeading) * mag
    def moveInDirection(self, angle, dist = 1.0):
        self.x += math.cos(angle) * dist
        self.y += math.sin(angle) * dist

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
    
    # --- Return manipulated self values:
    def toInt(self):
        return (int(self.x), int(self.y), 0 if self.z == None else int(self.z))
    def toScalar(self):
        if self.z == None:
            return (self.x, self.y)
        else:
            return (self.x, self.y, self.z)

    # --- Showing vector information:
    def render(self, startPosition, canvas, scale=1, colour=(255, 0, 255), thickness=4):
        
        if type(startPosition) is LL.Vector:
            x1, y1, _ = startPosition.toInt()
        elif type(startPosition) is tuple or type(startPosition) is list:
            x1 = int(startPosition[0])
            y1 = int(startPosition[1])

        x2 = x1 + int(self.x * scale)
        y2 = y1 + int(self.y * scale)

        pygame.draw.line(canvas, colour, (x1, y1), (x2, y2), thickness)
    def print(self):
        print(f"Vector: x={self.x}, y={self.y}, z={self.z}")

class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.start = Vector(x1, y1)
        self.end = Vector(x2, y2)

class Sensor:
    def __init__(self):
        self.position = Vector()
        self.direction = 0.0
        self.measuredDistance = -1.0 #pygame.Surface.get_width() * pygame.Surface.get_height()
    def update(self, pos, dir = 0.0):
        self.position.set(pos.x, pos.y)
        self.direction = dir
    def measure(self, wallList):
        cIPD = float("inf")# screen.get_width() * screen.get_height()
        
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
        
        if cIPD == float("inf"): #screen.get_width() * screen.get_height():
            self.measuredDistance = -1
        else:
            self.measuredDistance = cIPD
        
        return self.measuredDistance
    def render(self, screen, colour=(255, 100, 100), thickness=1):
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

def randomFloat(min_ = 0.0, max_ = 1.0, decimalPlaces_ = 3, seed_ = None):
    if seed_ != None: seed(seed_)
    
    min_ = min(min_, max_)
    max_ = max(min_, max_)
    
    rng = max_ - min_
    # random.seed(time.time())
    pct = randint(0, 10**decimalPlaces_) / float(10**decimalPlaces_)
    return float(round(min_ + (rng * pct), decimalPlaces_))

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
    
    return (int(val > 0) * 2) - 1

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

def smooth1DNoise(noiseArr, edgeLoop=True, feedback_=False):
    noiseLength = len(noiseArr)
    
    # pbar = progressbar.ProgressBar()
    # for curr in pbar(range(noiseLength)) if feedback_ else range(noiseLength):
    
    for curr in progressbar.ProgressBar()(range(noiseLength)) if feedback_ else range(noiseLength):
        if edgeLoop:
            prev = (curr + noiseLength - 1) % noiseLength
            next = (curr + 1) % noiseLength
        else:
            prev = max(0, curr - 1)
            next = min(curr + 1, noiseLength-1)
        prevDiff = noiseArr[prev] - noiseArr[curr]
        nextDiff = noiseArr[next] - noiseArr[curr]
        diffSum  = prevDiff + nextDiff
        noiseArr[curr] += diffSum
    
    # minNoise = min(noiseArr)
    # maxNoise = max(noiseArr)
    # maxMinDiff = maxNoise - minNoise
    # for c in range(noiseLength):
    #     noiseArr[c] = (noiseArr[c] - minNoise) / maxMinDiff

def generate1DNoise(noiseLength_, noiseScale_=0.1, noiseMin_=0.0, noiseMax_=1.0, precisionDP_=3, smooth_=True, smoothCount_=-1, edgeLoop_=True, feedback_=False, centerNoise_=None, seedForRandom_=None):

    if smoothCount_==-1:
        smoothCount_ = int(noiseLength_ * 1.5)
    # else:
    #     smoothCount_ = int(noiseLength_ * smoothCount_)

    noise = [randomFloat(noiseMin_, noiseMax_, precisionDP_, seed_=seedForRandom_) * noiseScale_ for _ in range(noiseLength_)]
    
    if smooth_:
        for _ in progressbar.ProgressBar()(range(smoothCount_)) if feedback_ else range(smoothCount_):
            smooth1DNoise(noise, edgeLoop=edgeLoop_)

    if centerNoise_ != None:
        avgNoiseValue = sum(noise) / noiseLength_
        diffFromCenter = avgNoiseValue - centerNoise_
        for n in range(noiseLength_):
            noise[n] -= diffFromCenter
        
    
    return noise

def smooth2DNoise(noiseArr, noiseScale=0.1, neighbourLayerCount=1, edgeLoop=False, feedback_=False):
    
    noiseWidth = len(noiseArr[0])
    noiseHeight= len(noiseArr)

    smoothedNoise = copy(noiseArr)

    for yc in progressbar.ProgressBar()(range(noiseHeight)) if feedback_ else range(noiseHeight):
    # for yc in range(noiseHeight):
        yp = yc-1
        yn = (yc+1) % noiseHeight
        for xc in range(noiseWidth):
            xp = xc-1
            xn = (xc+1) % noiseWidth

            smoothedNoise[yc][xc] = sum([
                noiseArr[yp][xp], noiseArr[yp][xc], noiseArr[yp][xn],
                noiseArr[yc][xp], noiseArr[yc][xc], noiseArr[yc][xn],
                noiseArr[yn][xp], noiseArr[yn][xc], noiseArr[yn][xn]
            ]) / 9.0
    
    return smoothedNoise

def generate2DNoise(noiseWidth, noiseHeight, noiseScale=0.1, precisionDP=3, smooth=True, smoothCount=-1, smoothEdgeLoop=False, feedback_=False):


    if smoothCount==-1:
        noiseHyp = math.sqrt((noiseWidth**2)+(noiseHeight**2))
        smoothCount = int(noiseHyp * 1.5)
    
    noise = [
        [randomFloat(decimalPlaces_=precisionDP) for _ in range(noiseWidth)]
        for _ in range(noiseHeight)
    ]

    if smooth:
        for _ in progressbar.ProgressBar()(range(smoothCount)) if feedback_ else range(smoothCount):
            noise = smooth2DNoise(noise, noiseScale, edgeLoop=smoothEdgeLoop)
    
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

def intToBinaryList(val, desiredListLength_=None):

    
    if desiredListLength_ == None:
        listLength = math.ceil(math.log2(val+1))
    else:
        listLength = desiredListLength_
    
    # Consider using bit-shifting here for efficiency
    
    ret = [0 for _ in range(int(listLength))]
    # print(f"val:{val}, len:{listLength}, list:{ret}")
    for i in range(listLength-1, -1, -1):
        if val >= (2 ** i):
            val -= (2 ** i)
            ret[i] = 1
    
    # print(f"val:{val}, ret:{ret}")
    return ret

def binaryListToInt(list_): # [0, 1, 0, 1, 1, 1] = 23
    # listLength = len(list_) # = 6

    # total = 0
    # for i in range(listLength-1, -1, -1): # 5, 4, 3, 2, 1, 0
    #     powerOfTwo = 2 ** (listLength-1 - i) # (2**0), (2**1), (2**3), ...
    #     total += powerOfTwo * list_[i]
    
    # return total

    return sum([ (2**(len(list_)-1 -i)) * list_[i] for i in range(len(list_)-1, -1, -1) ])

# print(binaryListToInt([0, 1, 0, 1, 1, 1]), ":23")
# print(binaryListToInt([1, 0, 1, 1]), ":11")

# This is the same as my "mapToRange()" method:
# def LinearInterpolation(x1, y1, x2, y2, x_):

    # return y1 + ((x_-x1) * (y2-y1))/(x2-x1)


def LineCoefficientsFromTwoPoints(A, B):
    
    # x1, x2 = A[0], B[0]
    # y1, y2 = A[1], B[1]

    # # y = mx + b
    # m = (y2 - y1) / (x2 - x1)
    # b = y1 - (m * x1)

    # # mx - y + b = 0
    # # Ax + By + C = 0

    # # mx - y + b = Ax + By + C
    
    Ax, Ay = A
    Bx, By = B

    a = Ay - By
    b = Bx - Ax
    c = ((Ax-Bx)*Ay) + ((By-Ay)*Ax)

    return a, b, c