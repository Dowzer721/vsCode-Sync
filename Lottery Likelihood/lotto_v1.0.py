
from random import randint

# (Minimum possible value, maximum possible value)
digitRange = (1, 9)

targetDigits = [1, 2, 3, 4]
numberOfDigits = len(targetDigits)

digitsAccepted = True
for digIndex, dig in enumerate(targetDigits):
    if (dig < digitRange[0]) or (dig > digitRange[1]):
        print(f"Digit[{digIndex}] = {dig}, which is outside of the accepted range ({digitRange[0]} -> {digitRange[1]}).")
        digitsAccepted = False

if digitsAccepted == False:
    exit()

attemptCounter = 0
attemptCorrect = False

# print("Beginning process: ")
while not attemptCorrect:
    randomDigits = [randint(digitRange[0], digitRange[1]) for _ in range(numberOfDigits)]
    attemptCounter += 1
    attemptCorrect = (randomDigits == targetDigits)
    # print(randomDigits)

print(f"Target {targetDigits} randomly reached in {attemptCounter} attempts.")
print(f"This gives a likelihood of {round(100/attemptCounter, 5)}%. ")