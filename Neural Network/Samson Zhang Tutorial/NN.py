
from math import exp, tanh
from matplotlib import pyplot as plt
from random import randint

def randomFloat(min_=0.0, max_=1.0, dp_=3):
    rng = max_ - min_
    pct = randint(0, 10**dp_) / float(10**dp_)
    return round(min_ + (rng * pct), dp_)

# Between 0.1 -> 10
graphSlopeMin = 0.1
graphSlopeMax = 10
graphSlope = 1#randomFloat(graphSlopeMin, graphSlopeMax)

layerNodeCount = (2, 3, 1)
numberOfLayers = len(layerNodeCount)
learningRate = 0.1

# activationMode: "relu" / "sigmoid" / "tanh"
activationMode = "sigmoid"

trainDataCount = 1000
trainData = []
for _ in range(trainDataCount):
    # input_ = (randomFloat(), randomFloat())
    input_ = [randomFloat() for _ in range(layerNodeCount[0])]
    output_ = int(input_[1] > (graphSlope * input_[0]))
    
    trainData.append((output_, input_))

def plotTrainingData():
    plotX = [dataItem[1][0] for dataItem in trainData]
    plotY = [dataItem[1][1] for dataItem in trainData]
    plotColour = ['g' if dataItem[0] else 'r' for dataItem in trainData]

    plt.scatter(plotX, plotY, c=plotColour, s=5)
    lineColour = 'k'
    if graphSlope >= 1:
        plt.plot([0, 1/graphSlope], [0, 1], c=lineColour)
    else:
        plt.plot([0, 1], [0, graphSlope], c=lineColour)
    
    plt.title(f"Slope: {graphSlope}")
    plt.show()

def activationFunction(value, derivative=False):
    # https://en.wikipedia.org/wiki/Activation_function#Table_of_activation_functions
    if activationMode == "relu":
        if derivative: return int(value > 0)
        return max(0, value)
    
    if activationMode == "sigmoid":
        try:
            activationValue = 1/(1 + exp(-value))
        except: # pylint: disable=bare-except
            activationValue = 1.0
            #raise Exception(value)

        if derivative: return activationValue * (1 - activationValue)
        return activationValue
    
    if activationMode == "tanh":
        activationValue = tanh(value)
        if derivative: return 1 - (activationValue ** 2)
        return activationValue
    
    raise Exception(f"No valid mode supplied to activation function; ({activationMode}).")
        

def softMax(values):
    valueExponents = [exp(val) for val in values]
    valueExponentsSum = sum(valueExponents)
    return [valueExponents[i] / valueExponentsSum for i in range(len(values))]

def costFunction(valueActual, valuePredicted):
    return (valueActual - valuePredicted) ** 2

