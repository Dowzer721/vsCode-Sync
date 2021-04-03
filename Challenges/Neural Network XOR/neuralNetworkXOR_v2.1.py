
import numpy as np
import progressbar
pbar = progressbar.ProgressBar()
from random import randint

def randFloat(min_ = -1.0, max_ = 1.0, dec_ = 2):
    rng = float(max_ - min_)
    pct = randint(0, 10**dec_) / float(10**dec_)
    return round(min_ + (rng * pct), dec_)

dataInputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
dataOutputs = [data[0] ^ data[1] for data in dataInputs]
# print(f"in: {dataInputs}, out: {dataOutputs}")

layerNeuronCount = (2, 4, 1)
class NeuralNetwork:
    def __init__(self):
        self.weights = [
            np.random.standard_normal((x, y)) for x, y in zip(layerNeuronCount[1:], layerNeuronCount[:-1])
        ]

        self.biases = [
            [randFloat() for _ in range(count)]
            for count in layerNeuronCount
        ]

        print(
            f"Weights: {self.weights} \n" +
            f"Biases: {self.biases} \n"
        )

n = NeuralNetwork()