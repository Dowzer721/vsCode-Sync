
# This version I am going to attempt to use matrices, but built myself, 
# instead of using a library such as numpy.
# This is just because I have operations that I want to do to the matrices that I do not know the 
# correct name of, and so cannot find any existing functions to use to perform the operations.

import math
import Matrix
import random

def randomFloat(min_ = -1.0, max_ = 1.0, dec_ = 2):
    """Choose a random floating point number between min_ and max_,
    
    Round said number to dec_ number of places,
    """

    rng = max_ - min_
    pct = random.randint(0, 10 ** dec_) / float(10 ** dec_)
    return round(min_ + (rng * pct), dec_)

# m = Matrix.newMatrix(2, 4)
# n = Matrix.randomSample(2, 4)
# print(m)
# print(n)

layerNeuronCount = [6, 4, 2] # [int(count) for count in input("Enter the counts of neurons per layer, separated by commas: ").split(",")]

weightShapes = [(w,h) for w,h in zip(layerNeuronCount[1:], layerNeuronCount[:-1])]
biasShapes = [(count,1) for count in layerNeuronCount[1:]]

class NeuralNetwork:
    def __init__(self):
        self.weights = [
            Matrix.randomSample(shape[0], shape[1])
            for shape in weightShapes
        ]
        self.biases = [
            Matrix.newMatrix(shape[0], shape[1])
            for shape in biasShapes
        ]
        print(self.weights)
        print(self.biases)
        
NN = NeuralNetwork()