class Network:
    def __init__(self, printNetwork=False):
        self.nodes = [] # Node location: [layer][index]
        self.weights = [] # Weight location: [layer][startNodeIndex][endNodeIndex]
        self.biases = [] # Bias location: [layer]
        
        self.costs = [] # Cost location: [layer][index]

        for layer in range(numberOfLayers):
            self.nodes.append( [1 for _ in range(layerNodeCount[layer])] )
            self.costs.append( [0 for _ in range(layerNodeCount[layer])] )

            if layer < numberOfLayers - 1:
                layerWeights = []
                
                # for currentIndex in range(layerNodeCount[layer]):
                for _ in range(layerNodeCount[layer]):
                    currentNodeWeights = []
                    
                    # for nextIndex in range(layerNodeCount[layer+1]):
                    for _ in range(layerNodeCount[layer+1]):

                        # Unsure what is best to set the weights to begin at here:
                        currentNodeWeights.append(randomFloat(-10.0, 10.0))
                        # currentNodeWeights.append((currentIndex * layerNodeCount[layer+1]) + nextIndex)
                    layerWeights.append(currentNodeWeights)
                self.weights.append(layerWeights)

                self.biases.append(0)
            
        if printNetwork:
            print("Neural Network: ")
            print(f"Shape: {layerNodeCount}")
            print(f"Nodes: {self.nodes}")
            print(f"Weights: {self.weights}")
            print(f"Biases: {self.biases}")
            print(f"Costs: {self.costs}")
            print("")


    def makePrediction(self, inputs_):
        self.nodes[0] = inputs_
        for layer in range(1, numberOfLayers):
            for currentNodeIndex in range(layerNodeCount[layer]):
                self.nodes[layer][currentNodeIndex] = 0
                for previousNodeIndex in range(layerNodeCount[layer-1]):
                    connectingWeight = self.weights[layer-1][previousNodeIndex][currentNodeIndex]
                    self.nodes[layer][currentNodeIndex] += (self.nodes[layer-1][previousNodeIndex] * connectingWeight)
                
                self.nodes[layer][currentNodeIndex] += self.biases[layer-1]

                self.nodes[layer][currentNodeIndex] = activationFunction(self.nodes[layer][currentNodeIndex])

        return self.nodes[-1]
    
    def calculateCosts(self, expectedOutputValue):
        # costFunction(valueActual, valuePredicted)

        self.costs[-1][0] = costFunction(self.nodes[-1][0], expectedOutputValue)
        for layer in range(numberOfLayers-2, -1, -1): # 1, 0
            for nodeIndex in range(layerNodeCount[layer]):
                nodeValue = self.nodes[layer][nodeIndex]
                # dC/dw weight->Cost
                # dA/dC Cost->Activation


    
    def backprop(self, expectedOutputValue):
        # Just to see if I am understanding this correctly, I am only going to adjust the weights in the final layer. I will update this in the future to do all layers, but for now it's just the final layer to confirm I understand it all. 
        # Using this: https://dimleve.medium.com/back-propagation-explained-9720c2d4a566#:~:text=5.%20Step%20by%20step%20Back%2Dpropagation%20examples
        
        weightChanges = []
        for layer in range(numberOfLayers-1): # 0, 1
            layerWeightChanges = []
            for startNodeIndex in range(layerNodeCount[layer]):#0,1
                startNodeWeightChanges = []
                for endNodeIndex in range(layerNodeCount[layer+1]):#0,1,2
                    startNodeWeightChanges.append(0)
                layerWeightChanges.append(startNodeWeightChanges)
            weightChanges.append(layerWeightChanges)
        

        layer = -1
        for startNodeIndex in range(layerNodeCount[layer - 1]):
            for endNodeIndex in range(layerNodeCount[layer]):
                # How much did the Activation Function affect the Cost Function?
                dCdA = -costFunction(expectedOutputValue, self.nodes[layer][0]) / self.nodes[layer][endNodeIndex]
                # How much did zeta affect the Activation Function?
                dAdz = self.nodes[layer][endNodeIndex] * (1 - self.nodes[layer][endNodeIndex])
                # How much did the weight affect zeta?
                dzdw = self.nodes[layer-1][startNodeIndex]

                # How much did the weight affect the Cost Function?
                dCdw = dCdA * dAdz * dzdw
                weightChanges[layer][startNodeIndex][endNodeIndex] = dCdw
        
        # Once all weightChanges have been calculated, then update all of the weights.
        layer = -1 #for layer in range(numberOfLayers):
        for startNodeIndex in range(layerNodeCount[layer - 1]):
            for endNodeIndex in range(layerNodeCount[layer]):
                weightValue = self.weights[layer][startNodeIndex][endNodeIndex]
                weightChange = weightChanges[layer][startNodeIndex][endNodeIndex]
                
                self.weights[layer][startNodeIndex][endNodeIndex] = weightValue + (weightChange * learningRate)
        

        # #dC/dw : How much did the weight (w) affect the cost function (C)?
        # for layer in range(numberOfLayers-1, 0, -1): # 2, 1
        #     # Weight location: [layer][startNodeIndex][endNodeIndex]
        #     for startNodeIndex in range(layerNodeCount[layer-1]):
        #         for endNodeIndex in range(layerNodeCount[layer]):
        #             currentWeightValue = self.weights[layer][startNodeIndex][endNodeIndex]
        #             dCdw = 

            


n = Network()

numberOfTrainingEpocs = 20
for _ in range(numberOfTrainingEpocs):
    for (dataOutput, dataInput) in trainData:
        prediction = n.makePrediction(dataInput)
        n.backprop(dataOutput)

dataInput = trainData[randint(0, trainDataCount)][1] # [0.942, 0.951]
dataOutput = int(dataInput[1] > (graphSlope * dataInput[0]))
print(f"Network Input: {dataInput}")
print(f"Correct Output: {dataOutput}")
print(f"Network Output: {round(n.makePrediction(dataInput)[0], 3)}")

# plotTrainingData()

# Perhaps I need to have two outputs ([1 < 0, 0 < 1]), instead of my current setup with just having the output either be 0/1 (TRUE/FALSE). 

