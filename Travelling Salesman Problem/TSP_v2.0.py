
import progressbar
import pygame
from random import randint, sample, seed


from math import pi, cos, sin

# This is the size of the window which is used to render the cities and traversal route.
canvasW, canvasH = (500, 500)

# How many cities to find the shortest distance through.
numberOfCities = 16

# Number of individuals attempting to find a solution.
populationSize = 100 # int(numberOfCities ** 2.2) # int(2 ** numberOfCities) # int(numberOfCities ** 2) # 100 

# Percentage chance of mutation (0 -> 1).
mutationChance = (numberOfCities / 100) #       More cities -> Higher mutation chance.
# mutationChance = 1 / (numberOfCities * 0.6) # More cities -> Lower mutation chance.

# I don't know whether to have a higher or lower chance of mutation for more cities. 
# I've tried both, and I can't tell which is working better.

# Number of times the population evolves.
numberOfEpocs = 1000 # int(populationSize * 12) # int(numberOfCities ** 3.3) # 1000

print(f"N:{numberOfCities}, P:{populationSize}, C:{round(100*mutationChance,1)}%, E:{numberOfEpocs}")

# seed(0)

# This is just for drawing the cities, and for keeping them away from the edges of the render window, can be any integer:
cityDrawingRadius = 16
class City:
    def __init__(self, id_, x_, y_):
        self.id = id_
        self.pos = (x_, y_)

def distanceBetweenCities(A, B):
    dx = A.pos[0] - B.pos[0]
    dy = A.pos[1] - B.pos[1]
    # (n**2 is n-squared), (n**0.5 is square root of n)
    return ((dx**2) + (dy**2)) ** 0.5

# Return a random value between 0.0 -> 1.0:
def randomFloat(decimalPlaces_=2):
    return randint(0, 10 ** decimalPlaces_) / float(10 ** decimalPlaces_)

# Return a random value between min_ -> max_:
# def randomFloat(min_=0.0, max_=1.0, decimalPlaces_=2):
#     rng = max_ - min_
#     pct = randint(0, 10 ** decimalPlaces_) / float(10 ** decimalPlaces_)
#     return round(min_ + (rng * pct), decimalPlaces_)

possibleCities = [
    City(i, randint(cityDrawingRadius, canvasW-cityDrawingRadius), randint(cityDrawingRadius, canvasH-cityDrawingRadius))
    for i in range(numberOfCities)
]

# This is just used for debugging, because there is a known shortest route (around the outside of the shape).
# possibleCities = []
# radius = min(canvasW, canvasH) * 0.45
# for i in range(numberOfCities):
#     angle = (pi * 2 * i) / numberOfCities
#     x = (canvasW / 2) + (cos(angle) * radius)
#     y = (canvasH / 2) + (sin(angle) * radius)
#     newCity = City(i, int(x), int(y))
#     possibleCities.append(newCity)


class GA_Individual:
    # The constructor expects an ID, and can optionally receive the traversal order.
    def __init__(self, id_, traversalOrder_=None):
        self.id = id_

        # If no traversal order has been provided (which is default):
        if traversalOrder_ == None:
            # 'random.sample' takes a sequence, and then the length of the sample to return. 
            # Documentation: https://docs.python.org/3/library/random.html#random.sample
            self.cityTraversalOrder = sample([i for i in range(numberOfCities)], numberOfCities)
        else:
            self.cityTraversalOrder = traversalOrder_
        
        # print(f"C{self.id}: O{self.cityTraversalOrder}")

        self.totalDistance = 0
        self.calculateRouteDistance()
    
    def calculateRouteDistance(self):
        
        # Reset the distance before calculation:
        self.totalDistance = 0

        for c in range(numberOfCities):
            n = (c + 1) % numberOfCities

            currentCity = self.cityTraversalOrder[c]
            nextCity = self.cityTraversalOrder[n]

            dist = distanceBetweenCities(possibleCities[currentCity], possibleCities[nextCity])
            self.totalDistance += dist
        
        # return self.totalDistance
    
    def mutate(self):
        
        if randomFloat() <= mutationChance:

            orderFlipIndexA, orderFlipIndexB = sample([i for i in range(numberOfCities)], 2)
            
            tempCityID_A = self.cityTraversalOrder[orderFlipIndexA]
            self.cityTraversalOrder[orderFlipIndexA] = self.cityTraversalOrder[orderFlipIndexB]
            self.cityTraversalOrder[orderFlipIndexB] = tempCityID_A
            
        


