from matplotlib import pyplot as plt
from random import randint
from time import time


def randomLetter():
    letters = [chr(65 + i) for i in range(26)] # A-Z: 26
    return letters[randint(0, len(letters)-1)]

target = ""
output = ""

highestSequenceLength = 5
maxSeconds = 120
print(f"Maximum run time is: {round(highestSequenceLength * maxSeconds / 60, 2)} minutes")

plotX = []
plotY = []

for sequenceLength in range(1, highestSequenceLength+1):

    target = ''.join([randomLetter() for _ in range(sequenceLength)])
    output = ""


    maxTimeReached = False

    startTime = time()
    while output != target:
        output = ''.join([randomLetter() for _ in range(len(target))])

        currentTime = time()
        currentDifTime = currentTime - startTime
        if currentDifTime > maxSeconds:
            print(f"Sequence of length {sequenceLength} has taken greater than {maxSeconds} seconds, stopping.")
            maxTimeReached = True
            break

    if maxTimeReached:
        break

    endTime = time()
    difTime = endTime - startTime

    plotX.append(sequenceLength)
    plotY.append(difTime)

    print(f"Sequence {sequenceLength}/{highestSequenceLength} complete.")

    # print(f"Target: {target}, Output: {output}")
    # print(f"Time taken: {difTime}")


plt.plot(plotX, plotY)

plt.title("Random monkeys")

plt.xlabel("Sequence Length")
plt.xticks(range(1, highestSequenceLength + 1))

plt.ylabel("Time taken (seconds)")

plt.show()