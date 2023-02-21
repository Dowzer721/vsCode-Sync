
from math import exp, tanh
import progressbar
from random import randint

dataInputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
dataOutputs = [(i0 ^ i1) for (i0, i1) in dataInputs]

layerNodeCount = (2, 2, 1)
numberOfLayers = len(layerNodeCount)
learningRate = 0.01

# "relu" / "lrelu" / "sigmoid" / "tanh"
activationMode = "sigmoid"
def activate(value, mode = activationMode):
    if mode == "relu":
        return max(0, value)
    
    if mode == "lrelu":
        return (0.01 * value) if value < 0 else value
    
    if mode == "sigmoid":
        return 1.0 / 1.0 + (exp(-value))
    
    if mode == "tanh":
        return tanh(value)
    
    raise Exception(f"mode set to unknown value ({mode}).")

def deactivate(value, mode = activationMode):
    if mode == "relu":
        # f'(x) = {x < 0, x > 0: 0, 1}
        return int(value > 0)
    
    if mode == "lrelu":
        # f'(x) = {x < 0, x > 0: 0.01x, 1}
        return (0.01 * value) if value < 0 else 1
    
    activatedValue = activate(value)

    if mode == "sigmoid":
        # f'(x) = f(x) * (1 - f(x))
        return activatedValue * (1 - activatedValue)
    
    if mode == "tanh":
        # f'(x) = 1 - (f(x)**2)
        return 1 - (activatedValue ** 2)
        
    raise Exception(f"mode set to unknown value ({mode}).")

def costFunction(valueActual, valuePredicted):
    return (valueActual - valuePredicted) ** 2