def crossoverTwoIndividuals(parentA, parentB, childID):
    
    # If:
    # The traversal order of parentA looks like this: [0 1 2 3 4 5 6]
    # The traversal order of parentB looks like this: [3 1 4 5 2 6 0]
    # 
    # The way in which this crossover function works is by taking a segment of parentA's order, 
    # then filling in the end with whatever is left in parentB, like this:
    #
    # pA =                      [0 1 2 3 4 5 6]
    # pB =                      [3 1 4 5 2 6 0]
    # segment =                 [- ->- - - -<-]
    # So the segment becomes:   A[2 3 4 5] + B[1 6 0] = [2 3 4 5 1 6 0]
    #
    #
    # Another example, for clarity:
    # pA =                      [2 0 1 6 3 4 5]
    # pB =                      [0 6 1 5 2 4 3]
    # segment =                 [->- -<- - - -]
    # So the segment becomes:   A[0 1] + B[6 5 2 4 3] = [0 1 6 5 2 4 3]
    
    
    childTraversalOrderSectionA = []
    childTraversalOrderSectionB = []

    # 'sorted' returns the provided sequence, in chronological order. 
    # Partnered with 'random.sample', and you get an ordered sequence of two integers, within the range 0 -> numberOfCities.
    sectionStart, sectionEnd = sorted(sample([i for i in range(numberOfCities)], 2))
    
    for i in range(sectionStart, sectionEnd):
        childTraversalOrderSectionA.append(parentA.cityTraversalOrder[i])
    
    childTraversalOrderSectionB = [item for item in parentB.cityTraversalOrder if item not in childTraversalOrderSectionA]

    # Creating the child, and passing in the optional argument of 'traversalOrder_':
    child = GA_Individual(childID, childTraversalOrderSectionA + childTraversalOrderSectionB)
    child.mutate()

    # While adding these comments, I realised I was missing this. 
    # This is important because the Individual has stored it's route distance before the mutation, instead of after it. 
    # This appears to be working much better now.
    child.calculateRouteDistance()

    return child


Population = [GA_Individual(id) for id in range(populationSize)]


minimumTraversalDistance = float("inf")
minimumTraversalDistIndex = 0

# My laptop is slow, so a progress bar is helpful to know how long I have to wait!
pbar = progressbar.ProgressBar() 
for epoc in pbar(range(numberOfEpocs)):

    # Getting the distances of each Individual in the current Population:
    populationTotalDistances = [
        Ind.totalDistance for Ind in Population
    ]

    # A mating pool for the Individuals to produce children for the 'newPopulation':
    matingPool = []
    for Ind in Population:

        # The larger Ind.totalDistance, the fewer times it will be added to the mating pool:
        numberOfMatingPoolPositions = int(max(populationTotalDistances) / Ind.totalDistance)
        # print(f"C{Ind.id} D:{Ind.totalDistance} N:{numberOfMatingPoolPositions}")

        for _ in range( numberOfMatingPoolPositions ):
            matingPool.append(Ind.id)

    
    newPopulation = []
    for newID in range(populationSize):
        
        # Select the two parents from the mating pool:
        parentA_ID, parentB_ID = (0, 0)
        while parentA_ID == parentB_ID:
            parentA_ID = matingPool[randint(0, len(matingPool)-1)]
            parentB_ID = matingPool[randint(0, len(matingPool)-1)]

        parentA = Population[parentA_ID]
        parentB = Population[parentB_ID]
        
        # Create a child from the two parents, and add it to the 'newPopulation':
        newPopulation.append( crossoverTwoIndividuals(parentA, parentB, newID) )
    
    
    # minimumTraversalDistance = float("inf")
    # for newInd in newPopulation:
    #     if newInd.totalDistance < minimumTraversalDistance:
    #         minimumTraversalDistance = newInd.totalDistance
    #         minimumTraversalDistIndex = newInd.id

    
    Population = newPopulation

# Working out with Individual in the evolved Population has the shortest traversal distance:
minimumTraversalDistance = float("inf")
for Ind in Population:
    if Ind.totalDistance < minimumTraversalDistance:
        minimumTraversalDistance = Ind.totalDistance
        minimumTraversalDistIndex = Ind.id
# print(f"After {epoc+1} epocs, minimum traversal distance={round(minimumTraversalDistance)}")



shortestRoute = Population[minimumTraversalDistIndex].cityTraversalOrder    

# Create a window for the cities and route to be drawn onto:
canvas = pygame.display.set_mode((canvasW, canvasH))

while True:

    # Events handling:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_ESCAPE:
                pygame.quit()
                exit(0)


    # Fill the background with white:
    canvas.fill((255, 255, 255))

    for C in possibleCities:
        # Draw a circle at each city location:
        pygame.draw.circle(
            canvas, (150, 150, 150),
            C.pos, cityDrawingRadius, 0
        )
    

    for c in range(numberOfCities):
        n = (c + 1) % numberOfCities

        currentCityPos = possibleCities[shortestRoute[c]].pos
        nextCityPos = possibleCities[shortestRoute[n]].pos

        # Draw a line connecting each city in the traversal order:
        pygame.draw.line(
            canvas, (0, 200, 0),
            currentCityPos, nextCityPos,
            5
        )
    
    # Flip the display, to show the result to the user:
    pygame.display.flip()