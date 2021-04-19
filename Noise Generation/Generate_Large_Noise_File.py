
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

noiseWidth, noiseHeight = 64, 64

noise = LL.generate2DNoise(noiseWidth, noiseHeight)

fileLocation = "Noise Generation/largeNoiseFile.txt"
noiseFile = open(fileLocation, 'w')

for y in range(noiseHeight):
    for x in range(noiseWidth):
        noiseString = str(noise[y][x]) + ","
        noiseFile.write(noiseString)

    noiseFile.write("\n")

noiseFile.close()

print(f"Finished. File saved at {fileLocation}.")

import matplotlib.pyplot as plt

plt.imshow(noise, "gray")
plt.show()