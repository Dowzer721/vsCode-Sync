from math import pi, cos, sin

from matplotlib import pyplot as plt

numberOfPoints = 2**6

def getXY(i, *functions):
    
    theta = i * 2 * pi / numberOfPoints
    thetaMod = theta % (pi / 2)
    thetaQuarter = round(theta / (pi/2))
    
    x, y = (0, 0)
    for f in functions:
        functionX, functionY = f(theta, thetaMod, thetaQuarter)
        x += functionX
        y += functionY
    
    return (round(x, 3), round(y, 3))

plotX = []
plotY = []

for i in range(numberOfPoints + 1):
    x, y = getXY(i, 
        # lambda *args: (round(cos(args[0])), round(sin(args[0]))),
        # lambda *args: (cos(args[0]), sin(args[0])),
        lambda *args: (cos(args[1] / (pi/2)), sin(args[1] / (pi/2)))
    )
    # print(f"i: {i}, x: {x}, y: {y}")
    plotX.append(x)
    plotY.append(y)

plt.title(f"N = {numberOfPoints}")
plt.plot(plotX, plotY)
# plt.scatter(plotX, plotY)
plt.show()