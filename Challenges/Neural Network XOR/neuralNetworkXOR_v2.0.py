
import numpy as np
from progressbar import ProgressBar
from random import randint

def randomFloat(min_ = -1.0, max_ = 1.0, dec_ = 2):
    rng = float(max_ - min_)
    pct = randint(0, 10**dec_) / float(10**dec_)
    return round(min_ + (rng * pct), dec_)

dataInputs = np.asmatrix([
    (0, 0), 
    (0, 1), 
    (1, 0), 
    (1, 1)
])
dataOutputs = (0, 1, 1, 0)

# print(f" dataInputs: {dataInputs} \ndataOutputs: {dataOutputs}")

layerNeuronCount = (2, 4, 1)
adjustmentRate = 1.0
trainingCount = 1000

class NeuralNetwork:
    def __init__(self):
        
        self.weights = [
            np.random.standard_normal((x, y)) for x, y in zip(layerNeuronCount[:-1], layerNeuronCount[1:])
            # np.ones((x, y)) * layer for layer, x, y in zip(range(len(layerNeuronCount)), layerNeuronCount[:-1], layerNeuronCount[1:])
        ]

        self.biases = [
            randomFloat() for _ in range(len(layerNeuronCount)-1)
            # 1.0 for _ in range(len(layerNeuronCount)-1)
        ]

        # print(f"Weights: {self.weights} \nBiases: {self.biases}")

        self.neuronValues = [
            [-1.0 for _ in range(count)]
            for count in layerNeuronCount[1:]
        ]
        # print(self.neuronValues)
    
    @staticmethod
    def activate(x, type_=""):
        """
        x = numpy matrix
        type_ = "" | "Sigmoid" | "ReLU" | "Leaky" | "tanh" | "SiLU"
        """
        
        if type_ == "":
            return x
        elif type_ == "Sigmoid":
            return 1.0 / (1.0 + np.exp(-x))
        elif type_ == "ReLU":
            return np.maximum(0, x)
        elif type_ == "Leaky":
            return np.where(x < 0.0, x * 0.1, x)
        elif type_ == "tanh":
            return np.tanh(x)
        elif type_ == "SiLU":
            return x / (1.0 + np.exp(-x))
    
    def predict(self, inputs):
        layerNeuronValues = inputs

        self.neuronValues[0] = inputs.tolist()[0]

        # for layer, wMatrix, bMatrix in zip(range(len(layerNeuronCount)-1), self.weights, self.biases):
        for layer, wMatrix, bMatrix in zip(range(len(layerNeuronCount)), self.weights, self.biases):
            # print(f"wM: {wMatrix}, bM: {bMatrix}")
            layerNeuronValues = self.activate(np.matmul(layerNeuronValues, wMatrix) + bMatrix, "Sigmoid")
            # input(layerNeuronValues)
            
            self.neuronValues[layer] = layerNeuronValues.tolist()[0]
            # self.neuronValues[self.weights.index(wMatrix)] = layerNeuronValues.tolist()[0]
        
        # input(self.neuronValues)
        prediction = layerNeuronValues.tolist()[0][0]
        return prediction

        # self.adjustWeights(prediction, expectedOutput)

    def adjustWeights(self, prediction, expectation):
        outputError = expectation - prediction
        # outputError = prediction - expectation

        # print(self.weights)

        layerWeightSums = [
            sum(weight[0] for weight in layerWeights.tolist())
            for layerWeights in self.weights
        ]
        # print(layerWeightSums)

        adjustedWeights = [
            np.asmatrix( self.weights[-1] + ((self.weights[-1] / layerWeightSums[-1]) * outputError * adjustmentRate) )
        ]
        # print(adjustedWeights)

        # finalHiddenLayerErrors = np.subtract(self.weights[-1], adjustedWeights[0])
        finalHiddenLayerErrors = np.subtract(adjustedWeights[0], self.weights[-1])
        # input(finalHiddenLayerErrors)

        self.weights[-1] = adjustedWeights[0]

        self.weights[0] = np.asmatrix(
            self.weights[0] + ((self.weights[0] / layerWeightSums[0]) * finalHiddenLayerErrors * adjustmentRate)
        )

        # input(self.weights)

        # input(
        #     f"Final Weights: {self.weights[-1]} \n" +
        #     f"Final Adjusted: {adjustedWeights} \n" +
        #     f"Final Diff: {diffWeights}"
        # )









n = NeuralNetwork()

pbar = ProgressBar()

print(f"Beginning training ({trainingCount}x)...")
for epoc in pbar(range(trainingCount)):
    
    for i in range(4):
        dataIn = dataInputs[i]
        dataOut= dataOutputs[i]
        prediction = n.predict(dataIn)
        n.adjustWeights(prediction, dataOut)

for i in range(4):
    
    print(
        f"Input: {dataInputs[i].tolist()[0]}, " +
        f"Expectation: {dataOutputs[i]}, " +
        f"Guess: {round(n.predict(dataInputs[i]))}, " +
        ("Correct" if (dataOutputs[i] == round(n.predict(dataInputs[i]))) else "Incorrect")
    )
