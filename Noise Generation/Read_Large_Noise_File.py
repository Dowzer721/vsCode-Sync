
from random import randint

noise = []
for line in open("Noise Generation/largeNoiseFile.txt", 'r'):
    noiseValuesStrings = line.split(',')[:-1] # Final string in line is "\n", so this gets rid of it
    noiseRow = []
    for string in noiseValuesStrings:
        noiseRow.append(float(string))
    noise.append(noiseRow)

# noiseFile.close()

# import matplotlib.pyplot as plt

# plt.imshow(noise, "gray")
# plt.show()