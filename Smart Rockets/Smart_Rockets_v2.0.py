
import math
import pygame
import random

screenW = 700
screenH = 500
maxDist = math.sqrt((screenW**2) + (screenH**2))
screen = pygame.display.set_mode((screenW, screenH))

populationSize = 50

rocketThrusterCount = 16
rocketRadius = 20
globalDrag = 0.9

mutationChance = 1. / rocketThrusterCount
mutationStep = 1 # int(rocketThrusterCount/2)

def randomFloat(min_=0.0, max_=1.0, dec_=2):
    rng = float(max_ - min_)
    pct = random.randint(0, 10 ** dec_) / float(10 ** dec_)

    return min_ + (rng * pct)

def isInt(val):
    return val == int(val)

def drawArrow(start, angle, length, colour=(0, 0, 0), thickness=1):
    x1 = int(start.x)
    y1 = int(start.y)
    x2 = int(x1 + (math.cos(angle) * length))
    y2 = int(y1 + (math.sin(angle) * length))
    pygame.draw.line(
        screen, colour,
        (x1, y1),
        (x2, y2),
        thickness
    )
    
    hLx = int(x2 + (math.cos(angle - (math.pi * 0.85)) * (length * 0.35)))
    hLy = int(y2 + (math.sin(angle - (math.pi * 0.85)) * (length * 0.35)))
    pygame.draw.line(
        screen, colour,
        (x2, y2),
        (hLx, hLy),
        thickness
    )

    hRx = int(x2 + (math.cos(angle + (math.pi * 0.85)) * (length * 0.35)))
    hRy = int(y2 + (math.sin(angle + (math.pi * 0.85)) * (length * 0.35)))
    pygame.draw.line(
        screen, colour,
        (x2, y2),
        (hRx, hRy),
        thickness
    )

