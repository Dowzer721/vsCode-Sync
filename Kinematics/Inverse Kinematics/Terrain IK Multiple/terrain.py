
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

def createTerrain(terrainLength_, xScale_=1.0, yScale_=1.0):

    terrainNoise = LL.generate1DNoise(terrainLength_, noiseScale_=0.05, centerNoise_=0.5)
    # print(terrainNoise)
    terrainPoints = []
    for c in range(terrainLength_):
        x = (xScale_ / (terrainLength_ -1)) * c
        y = terrainNoise[c] * yScale_
        terrainPoints.append([x, y])
        # print(f"x:{x}, y:{y}")

    return terrainPoints

# createTerrain(20)