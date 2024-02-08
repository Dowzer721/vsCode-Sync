
from math import exp
from random import randint

networkShape = (2, 1, 2)
populationSize = 100
epocCount = 1000

rf = lambda: randint(-1000, 1000) / 1000.0

def act(x):
    # Sigmoid:
    return 1 / (1 + exp(-x))

    # TanH:
    # return (2 / (1 + exp(-2*x))) - 1

class Net:
    def __init__(self, shape_):
        self.shape = shape_
        self.layerCount = len(shape_)

        self.nodes = [
            [0 for _ in range(nodeCount+1)]
            for nodeCount in shape_[:-1]
        ] + [[0 for _ in range(shape_[-1])]]
        for i in range(self.layerCount-1):
            self.nodes[i][-1] = rf()

        self.weights = []
        # Weight Reference: [weightLayer][startNode][endNode]

        # for Layer in range(self.layerCount - 1):
        #     startNodeCount = shape_[Layer]+1
        #     endNodeCount = shape_[Layer+1]+1
        #     if (Layer+1) == (self.layerCount-1):
        #         endNodeCount -= 1
        #     layerWeights = []
        #     for startNodeIndex in range(startNodeCount):
        #         startNodeWeights = []
        #         for endNodeIndex in range(endNodeCount):
        #             startNodeWeights.append(rf())
        #         layerWeights.append(startNodeWeights)
        #     self.weights.append(layerWeights)
        for Layer in range(self.layerCount-1):
            startNodeCount = shape_[Layer]+1
            endNodeCount = shape_[Layer+1]
            layerWeights = []
            for startNode in range(startNodeCount):
                startNodeWeights = [rf() for _ in range(endNodeCount)]
                layerWeights.append(startNodeWeights)
            self.weights.append(layerWeights)
    
    def guess(self, inputs):
        self.nodes[0] = inputs + [self.nodes[0][-1]]
        # print(self.nodes)
        for Layer in range(self.layerCount-1):
            startNodeCount = self.shape[Layer]
            endNodeCount = self.shape[Layer+1]
            for i in range(endNodeCount-1):
                self.nodes[Layer+1][i] = 0
            
            for eNI in range(endNodeCount): #endNodeIndex
                for sNI in range(startNodeCount): #startNodeIndex
                    # Weight Reference: [weightLayer][startNode][endNode]
                    connectingWeight = self.weights[Layer][sNI][eNI]
                    self.nodes[Layer+1][eNI] += self.nodes[Layer][sNI] * connectingWeight
                    self.nodes[Layer+1][eNI] = act(self.nodes[Layer+1][eNI])
        
        return self.nodes[-1]

def crossover(NetA, NetB):
    child = Net(networkShape)
    
    for Layer in range(child.layerCount-1):
        startNodeCount = child.shape[Layer]
        endNodeCount = child.shape[Layer+1]
        for eNI in range(endNodeCount): #endNodeIndex
            for sNI in range(startNodeCount): #startNodeIndex
                # Weight Reference: [weightLayer][startNode][endNode]
                aWeight = NetA.weights[Layer][sNI][eNI]
                bWeight = NetB.weights[Layer][sNI][eNI]
                child.weights[Layer][sNI][eNI] = (aWeight + bWeight) / 2
    
    return child

data = []
dataSize = 4
for dataIndex in range(dataSize): #0, 1, 2, 3: 00, 01, 10, 11
    # x = rf() * 100
    # y = rf() * 100
    # if x >= y:
    #     data.append([x,y,1,0])
    # else:
    #     data.append([x,y,0,1])
    bin_ = bin(dataIndex)[2:]
    if len(bin_) == 1: bin_ = '0' + bin_
    # print(bin_)
    x = int(bin_[0])
    y = int(bin_[1])
    z = x ^ y
    data.append([x, y, z, 1-z])

# print(data)
# input()

# averageIndividualError = [0 for _ in range(populationSize)]
# for d in data:
#     inputs = [d[0], d[1]]
#     outputs= [d[2], d[3]]
#     for individualIndex in range(populationSize):
#         guess = Networks[individualIndex].guess(inputs)
#         # error = sum([(outputs[i]-guess[i]) for i in range(2)])
#         error = sum([(guess[i]-outputs[i]) for i in range(2)])
#         averageIndividualError[individualIndex] += error
# for i, e in enumerate(averageIndividualError):
#     averageIndividualError[i] = e/dataSize

# print(averageIndividualError[randint(1, populationSize-1)])
# print(data[-1])
# print(inputs)
# print(outputs)
# print(guess)
# print(error)

Population = [
    Net(networkShape)
    for _ in range(populationSize)
]
for epoc in range(epocCount):
    averageIndividualError = [0 for _ in range(populationSize)]
    for index, Individual in enumerate(Population):
        for d in data:
            inputs = [d[0], d[1]]
            outputs= [d[2], d[3]]
            guess = Individual.guess(inputs)
            error = sum([(guess[i]-outputs[i]) for i in range(2)])
            # error = sum([(outputs[i]-guess[i]) for i in range(2)])
            averageIndividualError[index] += error
        averageIndividualError[index] /= dataSize
    
    newPopulation = []
    for p in range(populationSize):
        minimumError = min(averageIndividualError)
        parentAIndex = averageIndividualError.index(minimumError)
        averageIndividualError[parentAIndex] = 100+p
        
        minimumError = min(averageIndividualError)
        parentBIndex = averageIndividualError.index(minimumError)
        averageIndividualError[parentBIndex] = 100+p

        parentA = Population[parentAIndex]
        parentB = Population[parentBIndex]
        newPopulation.append(crossover(parentA, parentB))
    
    for i in range(populationSize):
        Population[i] = newPopulation[i]

    
    # indexedError = enumerate(averageIndividualError)
    
    # for i in indexedError:
    #     print(i)
    # input()

for d in data:
    # d = data[0]
    inputs = [d[0], d[1]]
    outputs= [d[2], d[3]]
    guess  = Population[0].guess(inputs)
    error  = sum([(guess[i]-outputs[i]) for i in range(2)])
    print(f"Inputs:{inputs}, Outputs:{outputs}, Guess:{guess}, Error:{error}")