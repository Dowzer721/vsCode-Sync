
import copy
import math
import random

layerNeuronCount = [6, 4, 2] # [int(count) for count in input("Enter the counts of neurons per layer, separated by commas: ").split(",")]

weightShapes = [(x, y) for x,y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])]
biasShapes = [(count, 1) for count in layerNeuronCount[1:]]
# print(weightShapes)
# print(biasShapes)

def randomFloat(min_ = 0.0, max_ = 1.0, dec_ = 2):
    rng = max_ - min_
    pct = random.randint(0, 10 ** dec_) / float(10 ** dec_)
    return round(min_ + (rng * pct), dec_)

dataLength = 3
dataInputsMin, dataInputsMax = -1.0, 1.0
dataOutputsMin, dataOutputsMax = -1.0, 1.0
dataInputs = []
dataOutputs= []
for _ in range(dataLength):
    dataInputs.append( [randomFloat(dataInputsMin, dataInputsMax) for _ in range(layerNeuronCount[0])] )
    dataOutputs.append( [randomFloat(dataOutputsMin, dataOutputsMax) for _ in range(layerNeuronCount[-1])] )
# print(dataInputs[0])
# print(dataOutputs[0])

# mode: '' | 'sigmoid' | 'aggressive_sigmoid' | 'relu' | 'leaky' | tanh
def activationFunction(xIn, mode = '', aggressive_sigmoid_multiplier = -10.0, leaky_multiplier = 0.01):
    # If no mode is given, then nothing needs to be changed, 
    # and therefore it's quicker just to return the original list
    if mode == '': return xIn

    for val in range(len(xIn)):
        if mode == 'sigmoid':
            xIn[val] = 1.0 / (1.0 + math.exp(-xIn[val]))
        elif mode == 'aggressive_sigmoid':
            xIn[val] = 1.0 / (1.0 + math.exp(aggressive_sigmoid_multiplier * xIn[val]))
        elif mode == 'relu':
            xIn[val] *= int(xIn[val] > 0.0)
        elif mode == 'leaky':
            xIn[val] *= (int(xIn[val] > 0.0) * (1.0 - leaky_multiplier)) + leaky_multiplier
        elif mode == 'tanh':
            xIn[val] = math.tanh(xIn[val])
    return xIn

def randomMatrix(width_, height_, min_=-1.0, max_=1.0):
    matrix = [
        [randomFloat(min_, max_) for _ in range(width_)]
        for _ in range(height_)
    ]
    if height_ == 1: # This will be true when creating a matrix for the biases
        matrix = matrix[0]
    return matrix

class NeuralNetwork:
    def __init__(self):
        self.weights = [randomMatrix(shape[0], shape[1]) for shape in weightShapes]
        self.biases  = [randomMatrix(shape[0], shape[1]) for shape in biasShapes]

        # self.weights = [[[1.0 for _ in range(shape[0])] for _ in range(shape[1])] for shape in weightShapes]
        # self.biases = [[1.0 for _ in range(shape[0])] for shape in biasShapes]

        # print(self.weights)
        # print(self.biases)

        self.neuronValues = [[0.]*count for count in layerNeuronCount]

        self.errorValues = [[0.]*count for count in layerNeuronCount]
    
    def predict(self, inputs, correctOutputs):

        self.neuronValues[0] = inputs

        # layerValues = inputs
        # for wMatrix, bMatrix in zip(self.weights, self.biases):

        for layer in range(1, len(layerNeuronCount)):
            # layer:  1 => len(layerNeuronCount)-1
            previousNeuronCount = layerNeuronCount[layer-1] # 6, 4
            currentNeuronCount  = layerNeuronCount[layer] #   4, 2

            # Neuron = weighted sum + bias
            # yn = sum(x * wn) + bn

            for neuron in range(currentNeuronCount):
                self.neuronValues[layer][neuron] = sum([self.neuronValues[layer-1][previousNeuron] * self.weights[layer-1][previousNeuron][neuron] for previousNeuron in range(previousNeuronCount)]) + self.biases[layer-1][neuron]
            self.neuronValues[layer] = activationFunction(self.neuronValues[layer], 'sigmoid')

        # print(f"Outputs: {self.neuronValues[-1]}")

        self.errorValues[-1] = [correctOutputs[value] - self.neuronValues[-1][value] for value in range(layerNeuronCount[-1])]
    
    def adjustWeights(self, correctOutputs):

        # print(f"Correct: {correctOutputs}")
        # print(f"Error:   {self.errorValues[-1]}")

        
        # (6, 4, 2)
        currentNeuronCount = layerNeuronCount[-1] # 2
        previousNeuronCount= layerNeuronCount[-2] # 4

        for prevNeuron in range(previousNeuronCount):
            weightSum = sum(self.weights[-1][prevNeuron]) * 0.01

            for currNeuron in range(currentNeuronCount):
                # weight -= (errorValue / weight)

                # self.weights[-1][prevNeuron][currNeuron] -= (self.weights[-1][prevNeuron][currNeuron] / self.errorValues[-1][currNeuron])
                # self.weights[-1][prevNeuron][currNeuron] -= (self.errorValues[-1][currNeuron] / self.weights[-1][prevNeuron][currNeuron])
                self.weights[-1][prevNeuron][currNeuron] -= (self.weights[-1][prevNeuron][currNeuron] * self.errorValues[-1][currNeuron]) / weightSum
                pass
                
            # self.neuronValues[layer] = activationFunction(self.neuronValues[layer], 'sigmoid')
            self.weights[-1][prevNeuron] = activationFunction(self.weights[-1][prevNeuron], 'sigmoid')
        





NN = NeuralNetwork()
NN.predict(dataInputs[0], dataOutputs[0])
print(NN.errorValues[-1])

for _ in range(1000):
    NN.predict(dataInputs[0], dataOutputs[0])
    NN.adjustWeights(dataOutputs[0])

print(NN.errorValues[-1])