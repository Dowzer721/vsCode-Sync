
"""
This version creates a number of layers of noise, then combines them; each with scaling influence.

The number of layers is chosen by "noiseCount", and the resolution by "res". 
"""


import copy

import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
# https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.RcParams

import matplotlib.pyplot as plt

import progressbar
from random import randint, seed

# seed(100)

res = 64
noiseCount = 9
plotShape = (3, 3) # Must be integers AND must multiply to "noiseCount"

def generateNoise(smoothingCount=int(res/4)):
    noise = [
        [randint(0, 255) for _ in range(res)]
        for _ in range(res)
    ]

    for _ in range(smoothingCount):
        newNoise = copy.copy(noise)
        for yc in range(res):
            yp = yc - 1
            yn = (yc + 1) % res
            for xc in range(res):
                xp = xc - 1
                xn = (xc + 1) % res
                neighbourValues = [
                    noise[yp][xp], noise[yp][xc], noise[yp][xn],
                    noise[yc][xp],                noise[yc][xn],
                    noise[yn][xp], noise[yn][xc], noise[yn][xn]
                ]
                newNoise[yc][xc] = sum(neighbourValues) / len(neighbourValues)
        
        noise = newNoise
    
    return noise


def combineNoise(noises, layerWeighting):
    
    newNoise = [
        [0.0 for _ in range(res)]
        for _ in range(res)
    ]

    for noise in range(noiseCount):
        noiseWeight = layerWeighting[noise]
        for y in range(res):
            for x in range(res):
                newNoise[x][y] += (noises[noise][x][y] * noiseWeight)

    for y in range(res):
        for x in range(res):
            newNoise[x][y] /= float(noiseCount)

    
    return newNoise



print(f"Generating noise ({noiseCount}x): ")
noiseLayers = [
    generateNoise()
    for _ in progressbar.ProgressBar()(range(noiseCount))
]

print(f"Combining noise.")
combinedNoise = combineNoise(noiseLayers, [i/noiseCount for i in range(1, noiseCount+1)])

fig1, axs1 = plt.subplots(plotShape[0], plotShape[1])
fig2, axs2 = plt.subplots(1)

fig1.canvas.set_window_title("Generated Noise")
fig1.tight_layout()

for i in range(noiseCount):
    
    x = i % plotShape[0]
    y = int(i / plotShape[0])

    axs1[x, y].imshow(noiseLayers[i], "gray")
    axs1[x, y].set_title("Noise weight: " + str(round((i+1)/noiseCount, 2)) )

fig2.canvas.set_window_title("Combined Noise")
axs2.imshow(combinedNoise, "gray")

plt.show()