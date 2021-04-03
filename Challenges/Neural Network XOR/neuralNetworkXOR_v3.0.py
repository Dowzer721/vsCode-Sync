"""
Although it is not standard practice, I am building this version to have the following shape:

INPUTS      OUTPUTS

    I1----.
           >-.--O1
    I2----'  |
    B--------'

This means that there is no hidden layer, so the connections are as follows:
O1I1
O1I2

Plus the [B]ias:
o1B

            B1-.
    I1---.---.-'-O1
         |   |
    I2---`---'-.-O2
            B2-'

This means that there is no hidden layer, so the connections are as follows:
O1I1
O1I2
O2I1
O2I2

Plus the [B]ias:
O1B
O2B

I am doing this because I don't fully understand the back propogation algorithm. 
I can do it for the final layer -> the one before final, but no more as of yet. 
So by not having a hidden layer, this isn't a concern.

The reason that there are 2 outputs is because I am using the following output rules:
abs(O1) > abs(O2) == Prediction ZERO
abs(O2) > abs(O1) == Prediction ONE
O1 > O2 == Prediction ZERO
O2 > O1 == Prediction ONE

"""

# I am using numpy for matrices. Could do this manually, but this just makes the code cleaner:
import numpy as np

# I am just using this to give the user some feedback of the progress of the NN training:
import progressbar

# Like I said at the top, I am not having a hidden layer, so the shape is just (INPUTS, OUTPUTS):
layerNeuronCount = (2, 2)

# This is the number of times to train the network:
trainingCount = 1000
# The more times you train, theoretically the better it will perform, 
# but it also increases the time taken.

# This just adjusts how aggressive the change is each time the NN adjusts the weights: 
adjustmentMultiplier = 0.1 # 1.0 / float(trainingCount/100) # Set to 1.0 to turn off
# If this wasn't taken into account (or set to 1.0) the NN might overshoot the best 
# solution each time it adjusts the values. 
# The smaller "adjustmentMultiplier" is, the slower the learning will be, 
# but the lower the risk of overshoot.

# The dataset for training the NN:
dataInputs = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1)
]
dataOutputs = [
    (1, 0), # ZERO
    (0, 1), # ONE 
    (0, 1), # ONE
    (1, 0)  # ZERO
]
# print(
#     f"INPUTS: {dataInputs} \n" + 
#     f"OUTPUTS:{dataOutputs}"
# )

# I guess it isn't really needed to have a class here when there is only one NN anyway, 
# but it has just become my way of doing it:
class NeuralNetwork:
    def __init__(self):

        # Setting the initial values of the weights to be random values in the normal distribution:
        self.weights = np.random.standard_normal((layerNeuronCount[-1], layerNeuronCount[0]))
        # self.weights = np.ones((layerNeuronCount[-1], layerNeuronCount[0]))

        # Setting the bias to a matrix, making it easier to work 
        # with in the maths of the "makePrediction" method:
        self.biases = np.random.standard_normal((layerNeuronCount[-1], 1))
        # self.biases = np.zeros((layerNeuronCount[-1], 1))
    
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
            # DESMOS: y=\frac{1}{1+e^{-x}}
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
        
        #
        layerNeuronValues = self.activate(np.matmul(self.weights, inputs) + self.biases, "Aggressive")
        # print(layerNeuronValues)

        prediction = layerNeuronValues[0]

        return prediction

        # print(f"PREDICTION: {prediction}")
    
    def adjustWeights(self, prediction, expectation):
        
        outputError = expectation - prediction
        # outputError = prediction - expectation
        # input(f"pred:{prediction}, exp:{expectation}, err:{outputError}")

        weightSum = np.sum(self.weights) * 0.1
        # input(f"{self.weights}, {weightSum}")

        adjustedWeights = self.weights + ((self.weights / weightSum) * outputError * adjustmentMultiplier)
        # input(f"W:{self.weights}, A:{adjustedWeights}")

        self.weights = adjustedWeights


# Neural Network object initialisation:
NN = NeuralNetwork()

# This is the training of the NN:
pbar = progressbar.ProgressBar()
for epoc in pbar(range(trainingCount)):

    # Each epoc the NN trains on all 4 datasets. 
    # Instead of the for-loop, you can use the following line:
    # i = epoc % 4
    # combinedPrediction = [0.0, 0.0]
    for i in range(4):
        # Tell the NN to make a prediction:
        prediction = NN.makePrediction(dataInputs[i])

        # combinedPrediction += prediction
        
        # Regardless of what the NN predicts, adjust the weights:
        NN.adjustWeights(prediction, dataOutputs[i])
    
    # Once all 4 predictions have been made, adjust the weights according to the sum of predictions:
    # NN.adjustWeights(combinedPrediction, (2, 2))


# Once the training has complete, this just runs the NN 
# and prints out the prediction for each dataset:
for i in range(4):
    prediction = NN.makePrediction(dataInputs[i]).tolist()

    predictedOutput = prediction.index(max(prediction))

    predictionCorrect = "CORRECT" if predictedOutput == dataOutputs[i][1] else "INCORRECT"

    print(
        f"{i}--- IN:{dataInputs[i]}, OUT:{dataOutputs[i][1]}. " +
        f"PREDICTION: " +
        # f"{int(prediction[0] < prediction[1])} ({prediction})"
        f"{predictedOutput} ({prediction}) " +
        f"({predictionCorrect})"
    )