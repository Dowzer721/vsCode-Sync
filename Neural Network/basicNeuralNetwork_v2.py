
import math
import random

layerNeuronCount = (6, 4, 2)

weightShapes = [(x, y) for x,y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])]
biasShapes = [(count, 1) for count in layerNeuronCount[1:]]

def randomFloat(min_=0.0, max_=1.0, dec_=3):
    rng = max_ - min_
    pct = random.randint(0, 10**dec_) / float(10**dec_)
    return round( min_ + (rng * pct), dec_ )

dataLength = 4
dataInputs = []
dataOutputs= []
for _ in range(dataLength):
    dataInputs.append([randomFloat() for _ in range(layerNeuronCount[0])])
    dataOutputs.append([random.randint(0, 1) for _ in range(layerNeuronCount[-1])])

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

class NeuralNetwork:
    def __init__(self):

        self.weights = []
        for i in range(len(layerNeuronCount)-1):
            r = layerNeuronCount[i]
            c = layerNeuronCount[i+1]
            newWeights = [[randomFloat(-1, 1) for _ in range(c)] for _ in range(r)]
            # newWeights = [[1.0] * c] * r
            self.weights.append(newWeights)
        # print(f"Weights: {self.weights}")

        self.biases = []
        for j in layerNeuronCount:
            newBiases = [randomFloat(-1, 1) for _ in range(j)]
            # newBiases = [0.1] * j
            self.biases.append(newBiases)
        # print(f"Biases: {self.biases}")

        self.neuronValues = [[0.0]*count for count in layerNeuronCount]
        # print(f"Values: {self.neuronValues}")

        self.errorValues  = [[1.0]*count for count in layerNeuronCount]
    
    def predict(self, inputs, expectations):
        for i in range(layerNeuronCount[0]):
            self.neuronValues[0][i] = inputs[i] + self.biases[0][i]

        for layer in range(1, len(layerNeuronCount)):
            newValues = [0.0] * layerNeuronCount[layer]
            for val in range(layerNeuronCount[layer]):
                # To interpret this line a bit easier, it is suggested to print self.weights and self.biases as this can aid in understanding.
                newValues[val] = self.biases[layer][val] + sum([self.neuronValues[layer-1][n] * self.weights[layer-1][n][val] for n in range(layerNeuronCount[layer-1])])
            
            newValues = activationFunction(newValues, 'sigmoid')
            self.neuronValues[layer] = newValues
        
        # print(self.neuronValues)
        for v in range(layerNeuronCount[-1]):
            self.errorValues[-1][v] = expectations[v] - self.neuronValues[-1][v]
        
        # There needs to be the calculation of what the errorValues should be at each layer, 
        # not just the final layer. The final layer is simple, as it's what was supposed to be predicted 
        # minus what actually was. 
        # However, I don't know how to calculate what the other layers' errorValues should be. 
        # It might be worth checking Daniel Shiffman's video "Back Propogation pt 3" as I believe that 
        # goes into it. 
        # However the language is different (JS) and the approach is different also, so it will need some 
        # translation.
        # This calculation will go here:
    
    def adjustWeights(self):
        # Each weight is equal to (itself / sum(all other weights in that layer)) * (error of 
        # neuron it connects TO)
        
        for layer in range(len(layerNeuronCount)-2, -1, -1):
            # layerNeuronCount = (6, 4, 2) 
            # print(layer)
            # >> 1, 0
            
            # Calculate the sum of the weights at the current layer:
            weightSum = 0.0
            for previousNode in range(0, layerNeuronCount[layer]):
                for nextNode in range(0, layerNeuronCount[layer+1]):
                    weightSum += self.weights[layer][previousNode][nextNode]
            # print(weightSum)

            # Adjust the weights for the current layer:
            for previousNode in range(0, layerNeuronCount[layer]):
                for nextNode in range(0, layerNeuronCount[layer+1]):
                    currentWeight = self.weights[layer][previousNode][nextNode]
                    newWeight = (currentWeight / weightSum) * self.errorValues[layer+1][nextNode]
                    self.weights[layer][previousNode][nextNode] = newWeight

NN = NeuralNetwork()

correctCount = 0
numberOfIterations = 100
for d in range(numberOfIterations):
    currentDataInput = dataInputs[d % dataLength]
    currentDataOutput= dataOutputs[d % dataLength]
    NN.predict(currentDataInput, currentDataOutput)
    NN.adjustWeights()

    predictionValues = [round(val) for val in NN.neuronValues[-1]]
    # print(f"Output={currentDataOutput}, Prediction={predictionValues}, Match={currentDataOutput==predictionValues}")
    correctCount += int(currentDataOutput == predictionValues)

print(f"Correct Percentage= {correctCount * 100.0 / numberOfIterations}%")