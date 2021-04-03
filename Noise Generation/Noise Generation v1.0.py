
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import random


# def randomFloat(min_:'Minimum Value'=0.0, max_:'Maximum Value'=1.0, dec_:'Number of decimals'=2)->'RandomFloat':
def randomFloat(min_ = 0.0, max_ = 1.0, dec_ = 2):
    rng = max_ - min_
    pct = random.randint(0, 10 ** dec_) / float(10 ** dec_)
    return round(min_ + (rng * pct), dec_)

# print(randomFloat.__annotations__)

resolution = 512
w, h = [resolution] * 2
global grid
grid = [[0 for _ in range(w)] for _ in range(h)]

radiiCount = int(resolution * 2)
startingRadiusMin = w * 0.0
startingRadiusMax = w * 0.75
radii = [randomFloat(startingRadiusMin, startingRadiusMax) for _ in range(radiiCount)]
# radii = [((startingRadiusMax * 0.5) / radiiCount) * i for i in range(radiiCount)]

def drawLineOnGrid(start, end, numberOfPointsMultiplier = 1.5):

    sx = max(1, min(start[0], w-1))
    sy = max(1, min(start[1], h-1))

    ex = max(1, min(end[0], w-1))
    ey = max(1, min(end[1], h-1))

    dx = ex - sx
    dy = ey - sy

    # The angle from start to end:
    theta = math.atan2(dy, dx)

    # The distance from start to end:
    dist = math.sqrt((dx ** 2.0) + (dy ** 2.0))

    # The number of points to check along the route:
    numberOfPoints = int(dist * numberOfPointsMultiplier)

    for i in range(numberOfPoints):
        d = (dist / numberOfPoints) * i
        x = int(sx + (math.cos(theta) * d))
        y = int(sy + (math.sin(theta) * d))
        grid[y][x] = 1



def smoothRadii(smoothingCount = 1, smoothEdges = True, smoothingRate = 0.1):
    # smoothingCount = int(smoothingCount)

    end = radiiCount - int(not smoothEdges)
    for _ in range(smoothingCount):
        for c in range(0, end):
            # p: Previous, n: Next
            # if smoothEdges: p = c - 1 else p = c
            p = (c - 1 + radiiCount + int(not smoothEdges)) % radiiCount
            n = (c + 1) % radiiCount

            prevDiff = radii[c] - radii[p]
            radii[p] += (prevDiff * smoothingRate)

            nextDiff = radii[c] - radii[n]
            radii[n] += (nextDiff * smoothingRate)

def drawShape(resetGrid=False):
    if resetGrid:
        global grid
        grid = [[0 for _ in range(w)] for _ in range(h)]
    
    angleSegment = (math.pi * 2.0 / radiiCount)
    for c in range(radiiCount):
        n = (c + 1) % radiiCount

        angleC = angleSegment * c
        angleN = angleSegment * n

        cx = (w/2) + (math.cos(angleC) * radii[c])
        cy = (h/2) + (math.sin(angleC) * radii[c])
        nx = (w/2) + (math.cos(angleN) * radii[n])
        ny = (h/2) + (math.sin(angleN) * radii[n])

        drawLineOnGrid([cx, cy], [nx, ny])


plt.ion()
fig1, ax1 = plt.subplots()
array = np.zeros((resolution, resolution), dtype=np.uint8)
array[0, 0] = 1
axim1 = ax1.imshow(array, "gray")
del array

ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)


global stopSmoothingVariable
stopSmoothingVariable = False
def stopSmoothingMethod(event):
    global stopSmoothingVariable
    stopSmoothingVariable = True

buttonAxis = plt.axes([0.05, 0.005, 0.9, 0.1])
stopSmoothingButton = Button(buttonAxis, "Stop Smoothing")
stopSmoothingButton.on_clicked(stopSmoothingMethod)
smoothCount = resolution * 5
for i in range(0, smoothCount, 10):
    smoothRadii(10)
    drawShape(True)

    axim1.set_data(np.asmatrix(grid))
    fig1.canvas.flush_events()

    fig1.canvas.set_window_title("%.1f%% complete" %((i*100) / smoothCount))

    if stopSmoothingVariable:
        break

if stopSmoothingVariable == False:
    fig1.canvas.set_window_title("100.0% complete")

input()