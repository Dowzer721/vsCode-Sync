
from math import exp, log

from random import randint, seed
def rf(min_=0., max_=1., dp_=2):
    rng = max_ - min_
    pct = randint(0, 10 ** dp_) / float(10 ** dp_)
    return round(min_ + (rng * pct), dp_)

# seed(0)

netShape = (2, 4, 1) # (2, 3, 4, 2)



# Refer to a specific weight by [layer][startNode][endNode]
weights = []
def setRandomWeights():
    for layer in range(len(netShape) - 1):
        # 0 1
        layerWeights = []

        currNodeCount = netShape[layer]
        nextNodeCount = netShape[layer + 1]

        for _ in range(currNodeCount):
            nodeWeights = []
            for _ in range(nextNodeCount):
                # nodeWeights.append(f"{c}:{n}")

                # Weights should be started in the range:
                # -1/root(d) -> 1/root(d),
                # where d is the number of inputs to a given neuron
                rootD = nextNodeCount ** 0.5
                randomMin = -1.0 / rootD
                randomMax =  1.0 / rootD

                nodeWeights.append(rf(randomMin, randomMax, 3) )
            layerWeights.append(nodeWeights)
        
        weights.append(layerWeights)
    # print(weights)
setRandomWeights()

def activation(x_):
    # https://en.wikipedia.org/wiki/Activation_function#Table_of_activation_functions

    # Sigmoid:
    return 1.0 / (1.0 + exp(-x_))

    # Gaussian:
    # return exp(-(x_ ** 2))

def inverseActivation(x_):

    # Inverse Sigmoid:
    return -log((1/x_) - 1)

def guess(inputIndex):

    inputs = [
        int(inputIndex > 1),
        int(inputIndex % 2)
    ]
    # print(f"{inputs}")

    nodeValues = [inputs] + [[0 for _ in range(nodeCount)] for nodeCount in netShape[1:]]
    # print("nodeValues: ", nodeValues)
    

    # Refer to a specific node by [layer][index]
    # Refer to a specific weight by [layer][startNode][endNode]
    
    for layer in range(1, len(netShape)):  # 1 2
        
        nodeCountAtPreviousLayer = netShape[layer - 1] # 2 3
        nodeCountAtLayer = netShape[layer] # 3 4
        
        # print(f"layer:{layer}, nodeCount(-1, 0):({nodeCountAtPreviousLayer}, {nodeCountAtLayer})")

        for currentLayerNodeIndex in range(nodeCountAtLayer):
            # print(nodeIndex)

            nodeValues[layer][currentLayerNodeIndex] = 0.0
            
            for previousLayerNodeIndex in range(nodeCountAtPreviousLayer):

                previousNodeValue = nodeValues[layer - 1][previousLayerNodeIndex]
                connectingWeight = weights[layer - 1][previousLayerNodeIndex][currentLayerNodeIndex]

                nodeValues[layer][currentLayerNodeIndex] += (previousNodeValue * connectingWeight)
            
            nodeValues[layer][currentLayerNodeIndex] = activation(nodeValues[layer][currentLayerNodeIndex])
            
            # FIXME
            # Rounding the node value just for debugging; REMOVE BEFORE TESTING.
            # nodeValues[layer][currentLayerNodeIndex] = round(nodeValues[layer][currentLayerNodeIndex], 1)
    
    # print("nodeValues: ", nodeValues)

    networkGuess = nodeValues[-1][0]
    correctAnswer = float(inputs[0] ^ inputs[1])
    # print(f"Inputs: {inputs}, Guess: {networkGuess}, Answer: {correctAnswer}")
    return networkGuess, correctAnswer, nodeValues

def backProp(networkGuess_, correctAnswer_, nodeValues_, learningRate_=0.01):

    # startingError = correctAnswer_ - networkGuess_
    # print(startingError)

    previous_dadw_dCda = 1

    # for layer in range(len(netShape) - 2, 0, -1): # 1
    for layer in range(len(netShape) - 2, -1, -1): # 1 0
        # print(layer)
        # weightLayer = layer - 1

        # currentNodeValuesAtLayer = nodeValues_[layer]
        # print(f"Layer: {layer}, NodeValues: {currentNodeValuesAtLayer}")

        # https://www.youtube.com/watch?v=CoPl2xn2nmk

        numberOfNodesAtPrevLayer = netShape[layer]
        numberOfNodesAtCurrLayer = netShape[layer + 1]

        for endNodeIndex in range(numberOfNodesAtCurrLayer):
            for startNodeIndex in range(numberOfNodesAtPrevLayer):

                # Using the letters denoted in the above YouTube video:

                # Refer to a specific node by [layer][index]
                i = nodeValues_[layer][startNodeIndex]

                # Refer to a specific weight by [layer][startNode][endNode]
                w = weights[layer][startNodeIndex][endNodeIndex]

                # Activation function:
                a = activation(i * w)

                # Desired output:
                if layer == len(netShape) - 2:
                    t = correctAnswer_
                else:
                    t = inverseActivation(a) / weights[layer+1][endNodeIndex][0]
                
                # Cost function:
                # C = (a - t) ** 2

                # Rate of change of a[ctivation function] with respect to w (derivative of activation function):
                # This is a correction found in the comments of the video (Laurie Linnett):
                dadw = i * a * (1 - a)
                
                # Rate of change of C[ost] with respect to a[ctivation] (derivative of Cost function):
                dCda = 2 * (a - t)

                # New value of w:
                wDash = w - (learningRate_ * previous_dadw_dCda * dadw * dCda)

                # TODO: This doesn't want to be here, because it wants to be stored before moving to next layer. 
                # But it is going to only store values which are in relation to the last changed weight, which I don't believe is correct. 
                # It works in the video because he only has a network of shape (1, 1, 1), so there is only one weight connecting the layers, but I 
                # don't think this would work when the shape is different, and therefore there is a different number of weights connecting the layers. 
                
                # Store this rate of change for next layer:
                previous_dadw_dCda = dadw * dCda

                # Setting new value of w:
                weights[layer][startNodeIndex][endNodeIndex] = wDash
        
        # previous_dadw_dCda = dadw * dCda
        
        # numberOfNodesAtLayer = netShape[layer]
        # for n in range(numberOfNodesAtLayer):
        #     # C = 0
        #     # if layer == len(netShape) - 1:
        #     #     # Cost function:
        #     #     C = (activation(nodeValues_[layer][n]) - correctAnswer_) ** 2
        #     # else:
        #     #     #
        #     #     pass

        #     # Cost function:
        #     C = nodeValues_[layer][n] - 0
        #     # print(C)

        #     # i, w, a, r, t
        #     # i = nodeValues_[layer - 1]
        
        # # Cost function:
        # # print(C)

    


# for _ in range(16):
#     print("---")
#     for i in range(4):
#         g, a = guess(i)
#         print(f"Guess: {round(g,1)}, Answer: {a}")

#         backProp(g, a)

# for _ in range(10000):
#     g, a, v = guess(2)
#     backProp(g, a, v)

# n = 2
# g, a, v = guess(n)

# print(f"Inputs: {[int(n > 1),int(n % 2)]}, Guess: {g}, Answer: {a}")

trainingCycleCount = 1000

for epoc in range(trainingCycleCount):

    for i in range(4):

        # _guess, _answer, _nodeValues = guess(i)

        # backProp(_guess, _answer, _nodeValues)

        backProp( *guess(i) )

for i in range(4):
    g, a, _ = guess(i)
    print(f"Inputs: {[int(i > 1),int(i % 2)]}, Guess: {round(g, 0)}, Answer: {a}")
