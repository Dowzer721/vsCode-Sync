"""
THIS IS NOT MY CODE. 
I used OpenAI's GPT-4o to create this. 
I have slightly modified it but it is essentially the AI's code. 

Now that I have this code, I can begin to study it and learn exactly how it works. 
I specified that the code the AI created was as simple as possible and didn't use too many external libraries 
as I felt this would make it harder to understand. Using random and math is okay though as they don't affect my 
learning process. 

I do understand the fundamentals, but I think I ought to sit down and go through this code with a paper and pencil
and go through the mathematics, especially the "delta" and "deactivation function" calculation. 
(Deactivate is derivative of activation function.)
"""


import random
import math

# Activation Function:
def activate(x):
  return 1 / (1 + math.exp(-x))

# Deactivation Function:
def deactivate(x):
  return x * (1 - x)

# Initialise weights with small random values:
def initialiseWeights(inputSize, hiddenSize, outputSize):
  hiddenWeights = [[random.randint(-1000, 1000)/1000. for _ in range(inputSize +1)] for _ in range(hiddenSize)]
  outputWeights = [[random.randint(-1000, 1000)/1000. for _ in range(hiddenSize+1)] for _ in range(outputSize)]
  return hiddenWeights, outputWeights

# Feedforward:
def feedForward(inputs, hiddenWeights, outputWeights):
  # Add bias to inputs
  inputs = inputs + [1]
  
  # Calculate hidden layer activations:
  hiddenInputs = [sum(i * w for i,w in zip(inputs, hiddenWeights[j])) for j in range(len(hiddenWeights))]
  hiddenOutputs= [activate(h) for h in hiddenInputs]
  
  # Add bias to hiiden outputs:
  hiddenOutputs = hiddenOutputs + [1]
  
  # Calculate output layer activations:
  finalInputs = [sum(h*w for h,w in zip(hiddenOutputs, outputWeights[k])) for k in range(len(outputWeights))]
  finalOutputs= [activate(f) for f in finalInputs]
  
  return hiddenOutputs, finalOutputs
  
# Back-propogation step:
def backpropagation(inputs, hiddenOutputs, outputs, targets, hiddenWeights, outputWeights, learningRate):
  
  # Calculate output layer errors and deltas:
  outputErrors = [target - output for target,output in zip(targets, outputs)]
  outputDeltas = [error * deactivate(output) for error, output in zip(outputErrors, outputs)]
  
  # Update output weights:
  for i in range(len(outputWeights)):
    for j in range(len(outputWeights[i])):
      outputWeights[i][j] += learningRate * outputDeltas[i] * hiddenOutputs[j]
  
  # Calculate hidden layer errors and deltas:
  hiddenErrors = [sum(outputDeltas[k] * outputWeights[k][j] for k in range(len(outputWeights))) for j in range(len(hiddenWeights))]
  hiddenDeltas = [error * deactivate(hiddenOutput) for error,hiddenOutput in zip(hiddenErrors[:-1], hiddenOutputs[:-1])]

  # Update hidden weights:
  for i in range(len(hiddenWeights)-1):
    for j in range(len(hiddenWeights[i])-1):
      hiddenWeights[i][j] += learningRate * hiddenDeltas[i] * inputs[j]


# Train the network:
def trainNeuralNetwork(inputs, targets, inputSize, hiddenSize, outputSize, learningRate, epochs):
  hiddenWeights, outputWeights = initialiseWeights(inputSize, hiddenSize, outputSize)
  
  for epoch in range(epochs):
    totalError = 0
    for inputVector, targetVector in zip(inputs, targets):
      # Feedforward:
      hiddenOutputs, outputs = feedForward(inputVector, hiddenWeights, outputWeights)
      
      # Calculate the total error for monitoring:
      totalError += sum(0.5 * (target-output) ** 2 for target, output in zip(targetVector, outputs))

      # Back-propagation:
      backpropagation(inputVector, hiddenOutputs, outputs, targetVector, hiddenWeights, outputWeights, learningRate)

    # Print the error:
    if epoch % 1000 == 0:
      print(f"Epoch {epoch+1}/{epochs}, Error: {totalError:.4f}")
  
  return hiddenWeights, outputWeights

# # Training data: XOR problem
# inputs = [[0,0], [0,1], [1,0], [1,1]]
# targets= [[0],[1],[1],[0]]

# inputSize = 2
# hiddenSize = 8
# outputSize = 1
# learningRate = 0.4
# epochs = 10000

# hiddenWeights, outputWeights = trainNeuralNetwork(inputs, targets, inputSize, hiddenSize, outputSize, learningRate, epochs)

# # Test the trained Network:
# for i,inputVector in enumerate(inputs):
#   _, outputs = feedForward(inputVector, hiddenWeights, outputWeights)
  
#   I = inputVector
#   T = targets[i][0]
#   O = round(outputs[0])
#   R = "Correct" if T == O else "Incorrect"
#   print(f"Input: {I}, Output: {O}, Result: {R}")

# Training data: 
inputs = [[random.randint(-100, 100), random.randint(-100, 100)] for _ in range(50)]
targets= [[int(input_[0] < input_[1])] for input_ in inputs]

inputSize = len(inputs[0])
hiddenSize = 7
outputSize = len(targets[0])
learningRate = 0.4
epochs = 10000

hiddenWeights, outputWeights = trainNeuralNetwork(inputs, targets, inputSize, hiddenSize, outputSize, learningRate, epochs)

# Test the trained Network:
correctCount = 0
for i,inputVector in enumerate(inputs):
  _, outputs = feedForward(inputVector, hiddenWeights, outputWeights)
  
  I = inputVector
  T = targets[i][0]
  O = round(outputs[0])
  R = T == O
  correctCount += int(R)
  print(f"Input: {I}, Output: {O}, Result: {'Correct' if R else 'Incorrect'}")

print(f"Final accuracy: {100*correctCount/len(inputs)}%")
