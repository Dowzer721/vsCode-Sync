
from random import randint

networkShape = (6, 4, 2)
# networkShape = (1, 1, 1)

"""
With networkShape as (1, 1, 1), the network will look like this:

INPUT LAYER         HIDDEN LAYER        OUTPUT LAYER
     O--------w0---------O---------w1---------O
              B0---------^         B1---------^   


With networkShape as (1, 1, 2), the network will look like this:

"""

networkLayers = [
    [randint(0, 1) for _ in range(networkShape[0])] # Input layer
]

networkLayers.append( [
    [0 for _ in range(networkShape[i])]
    for i in range(1, len(networkShape)-1)
] )

networkLayers.append( [0 for _ in range(networkShape[-1])] ) # Output layer

# print(networkLayers)
# print(f"inputNeurons:  {networkLayers[0]}")
# print(f"hiddenLayers: {networkLayers[1:-1]}")
# print(f"outputNeurons: {networkLayers[-1]}")

networkWeights = [
    [randint(0, 1000) / 1000.0 for _ in range(networkShape[L] * networkShape[L+1])]
    for L in range(0, len(networkShape)-1)
]

print(networkShape)
print(networkWeights)