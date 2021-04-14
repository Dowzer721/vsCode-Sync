
import matplotlib.pyplot as plt
import numpy as np
from progressbar import progressbar
from random import randint, seed

# seed(0)
# np.random.seed(0)

def randomFloat(min_ = 0.0, max_ = 1.0, dec_ = 2):
    rng = max_ - min_
    pct = randint(0, 10 ** dec_) / float(10 ** dec_)
    return round(min_ + (rng * pct), dec_)

dataIn = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1)
]
dataOut = [
    int(data[0] ^ data[1]) # carat is xor operator
    for data in dataIn
]

networkShape = (2, 4, 1)
mutationRate = 0.01
mutationStep = 0.01
netCount = 100
evolveCount = 50

weightShapes = [
    (x, y) for x,y in zip(networkShape[1:], networkShape[:-1])
]
biasShapes = [
    (count, 1) for count in networkShape[1:]
]

class NN:
    def __init__(self, id_):
        self.id = id_

        self.weights = [np.random.standard_normal(shape) for shape in weightShapes]
        self.biases = [np.random.standard_normal(shape) for shape in biasShapes]

        # print(self.weights)
        # print(self.biases)
    
    def makeGuess(self, inputs, expectedOutput):
        layerValues = inputs
        for wMat, bMat in zip(self.weights, self.biases):
            layerValues = np.matmul(wMat, layerValues) + bMat
        
        guess = layerValues.tolist()[0][0]
        
        # Cost = (guess - correct) ** 2
        # Cost = (a - y) ** 2
        Cost = (guess - expectedOutput) ** 2
        
        return Cost, guess
        # return int(10.0 / Cost)
    
    def mutate(self):
        self.weights = np.where(
            randomFloat() <= mutationRate,
            self.weights,
            self.weights + randomFloat(-mutationStep, mutationStep)
        )
        self.biases = np.where(
            randomFloat() <= mutationRate,
            self.biases,
            self.biases + randomFloat(-mutationStep, mutationStep)
        )


nets = [NN(id) for id in range(netCount)]

def crossover(parentA, parentB, newID):
    pAWeights = parentA.weights
    pBWeights = parentB.weights

    pABiases = parentA.biases
    pBBiases = parentB.biases

    pA_crossoverRatio = randomFloat()
    pB_crossoverRatio = (1.0 - pA_crossoverRatio) * 0.5
    pA_crossoverRatio *= 0.5

    childWeights = np.multiply(pAWeights, pA_crossoverRatio) + np.multiply(pBWeights, pB_crossoverRatio)
    childBiases  = np.multiply(pABiases,  pA_crossoverRatio) + np.multiply(pBBiases,  pB_crossoverRatio)

    child = NN(newID)
    child.weights = childWeights
    child.biases  = childBiases
    child.mutate()

    return child


yAxis = []
pbar = progressbar.ProgressBar()
for _ in pbar(range(evolveCount)):

    networkCosts = []
    for net in nets:
        totalCost = 0.0
        for d in range(4):
            totalCost += net.makeGuess(dataIn[d], dataOut[d])[0]
        
        networkCosts.append(totalCost)
        
    # print(f"Costs: {networkCosts}")
    
    matingPoolAdditionCounts = [
        int(max(networkCosts) / networkCosts[n])
        for n in range(netCount)
    ]
    # print(f"adds: {matingPoolAdditionCounts}")

    # This will be my measure of how the system is evolving:
    yAxis.append(max(networkCosts))

    matingPool = []
    for n in range(netCount):
        for _ in range(matingPoolAdditionCounts[n]):
            matingPool.append(n)
    # print(matingPool)

    newNetworks = []
    for newID in range(netCount):
        parentA = nets[matingPool[randint(0, len(matingPool)-1)]]
        parentB = nets[matingPool[randint(0, len(matingPool)-1)]]
        child = crossover(parentA, parentB, newID)
        newNetworks.append(child)
    
    nets = newNetworks



# plt.plot(range(evolveCount), yAxis)
# plt.show()

for d in range(4):
    inputs = dataIn[d]
    output = dataOut[d]
    guess = round(nets[0].makeGuess(inputs, output)[1])
    print(f"input:{inputs}, output:{output}, guess:{guess}")