class Vector:
    def __init__(self, x_=0.0, y_=0.0):
        self.x = x_
        self.y = y_
        # print(f"x:{self.x}, y:{self.y}")
    
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
    
    def sub(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    def mult(self, val):
        self.x *= val
        self.y *= val
    
    def div(self, val):
        self.x /= val
        self.y /= val
    
    def heading(self):
        # return math.atan2(self.x, self.y) - (math.pi / 2.0)
        return math.atan2(self.y, self.x)

    def copy(self):
        return Vector(self.x, self.y)
    
    @staticmethod
    def fromAngle(angle):
        return Vector(math.cos(angle), math.sin(angle))

targetX = int(screenW * randomFloat(0.3, 0.5) )
targetY = int(screenH * randomFloat(0.1, 0.3) )
targetRadius = int(rocketRadius * 0.5)

rocketStartX = screenW / randomFloat(2.0, 1.8)
rocketStartY = screenH - (rocketRadius * randomFloat(2.5, 3.0))

dx = ((targetX-rocketStartX) **2)
dy = ((targetY-rocketStartY) **2)
numberOfThrusts = int(math.sqrt(dx + dy) * 1.25)
# print(numberOfThrusts)
class Rocket:
    def __init__(self, id_, thrusters_=-1, thrustAmount_=-1):
        self.id = id_

        self.pos = Vector(rocketStartX, rocketStartY)
        self.vel = Vector()
        self.acc = Vector()

        if thrusters_==-1:
            self.thrusters = [random.randint(0, rocketThrusterCount) for _ in range(numberOfThrusts)]
        else:
            self.thrusters = thrusters_
        

        self.thrustAmount = randomFloat(0.01, 0.1) if (thrustAmount_ == -1) else thrustAmount_
        
        self.health = len(self.thrusters)
        
        self.dead = False
        self.hitWall = False
        self.hitTarget = False
        self.ranOutOfHealth = False
        self.healthAtDeath = 0
        self.fitness = 0.0
        
    def update(self, thrust_=True, move_=True, checkCollisions_=True, kill_=True, render_=True):
        if (self.dead == False):
            self.thrust()
            self.move()
            self.checkCollisions()
            self.health = max(0, self.health - 1)
            if self.health == 0:
                self.ranOutOfHealth = True
                self.kill()
            
            if render_:
                self.render()
        else:
            if render_:
                self.render((255, 0, 0), 2)
    
    def thrust(self):
        thruster = self.thrusters[numberOfThrusts - self.health]
        thrustAngle = ((math.pi * 2. / rocketThrusterCount) * thruster) # + self.vel.heading()

        thrustVector = Vector.fromAngle(thrustAngle)
        thrustVector.mult(self.thrustAmount)
        self.acc.sub(thrustVector)
    
    def move(self):
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        
        self.vel.mult(globalDrag)
        self.acc.mult(0.0)
    
    def checkCollisions(self):
        if (
            (self.pos.x <= rocketRadius) or
            (self.pos.y <= rocketRadius) or 
            (self.pos.x >= screenW - rocketRadius) or 
            (self.pos.y >= screenH - rocketRadius)
        ): 
            self.hitWall = True
            self.kill()
            return True
        return False
    
    def checkTargetHit(self):
        targetDx = self.pos.x - targetX
        targetDy = self.pos.y - targetY
        dist = math.sqrt((targetDx**2) + (targetDy**2))
        if (dist <= rocketRadius + targetRadius):
            self.hitTarget = True
    
    def kill(self):
        self.healthAtDeath = self.health
        self.dead = True
    
    def render(self, colour=(0, 0, 0), thickness=1):
        posX = self.pos.x
        posY = self.pos.y
        pygame.draw.circle(
            screen, colour,
            (int(posX), int(posY)),
            rocketRadius, thickness
        )
        if self.dead:
            return

        drawArrow(self.pos, self.vel.heading(), rocketRadius * 2)
        
        # for i in range(rocketThrusterCount):
        #     theta = (math.pi * 2.0 / rocketThrusterCount) * i
            
        #     thrusterColour = (255, 0, 0) if (self.thrusters[numberOfThrusts - self.health] == i) else (0, 0, 0)
            
        #     drawArrow(self.pos, theta, rocketRadius * 0.9, thrusterColour, thickness)
    
    def calculateFitness(self):
        
        # if self.hitWall:
        #     self.fitness = 0
        #     return
        
        # if self.hitTarget:
        #     self.fitness = int(maxDist)
        #     return
        
        targetDx = self.pos.x - targetX
        targetDy = self.pos.y - targetY
        dist = math.sqrt((targetDx**2) + (targetDy**2))

        # if self.ranOutOfHealth:
        self.fitness = int(maxDist / dist) + self.healthAtDeath
        self.fitness = int(maxDist - dist) + self.healthAtDeath
        return

        # print("NO FITNESS IF FIRED")

    def mutate(self):
        self.thrustAmount += randomFloat(-0.01, 0.01)
        for thruster in range(numberOfThrusts):
            if randomFloat() <= mutationChance:
                self.thrusters[thruster] = (self.thrusters[thruster] + random.randint(0, rocketThrusterCount-1)) % rocketThrusterCount
                # self.thrusters[thruster] = (self.thrusters[thruster] + rocketThrusterCount + random.randint(-mutationStep, mutationStep)) % rocketThrusterCount
                


def crossover(rocketA, rocketB, newID):
    # crossoverPoint = random.randint(0, numberOfThrusts-1)
    # childThrusters = (rocketA.thrusters[:crossoverPoint] + rocketB.thrusters[crossoverPoint:])

    childThrusters = []
    for thr in range(numberOfThrusts):
        rAThr = rocketA.thrusters[thr]
        rBThr = rocketB.thrusters[thr]
        childThr = (rAThr + rBThr) / 2.0
        if not isInt(childThr):
            childThr += ((random.randint(0, 1) * 2) - 1) * 0.5
        
        childThrusters.append(int(childThr))
    
    childThrustAmount = (rocketA.thrustAmount + rocketB.thrustAmount) / 2.0

    child = Rocket(newID, childThrusters, childThrustAmount)

    child.mutate()
    return child

Population = [Rocket(i) for i in range(populationSize)]

closestIndividual = 0
# frameCount = 0
while(True):
    # screen.fill((255, 255, 255))
    
    avgPosition = Vector()
    avgDirection = Vector()
    numberOfDeadRockets = sum([int(rocket.dead) for rocket in Population])
    # print(numberOfDeadRockets)
    while (numberOfDeadRockets < populationSize):
        screen.fill((255, 255, 255))

        numberOfDeadRockets = sum([int(rocket.dead) for rocket in Population])
        for rocket in Population:
            rocketRender = True # bool(rocket.id == closestIndividual)
            rocket.update(render_=rocketRender)

            avgPosition.add(rocket.pos)
            avgDirection.add(rocket.vel)
        
        avgPosition.div(populationSize)
        avgDirection.div(populationSize)
        drawArrow(
            avgPosition,
            avgDirection.heading(),
            maxDist * 0.1,
            (0, 0, 200), 2
        )
        
        pygame.draw.circle(
            screen, (0, 200, 0),
            (targetX, targetY),
            int(rocketRadius * 0.8),
            int(rocketRadius * 0.4)
        )

        pygame.display.flip()
    
    # All rockets dead
    # print("All rockets dead, creating new Population")

    lowestDistance = math.inf
    matingPool = []
    for r in range(populationSize):

        dx = Population[r].pos.x - targetX
        dy = Population[r].pos.y - targetY
        dist = math.sqrt((dx**2) + (dy**2))
        if dist < lowestDistance:
            lowestDistance = dist
            closestIndividual = r

        Population[r].calculateFitness()
        for _ in range(Population[r].fitness):
            matingPool.append(r)
    
    print(lowestDistance)
    
    newPopulation = []
    for i in range(populationSize):
        parentA = Population[matingPool[random.randint(0, len(matingPool)-1)]]
        parentB = Population[matingPool[random.randint(0, len(matingPool)-1)]]
        child = crossover(parentA, parentB, i)
        newPopulation.append(child)
    
    Population = newPopulation

    # pygame.draw.circle(
    #     screen, (0, 200, 0),
    #     (targetX, targetY),
    #     targetRadius,
    #     int(targetRadius/2)
    # )

    # pygame.display.flip()

    

    # frameCount += 1