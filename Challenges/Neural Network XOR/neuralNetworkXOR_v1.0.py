
from random import randint

dataInputs = [
    (int(i>=2), int(i%2>0)) 
    for i in range(4)
]

dataOutputs = [
    int(dataInputs[o][0] + dataInputs[o][1] == 1)
    for o in range(4)
]

layerNeuronCount = (2, 2, 1)

weightShapes = [(x, y) for x,y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])]
biasShapes = [(count, 1) for count in layerNeuronCount[1:]]

def randomFloat(min_ = -1.0, max_ = 1.0, dec_ = 2):
    rng = float(max_) - float(min_)
    pct = randint(0, 10 ** dec_) / float(10 ** dec_)
    return round(min_ + (rng * pct), dec_)

class NeuralNetwork:
    def __init__(self):
        self.weights = [
            [
                [0.0 for _ in range(shape[0])]
                for _ in range(shape[1])
            ] for shape in weightShapes
        ]

        self.biases = [
            
        ]

        print(self.weights)

NN = NeuralNetwork()