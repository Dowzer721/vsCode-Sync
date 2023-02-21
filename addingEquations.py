
from math import pi, cos, sin, tan

# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

numberOfPoints = 2 ** 6

plotX = []
plotY = []

for i in range(numberOfPoints + 1):
    angle = i * pi * 2 / numberOfPoints

    x, y = (0,0)

    # Simple unit circle
    x += cos(angle)
    y += sin(angle)

    # Simple unit square
    x += round(cos(angle))
    y += round(sin(angle))
    
    # Pointed star
    starPointCount = 4 # numberOfPoints // 8
    currentSegment = int(angle / (pi/starPointCount))
    angleDifference = 0
    if currentSegment % 2 == 0: # Even segment:
        angleDifference = (currentSegment * pi / starPointCount) - angle
    else:
        angleDifference = angle - ((currentSegment+1) * pi / starPointCount)
    
    x -= cos(angle) * angleDifference
    y -= sin(angle) * angleDifference
    

    
    
    
    plotX.append(x)
    plotY.append(y)

xMax, yMax = max(plotX), max(plotY)
for i in range(numberOfPoints + 1):
    plotX[i] /= xMax
    plotY[i] /= yMax


figure = plt.figure()
ax = figure.add_subplot()

plt.title(f"Vertices = {numberOfPoints}")
plt.plot(plotX, plotY)
ax.set_aspect('equal', adjustable='box')

# plt.axis('off')
plt.show()