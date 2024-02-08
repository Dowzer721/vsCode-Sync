
from math import exp
from random import randint, sample

def rf(min_=-1, max_=1, dp_=3):
    range_ = max_ - min_
    pct_ = randint(0, 1000) / 1000
    return round(min_ + (range_ * pct_), dp_)

act= lambda x: 1 / (1 + exp(-x))


# I DUNNO Y DIS NO WORK

epocCount = 1000
PopulationSize = 100

targetWeight = 0.8
mutationChance = 40
mutationRate = 1

class Network:
    def __init__(self, weight):
        self.weight = weight
        self.error = 0
    
    def guess(self, input_):
        return input_ * self.weight
    
    def mutate(self):
        if randint(0, 100) < mutationChance:
            self.weight += (rf() * mutationRate)

def crossover(weightA, weightB):
    ratioA = rf(min_=0)
    ratioB = 1.0 - ratioA
    # print(f"rA:{ratioA}, rB:{ratioB}")

    return (weightA*ratioA) + (weightB*ratioB)


def orderByError(Nets):
    NetworkCount = len(Nets)
    NetworkIndex = []
    NetworkErrors = [N.error for N in Nets]
    while len(NetworkIndex) < NetworkCount:
        minimumError = min(NetworkErrors)
        minimumErrorIndex = NetworkErrors.index(minimumError)
        NetworkIndex.append(minimumErrorIndex)
        NetworkErrors[minimumErrorIndex] = float("inf")
    return NetworkIndex

dataCount = 20
data = [(i,i+targetWeight) for i in range(1, dataCount+1)]

Population = [Network(rf()) for _ in range(PopulationSize)]
Children = []

for _ in range(epocCount):
    
    for P in Population:
        P.error = 0
        for d in data:
            guess = P.guess(d[0])
            output= d[1]
            P.error += (output - guess)
    
    PopulationIndex_OrderedByError = orderByError(Population)
    
    matingPool = []
    for i,ind in enumerate(PopulationIndex_OrderedByError):
        matingPool.extend([ind for _ in range((PopulationSize-i))])
    # input(matingPool)
    # matingPoolSize = len(matingPool)-1

    Children = []
    for _ in range(PopulationSize):
        parentAIndex = sample(matingPool, 1)[0]
        parentBIndex = sample(matingPool, 1)[0]
        while parentAIndex == parentBIndex:
            parentBIndex = sample(matingPool, 1)[0]
        
        parentAWeight = Population[parentAIndex].weight
        parentBWeight = Population[parentBIndex].weight
        childWeight = crossover(parentAWeight, parentBWeight)
        child = Network(childWeight)
        child.mutate()
        Children.append(child)
    
    Population = [C for C in Children]

ChildrenIndex_OrderedByError = orderByError(Population)
smallestErrorIndividual = Population[ChildrenIndex_OrderedByError[0]]
print(f"{smallestErrorIndividual.error} : {smallestErrorIndividual.weight}")