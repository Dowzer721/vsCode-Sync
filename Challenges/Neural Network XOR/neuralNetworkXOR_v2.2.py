
"""
I had an idea of writing this version with a recursive function for the back propogation, 
but not yet sure how I would approach that. 

Here are some links which have been helpful:
Why are bias nodes used in NNs: https://stats.stackexchange.com/questions/185911/why-are-bias-nodes-used-in-neural-networks
Let's code a NN in plain numpy: https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
Implementation of NN from scratch using numpy: https://www.geeksforgeeks.org/implementation-of-neural-network-from-scratch-using-numpy/
'z' reasoning + some other stuff: https://ml4a.github.io/ml4a/neural_networks/#from-linear-classifiers-to-neurons
"""

import numpy as np

import progressbar
pbar = progressbar.ProgressBar()

dataInputs = [
    np.asarray((0, 0)), 
    np.asarray((0, 1)), 
    np.asarray((1, 0)), 
    np.asarray((1, 1))
]
# dataOutputs = [
#     0,
#     1, 
#     1, 
#     0
# ]

dataOutputs = [
    np.asarray([0]),
    np.asarray([1]),
    np.asarray([1]),
    np.asarray([0])
]

layerNeuronCount = (2, 4, 1) # (2, 4, 8, 16, 32, 64, 128, 64, 32, 16, 8, 4, 2, 1)
trainingCount = 10000
trainingRate = 0.01

# weightShapes = [(x, y) for x, y in zip(layerNeuronCount[:-1], layerNeuronCount[1:])]
weightShapes = [(x, y) for x, y in zip(layerNeuronCount[:-1], layerNeuronCount[1:])]

# biasShapes = [(count, 1) for count in layerNeuronCount[:-1]]