class NeuralNetwork:
    def __init__(self, showInfo_ = False):
        self.nodes = [] # Node Location: [layer][index]
        self.weights = [] # Weight Location: [layer][startNodeIndex][endNodeIndex]
        self.biases = [] # Bias Location: [layer]

        self.prediction = 0
        self.expectedNodeValues = [] # expectedNodeValues Location: [layer][index]

        for layer in range(numberOfLayers):
            self.nodes.append([0 for _ in range(layerNodeCount[layer])])
            self.expectedNodeValues.append([0 for _ in range(layerNodeCount[layer])])

            if layer < (numberOfLayers-1):
                layerWeights = []

                for _ in range(layerNodeCount[layer]): # startNodeIndex
                    startNodeWeights = []
                    
                    for _ in range(layerNodeCount[layer + 1]): # endNodeIndex
                        startNodeWeights.append(randint(-1000, 1000) / 1000.0)
                    layerWeights.append(startNodeWeights)
                self.weights.append(layerWeights)
                
                self.biases.append(1.5)
        
        if showInfo_:
            print(f"Nodes: {self.nodes}")
            print(f"Weights: {self.weights}")
            print(f"Biases: {self.biases}")
    
    def makePrediction(self, inputs_):

        # Node Location: [layer][index]
        # Weight Location: [layer][startNodeIndex][endNodeIndex]
        # Bias Location: [layer]
        
        self.nodes[0] = inputs_

        for nodeLayer in range(1, numberOfLayers): # 1, 2
            for nodeIndex in range(layerNodeCount[nodeLayer]):
                nodeSumValue = 0
                for previousLayerNodeIndex in range(layerNodeCount[nodeLayer - 1]):
                    nodeSumValue += (self.nodes[nodeLayer - 1][previousLayerNodeIndex] * self.weights[nodeLayer - 1][previousLayerNodeIndex][nodeIndex])
                self.nodes[nodeLayer][nodeIndex] = nodeSumValue + self.biases[nodeLayer - 1]
                self.nodes[nodeLayer][nodeIndex] = activate(self.nodes[nodeLayer][nodeIndex])
        
        self.prediction = self.nodes[-1][0]
        
        # self.nodes[1][0] = (self.nodes[0][0] * self.weights[0][0][0]) + (self.nodes[0][1] * self.weights[0][1][0]) + self.biases[0]
        # self.nodes[1][1] = (self.nodes[0][0] * self.weights[0][0][1]) + (self.nodes[0][1] * self.weights[0][1][1]) + self.biases[0]

        # self.nodes[1][0] = activate(self.nodes[1][0])#, "tanh")
        # self.nodes[1][1] = activate(self.nodes[1][1])#, "tanh")

        # self.nodes[2][0] = (self.nodes[1][0] * self.weights[1][0][0]) + (self.nodes[1][1] * self.weights[1][1][0]) + self.biases[1]
        # self.nodes[2][0] = activate(self.nodes[2][0])

        #return self.nodes[2][0]
        # self.prediction = self.nodes[-1][0]
    
    def backPropogateError(self, expectedOutput):

        # print(f"Prediction:{self.prediction}, Expected:{expectedOutput}, Weights:{self.weights}")

        # Node Location: [layer][index]
        # Weight Location: [layer][startNodeIndex][endNodeIndex]
        # Bias Location: [layer]
        # ExpectedNodeValues Location: [layer][index]

        # L=numberOfLayers
        # Σ(i=0:L){ni*wi} = node
        # nj*wj = (Σ(i=0:j){ni*wi}) + (Σ(i=j+1:L){ni*wi})
        # nj = [ (Σ(i=0:j){ni*wi}) + (Σ(i=j+1:L){ni*wi}) ] / wj

        # Reset the expectedNodeValues all to 0:
        for layer in range(numberOfLayers):
            for nodeIndex in range(layerNodeCount[layer]):
                # expectedNodeValues Location: [layer][index]
                self.expectedNodeValues[layer][nodeIndex] = 0

        self.expectedNodeValues[numberOfLayers - 1][0] = deactivate(expectedOutput)
        for errorLayer in range(numberOfLayers - 1, 0, -1): # 2, 1
            
            numberOfNodesAtErrorLayer = layerNodeCount[errorLayer]
            
            nodeExpectationLayer = errorLayer - 1
            numberOfNodesAt_ExpectationLayer = layerNodeCount[nodeExpectationLayer]
            # print(f"\nnodeExpectationLayer:{nodeExpectationLayer}")

            for endNodeIndex in range(numberOfNodesAtErrorLayer):
                errorAtNode = self.nodes[errorLayer][endNodeIndex] - self.expectedNodeValues[errorLayer][endNodeIndex]
                # print(f"Layer:{errorLayer}, ENI{endNodeIndex}")
                layer_NodeWeight_Sum = deactivate(self.nodes[errorLayer][endNodeIndex])
                for startNodeIndex in range(numberOfNodesAt_ExpectationLayer):
                    
                    nodeAdjustedValue = layer_NodeWeight_Sum - (self.nodes[nodeExpectationLayer][startNodeIndex] * self.weights[nodeExpectationLayer][startNodeIndex][endNodeIndex])# - self.biases[nodeExpectationLayer]
                    if self.weights[nodeExpectationLayer][startNodeIndex][endNodeIndex] != 0:
                        nodeAdjustedValue /= self.weights[nodeExpectationLayer][startNodeIndex][endNodeIndex]
                    self.expectedNodeValues[nodeExpectationLayer][startNodeIndex] += nodeAdjustedValue
                
                    #print(f"Node[{nodeExpectationLayer}][{startNodeIndex}]- Original Value:{self.nodes[nodeExpectationLayer][startNodeIndex]}, New Value:{self.expectedNodeValues[nodeExpectationLayer][startNodeIndex]}")

                    # print(f"Layer:{errorLayer}, ENI{endNodeIndex}, SNI:{startNodeIndex}")
                
                for startNodeIndex in range(numberOfNodesAt_ExpectationLayer):
                    # ExpectedNodeValues Location: [layer][index]
                    self.weights[nodeExpectationLayer][startNodeIndex][endNodeIndex] += (layer_NodeWeight_Sum - (self.expectedNodeValues[nodeExpectationLayer][startNodeIndex] * self.weights[nodeExpectationLayer][startNodeIndex][endNodeIndex]) - self.biases[nodeExpectationLayer]) / self.expectedNodeValues[nodeExpectationLayer][startNodeIndex]

            
        
        
        
        
        
        # cost = costFunction(self.prediction, expectedOutput)
        
        # # How much did the Activation Function affect the Cost Function?
        # dCdA = -cost / self.nodes[-1][0]

        # # How much did zeta affect the Activation Function?
        # dAdz = deactivate(self.prediction)#, "sigmoid")

        # # How much did the weight affect zeta?
        # dzdw0 = self.nodes[-2][0]
        # dzdw1 = self.nodes[-2][1]

        # # How much did the weight affect the Cost Function?
        # dCdw0 = dCdA * dAdz * dzdw0
        # dCdw1 = dCdA * dAdz * dzdw1

        # self.weights[1][0][0] = self.weights[1][0][0] + (dCdw0 * learningRate)
        # self.weights[1][1][0] = self.weights[1][1][0] + (dCdw1 * learningRate)



net = NeuralNetwork()

pbar = progressbar.ProgressBar()
for _ in pbar(range(10000)):
    dataIndex = randint(0, 3)
    input_ = dataInputs[dataIndex]
    output_ = dataOutputs[dataIndex]
    net.makePrediction(input_)
    net.backPropogateError(output_)
    

for i in range(4):
    input_ = dataInputs[i]
    output_ = dataOutputs[i]
    net.makePrediction(input_)
    
    print(f"{i}: {input_} = {output_}: {net.prediction}")
