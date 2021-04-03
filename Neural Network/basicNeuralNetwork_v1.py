
import copy
import numpy as np
import random

layerNeuronCount = (6, 4, 2)
activationMethod = 'sigmoid' # '' | 'sigmoid' | 'aggressive_sigmoid' | 'relu' | 'leaky' | 'tanh' |
learningRate = 0.05

dataLength = 50
inputCount = layerNeuronCount[0]

dataInputs = []
dataOutputs= []

for _ in range(dataLength):
    dataInputs.append(np.asmatrix(
        [random.randint(0, 1000) / 1000.0 for _ in range(inputCount)]
    ).reshape((inputCount, 1)))

    if layerNeuronCount[-1]==1:
        dataOutputs.append([random.randint(0, 1)])
    else:
        newOutput = random.randint(0, layerNeuronCount[-1]-1)
        dataOutputs.append([int(i==newOutput) for i in range(layerNeuronCount[-1])])
# print(dataInputs[0])
# print(dataOutputs[0])

def multiplyArrays(a, b):
    
    newA = copy.deepcopy(a)
    
    for row in range(len(a)):
        newA[row] = newA[row] * b[row]
    
    return newA


class NeuralNetwork:
    def __init__(self, id_ = -1):
        self.id = id_

        self.weightShapes = [(x,y) for x,y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])]
        self.biasShapes = [(count, 1) for count in layerNeuronCount[1:]]

        self.weights = [np.random.standard_normal(shape) / (shape[1]**0.5) for shape in self.weightShapes]
        # self.weights = [np.random.randint(0, 2, shape)*1.0 for shape in self.weightShapes]
        self.biases  = [np.random.standard_normal(shape) for shape in self.biasShapes]

        # input(self.weights[1])
        # self.backPropogate()
        # input()

        # self.weights = [np.random.uniform(-1, 1, shape) for shape in self.weightShapes]
        # self.biases  = [np.random.uniform(-1, 1, shape) for shape in self.biasShapes]

        self.predictions = 0
        self.errorValues = 0
    
    def makePrediction(self, inputs, expectedOutput):
        
        layerValues = inputs
        for weightMatrix, biasMatrix in zip(self.weights, self.biases):
            layerValues = self.activate(
                np.matmul(weightMatrix, layerValues) + biasMatrix
            )
        
        self.prediction = [np.asarray(layerValues[i])[0][0] for i in range(layerNeuronCount[-1]) ]
        # print(self.prediction)

        self.errorValues = [expectedOutput[i] - self.prediction[i] for i in range(layerNeuronCount[-1])]
        # self.errorValues = [self.prediction[i] - expectedOutput[i] for i in range(layerNeuronCount[-1])]
        # print(self.errorValues)
    
    def backPropogate(self):

        weightsReversed = copy.deepcopy(self.weights)
        weightsReversed.reverse()

        for m in range(len(weightsReversed)):
            weightMatrix = weightsReversed[m]
            weightDivision = 1.0 / weightMatrix.sum(axis=1)
            weightsReversed[m] = multiplyArrays(weightMatrix, weightDivision) #* self.errorValues[m]
        
        # print(weightsReversed)
        self.weights = weightsReversed.reverse()


        

        # if activationMethod == 'sigmoid':
        #     pass
            
        # elif activationMethod == 'aggressive_sigmoid':
        #     pass
        # elif activationMethod == 'relu':
        #     pass
        # elif activationMethod == 'leaky':
        #     pass
        # elif activationMethod == 'tanh':
        #     pass

        # errorSum = sum(self.errorValues)
        # addMin = min(0, errorSum)
        # addMax = max(errorSum, 0)

        # min_ = 0
        # max_ = errorSum
        # rng = max_ - min_
        # pct = random.randint(0, 1000) / 1000.0
        # return min_ + (rng * pct)
        # return min_ + ( (max_ - min_) * (random.randint(0, 1000) / 1000.0) )
        # return addMin + ( (addMax - addMin) * (random.randint(0, 1000) / 1000.0) )
        
        # for i in range(len(layerNeuronCount)-1):
        #     self.weights[i] = np.add(self.weights[i], np.random.uniform(0, errorSum * learningRate, np.shape(self.weights[i])) )

            # self.weights[i] = np.add(self.weights[i], np.random.uniform(addMin, addMax, np.shape(self.weights[i])) )
            # self.weights[i] = np.add(self.weights[i], np.full(np.shape(self.weights[i]), errorSum * learningRate))
            
            # errorAddition = addMin + ( (addMax - addMin) * (random.randint(0, 1000) / 1000.0) )
            # errorAddition = errorSum + ( (0 - errorSum) * (random.randint(0, 1000) / 1000.0) )
            # self.weights[i] = np.add(self.weights[i], np.full(np.shape(self.weights[i]), errorAddition))


        # for weightMatrix in self.weights:
        #     weightMatrix = np.add(weightMatrix, np.random.uniform(0, errorSum, np.shape(weightMatrix)) )
        

    @staticmethod
    def activate(x):
        if activationMethod == 'sigmoid':
            return 1.0 / (1.0 + np.exp(-x))
        elif activationMethod == 'aggressive_sigmoid':
            return 1.0 / (1.0 + np.exp(-10.0 * x))
        elif activationMethod == 'relu':
            return np.where(x < 0.0, 0.0, x)
        elif activationMethod == 'leaky':
            return np.where(x < 0.0, x * 0.01, x)
        elif activationMethod == 'tanh':
            return np.tanh(x)

        return x

NN = NeuralNetwork(0)

errorSum = 1.0
while(abs(errorSum) > 0.001): #1.0 / dataLength):
# for _ in range(100):

    errorSum = 0.0
    for dataIndex in range(dataLength):
        NN.makePrediction(dataInputs[dataIndex], dataOutputs[dataIndex])
        # errorSum += abs(sum(NN.errorValues))
        errorSum += sum(NN.errorValues)
    errorSum /= dataLength
    print("%.5f" %errorSum)

    NN.backPropogate()

print("\n"*3)
for d in range(dataLength):
    NN.makePrediction(dataInputs[d], dataOutputs[d])

    expectedOutput = dataOutputs[d]
    predictedOutput= [int(round(pred)) for pred in NN.prediction]

    print(expectedOutput , ": ", predictedOutput, ": ", end="")
    print(expectedOutput == predictedOutput)