class NeuralNetwork:
    def __init__(self):
        self.weights = [np.random.standard_normal(wShape) for wShape in weightShapes]
        # self.biases  = [np.random.standard_normal(bShape) for bShape in biasShapes]
        self.neuronValues = [
            [0.0 for _ in range(count)]
            for count in layerNeuronCount
        ]

        # print(
        #     f"W: {self.weights} \n" +
        #     f"B: {self.biases} \n" +
        #     f"V: {self.neuronValues} \n"
        # )
    
    @staticmethod
    def activate(x, mode="None"):
        """
        x= numpy matrix

        mode= "None" | "Sigmoid" | "Aggressive" | "ReLU" | "Leaky" | "tanh" | "SiLU"

        If you are unsure of any of the equations, I have provided an equation with 
        each of them with can be typed into the left-side fields at the following website:
        https://www.desmos.com/calculator
        """
        
        if mode == "None":
            return x
        elif mode == "Sigmoid":
            # DESMOS: \frac{1}{1+e^{-x}}
            return 1.0 / (1.0 + np.exp(-x))

        elif mode == "Aggressive":
            # DESMOS: \frac{1}{1+e^{-0.6x}}
            a = 0.6
            return 1.0 / (1.0 + np.exp(a * -x))

        elif mode == "ReLU":
            # DESMOS: \left\{x>0:x,0\right\}
            return np.maximum(0, x)

        elif mode == "Leaky":
            # DESMOS: \left\{x<0:\ x\cdot0.1,\ x\right\}
            return np.where(x < 0.0, x * 0.1, x)

        elif mode == "tanh":
            # DESMOS: \tanh\left(x\right)
            return np.tanh(x)

        elif mode == "SiLU":
            # DESMOS: \frac{x}{1+e^{-x}}
            return x / (1.0 + np.exp(-x))
            
        else:
            raise Exception(f"Unknown input to 'activate' method ({mode})")

    def makePrediction(self, inputs):

        # layerNeuronValues = inputs
        # for wMatrix, bMatrix in zip(self.weights, self.biases):
        #     layerNeuronValues = self.activate(np.matmul(wMatrix, layerNeuronValues) + bMatrix, "Sigmoid")
        
        # # finalWeightsTransposed = np.transpose(self.weights[-1])
        # # layerNeuronValues = self.activate(np.matmul(finalWeightsTransposed, layerNeuronValues), "Sigmoid")

        # # print(layerNeuronValues)

        # def f_forward(x, w1, w2):
        #     # hidden
        #     z1 = x.dot(w1)# input from layer 1 
        #     a1 = sigmoid(z1)# out put of layer 2 
            
        #     # Output layer
        #     z2 = a1.dot(w2)# input of out layer
        #     a2 = sigmoid(z2)# output of out layer
        #     return(a2)

        
        # I don't understand this as of yet; need to refactor it and 
        # that should help me understand better:

        # 'z' just appears to be used in the Neural Networks, without any explanation for this lettering. 
        # It would make sense if it was 's', to correspond with sigmoid, but it is not. 
        # ...
        # Ok so 'z' appears to be the single letter to denote 'weighted-sum + bias',
        # so I am instead going to use a variable with the name 'weightedSumPlusBias',
        # because Neural Networks are difficult enough without confusing variable names:

        weightedSumPlusBias = np.asarray(inputs).dot(self.weights[0])# + self.biases[0]
        activatedValues = self.activate(weightedSumPlusBias, "Sigmoid")
        for w in zip(self.weights[1:]):#, self.biases[1:]):
            # An error pops here and I am not sure why. It references "shapes (2,3) (3,1)".
            # The second pair (3,1) I understand; that is the shape of 'b'.
            # But the first shape (2,3); I do not know what it is refering to.
            # If you run this program and this error pops up, hover your mouse over each of the
            # variables on the following line and you'll see the shape at the bottom of the window
            # does not match (2,3) for any of them. 
            # (2,3) is the shape of the first 
            # print(f"w: {w}, b: {b}")
            #
            # Okay so the tutorial I was following was not actually using the biases, so my inclusion 
            # of them was causing issues. Once I fully understand this code and exactly what is happening 
            # I am sure I will be able to come back and add them in. However, without the biases, 
            # the tutorial ended up getting a working NN, so maybe I won't need them; we shall see.
            
            # weightedSum = activatedValues.dot(w)
            weightedSumPlusBias = activatedValues.dot(w) # + b
            activatedValues = self.activate(weightedSumPlusBias, "Sigmoid")
        
        # z = np.asarray(inputs).dot(self.weights[0])
        # a = self.activate(z, "Sigmoid")
        # for i in range(1, len(layerNeuronCount)-1): # 1
        #     z = a.dot(self.weights[i])
        #     a = self.activate(z, "Sigmoid")

        # This flattens the array, and then converts it into a list:
        activatedValues = np.concatenate(activatedValues).ravel().tolist()
        
        return activatedValues
    
    def backPropogateError(self, layer, error):
        if layer < 0: return

        layerWeightSum = np.sum(self.weights[layer])
        adjustedWeights = (self.weights[layer] / layerWeightSum) * error * trainingRate# * (layer / len(layerNeuronCount))
        self.weights[layer] = adjustedWeights
        
        self.backPropogateError(layer-1, error)

        # print(f"L{layer}: E{error}")
        # self.backPropogateError(layer-1, error)

    # def adjustWeights(self, prediction, expectation):
    #     outputError = expectation - prediction
    #     print(f"ERR:{outputError}")


NN = NeuralNetwork()
for epoc in pbar(range(trainingCount)):
    totalError = 0.0
    for i in range(4):
        prediction = NN.makePrediction(dataInputs[i])
        # Although it appears to be very rare, the predictions do change, 
        # and are not always the same, despite that being extremely common here:
        # print(f"IN:{dataInputs[i]}, OUT:{dataOutputs[i]}, PRED:{int(np.round(prediction, 0))} {np.round(prediction, 3)}")
        # print(f"PREDICTION: {prediction}")
        
        outputError = dataOutputs[i] - prediction

        totalError += np.sum(outputError)

        NN.backPropogateError(len(layerNeuronCount)-2, outputError)

        # print()
    
    # print(f"{epoc}: Total Error: {totalError}")

def absrnd(val, dec=2):
    return round(abs(val), dec)

print(f"Neural Network shape: {layerNeuronCount}")
print(f"Training cycles: {trainingCount}")
for i in range(4):
    
    dataI = dataInputs[i]
    dataO = dataOutputs[i]

    prediction = NN.makePrediction(dataI)

    print(
        f"IN{dataI}, " +
        f"OUT:{dataO}, " +
        f"PREDICTION:{np.round(prediction, 4)[0]}, " +
        f"ERROR:{absrnd((dataO - prediction)[0], 4) }"
    )