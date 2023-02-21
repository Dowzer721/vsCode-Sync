
import math
import matplotlib.pyplot as plt
import random

# Equation: y = mx + b
# Variables: m, b - (2, 3)

# Equation: y = ax^2 + bx + c
# Variables: a, b, c - (2, 4, 5)

variableTargetValues = (2, 4, 5)
numberOfVariables = len(variableTargetValues)
sampleRange = range(-10, 10)
targetPoints = [
    # (x, variableTargetValues[0]*x + variableTargetValues[1])
    (x, variableTargetValues[0]*x**2 + variableTargetValues[1]*x + variableTargetValues[2])
    for x in sampleRange
]
# print(targetPoints)


mutationChance = 0.4 # Percentage
mutationRate = 0.1 # Change

def mutate(startingValues):
    if random.random() <= mutationChance:
        mutatedValues = []
        for value in startingValues:
            _percentage = random.randint(0, 1000) / 1000.0
            _range = mutationRate
            _sign = (random.randint(0, 1) * 2) - 1
            mutatedValues.append(value + (_percentage * _range * _sign) )
        return mutatedValues
    return startingValues

def crossover(parentA, parentB):
    child = []
    for variableIndex in range(numberOfVariables):
        child.append( (parentA[variableIndex] + parentB[variableIndex]) / 2 )
    return mutate(child)

populationSize = 20
Population = [
    tuple([random.random() for _ in range(numberOfVariables)])
    # tuple([0 for _ in range(numberOfVariables)])
    for _ in range(populationSize)
]

numberOfEpocs = 100
for epoc in range(numberOfEpocs):

    PopulationFitness = []
    for IndividualIndex, IndividualVariables in enumerate(Population):
        IndividualPoints = [
            # (x, IndividualVariables[0]*x + IndividualVariables[1])
            (x, IndividualVariables[0]*x**2 + IndividualVariables[1]*x + IndividualVariables[2])
            for x in sampleRange
        ]
        IndividualFitness = sum([
            (IndividualPoints[x-sampleRange.start][1] - targetPoints[x-sampleRange.start][1]) ** 2
            for x in sampleRange
        ])
        PopulationFitness.append((IndividualIndex, IndividualFitness))
    maximumFitness = max([IndividualFitness[1] for IndividualFitness in PopulationFitness])


    matingPool = []
    for index, fitness in PopulationFitness:
        matingPoolAdditionCount = int(maximumFitness - fitness)
        for _ in range(matingPoolAdditionCount):
            matingPool.append(index)
    matingPoolSize = len(matingPool)
    if matingPoolSize == 0:
        matingPool = [i for i in range(populationSize)]
        matingPoolSize = len(matingPool)

    # input(matingPool)

    newPopulation = []
    for _ in range(populationSize):
        parentAIndex = parentBIndex = -1
        while parentAIndex == parentBIndex:
            parentAIndex = random.randint(0, matingPoolSize-1)
            parentBIndex = random.randint(0, matingPoolSize-1)
        parentA = Population[ matingPool[parentAIndex] ]
        parentB = Population[ matingPool[parentBIndex] ]
        child = crossover(parentA, parentB)
        newPopulation.append(child)
    
    Population = newPopulation

bestIndividualIndex = 0
bestIndividualFitness = math.inf
for IndividualIndex, IndividualVariables in enumerate(Population):
    IndividualPoints = [
        # (x, IndividualVariables[0]*x + IndividualVariables[1])
        (x, IndividualVariables[0]*x**2 + IndividualVariables[1]*x + IndividualVariables[2])
        for x in sampleRange
    ]
    IndividualFitness = sum([
        (IndividualPoints[x-sampleRange.start][1] - targetPoints[x-sampleRange.start][1]) ** 2
        for x in sampleRange
    ])
    if IndividualFitness < bestIndividualFitness:
        bestIndividualFitness = IndividualFitness
        bestIndividualIndex = IndividualIndex

evolvedVariables = Population[bestIndividualIndex]
print(evolvedVariables)

targetScatterX = []
targetScatterY = []
for tgt_pt in targetPoints:
    targetScatterX.append(tgt_pt[0])
    targetScatterY.append(tgt_pt[1])

evolvedScatterX = []
evolvedScatterY = []
for x in sampleRange:
    evolvedScatterX.append(x)
    # evolvedScatterY.append((evolvedVariables[0] * x) + evolvedVariables[1])
    evolvedScatterY.append(evolvedVariables[0]*x**2 + evolvedVariables[1]*x + IndividualVariables[2])

plt.plot(targetScatterX, targetScatterY)
plt.plot(evolvedScatterX, evolvedScatterY)
plt.show()

