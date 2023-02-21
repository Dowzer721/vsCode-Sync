
# PID Equation Diagram:
# https://upload.wikimedia.org/wikipedia/commons/4/43/PID_en.svg

# Helpful image for tuning:
# https://www.rchelicopterfun.com/images/PID_7_250pics.jpg

import matplotlib.pyplot as plt

from random import randint

m = 0.1
kP = 0.0005 * m
kI = 0.0 * m
kD = 0.005 * m

tgt = 100
pos = randint(0, tgt * 2)
vel = 0
acc = 0

numberOfEpocs = int(2000 / m)
samplingTime = 1

pError = 0
iError = 0
dError = 0
prevError = 0
currError = tgt - pos

allAcc = []
allPositions = []

for epoc in range(numberOfEpocs):

    currError = tgt - pos
    
    pError = currError
    iError = iError + (currError * samplingTime)
    dError = (currError - prevError) / samplingTime

    prevError = currError

    acc = (kP * pError) + (kI * iError) + (kD * dError)
    vel += acc
    pos += vel

    allPositions.append(pos)

# print(f"min:{tgt - max(allPositions)}, max:{tgt - min(allPositions)}")

plt.plot(list(range(numberOfEpocs)), [tgt]*numberOfEpocs, label="Target")

plt.plot(list(range(numberOfEpocs)), allPositions, label="Position")
plt.legend()
plt.show()