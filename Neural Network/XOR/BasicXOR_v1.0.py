"""

I didn't even realise, but I am missing a whole layer. That is probably why it hasn't been performing as expected (from on-paper calculations). 
I currently have the two inputs each multiplying with a single weight, then summing to make the output. But instead, 
I need to add a hidden layer into the mix, with the current layout:

i0---.---h0---.
 |   |        |
 '---+---.    |--- O
     |   |    |
i1---'---h1---'
  
I then need to assign the weights of each connection. I think I will start with having separate lists for each layer of weights, to make it 
simpler. Once I have that working though, I probably will be able to condense them down into one nested list, so as to allow for different 
size Networks. 

Note to future me- "Do it on paper/stylus first!"

"""
from random import randint

def randomFloat(min_, max_, dp_=2):
    rng = max_ - min_
    pct = randint(0, 10 ** dp_) / float(10 ** dp_)
    return round(min_ + (rng * pct), dp_)

inputs = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1)
]

# output = inputs[n][0] ^ inputs[n][1]

# NN Shape:
#
# I0 ----w0---.
#              --- O
# I1 ----w1---'

bias = 0.001

weights = [
    randomFloat(0.0, 1.0)
    for _ in range(2)
]
# print(weights)

LearningRate = 0.00125

for trainingEpoc in range(100000):

    for i0, i1 in inputs:
        # if i0+i1 < 2: continue
        # # i0, i1 = inputs[0]
        # iw0 = i0 * weights[0]
        # iw1 = i1 * weights[1]
        # Output = iw0 + iw1 + bias

        # Target = int(i0 ^ i1)

        # Error = abs(Target - Output)

        # AdjustmentMultiplier = Target - (Error / Output)

        # weights[0] = weights[0] * AdjustmentMultiplier * 0.01
        # weights[1] = weights[1] * AdjustmentMultiplier * 0.01

        iw0 = i0 * weights[0]
        iw1 = i1 * weights[1]
        Output = iw0 + iw1 + bias

        Target = int(i0 ^ i1)

        Error = Target - Output

        weights[0] = weights[0] - (LearningRate * (1 - (Error / weights[0])) )
        weights[1] = weights[1] - (LearningRate * (1 - (Error / weights[1])) )

        0

# print(weights)

for i0, i1 in inputs:
    iw0 = i0 * weights[0]
    iw1 = i1 * weights[1]
    Output = iw0 + iw1 + bias

    Target = int(i0 ^ i1)

    print(f"Inputs: {i0}-{i1}, Target: {Target}, Output: {round(Output)} ({Output})")

    0

