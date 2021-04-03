
import math
import pygame
import random

screenW = 700
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

maxDist = math.sqrt((screenW**2) + (screenH**2))
globalDrag = 0.99

rocketCount = 500
rocketThrusterCount = 7
rocketRadius = 20
rocketStartX = int(screenW * 0.5)
rocketStartY = int(screenH - (rocketRadius*1.1))

mutationChance = 0.05
mutationStep = int(rocketThrusterCount / 4)

targetRadius = int(rocketRadius * 0.8)
randX = random.randint(int(screenW*0.2), int(screenW*0.5))
randY = random.randint(int(screenH*0.1), int(screenH*0.3))
targetX = min(max(randX, targetRadius), screenW-targetRadius)
targetY = min(max(randY, targetRadius), screenH-targetRadius)

targetStartDx = targetX - rocketStartX
targetStartDy = targetY - rocketStartY
distFromStartToTarget = math.sqrt((targetStartDx**2) + (targetStartDy**2))

numberOfRocketThrusts = int(distFromStartToTarget * 2.5)

def drawTarget():
    pygame.draw.circle(
        screen, (200, 0, 0),
        (targetX, targetY),
        targetRadius, 0
    )
    pygame.draw.circle(
        screen, (200, 200, 200),
        (targetX, targetY),
        int(targetRadius/1.25), 0
    )
    pygame.draw.circle(
        screen, (200, 0, 0),
        (targetX, targetY),
        int(targetRadius/1.75), 0
    )
    pygame.draw.circle(
        screen, (200, 200, 200),
        (targetX, targetY),
        int(targetRadius/2.75), 0
    )
    pygame.draw.circle(
        screen, (200, 0, 0),
        (targetX, targetY),
        int(targetRadius/5.5), 0
    )

minDistToTargetOverall = math.inf
minDistToTarget = math.inf
def drawMinCircles():
    pygame.draw.circle(
        screen, (150, 0, 0),
        (targetX, targetY),
        int(minDistToTargetOverall), 1
    )

    pygame.draw.circle(
        screen, (200, 0, 0),
        (targetX, targetY),
        int(minDistToTarget), 2
    )

def randomFloat(min_=0.0, max_=1.0, dec_=2):
    rng = max_ - min_
    pct = random.randint(0, 10**dec_) / float(10 ** dec_)
    return min_ + (rng * pct)

class Vector:
    def __init__(self, x_=0.0, y_=0.0):
        self.x = x_
        self.y = y_
    
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
        return math.atan2(self.y, self.x)
    
    @staticmethod
    def fromAngle(angle):
        return Vector(math.cos(angle), math.sin(angle))
    
    @staticmethod
    def random():
        angle = randomFloat(0.0, math.pi * 2.0)
        return Vector.fromAngle(angle)

class Rocket:
    def __init__(self, id_):
        self.id = id_

        self.pos = Vector(rocketStartX, rocketStartY)
        self.vel = Vector()
        self.acc = Vector()

        self.thrusters = [random.randint(0, rocketThrusterCount-1) for _ in range(numberOfRocketThrusts)]
        self.thrustAmount = 0.1 # randomFloat(0.01, 0.1)

        self.health = numberOfRocketThrusts
        
        self.dead = False
        self.healthAtDeath = numberOfRocketThrusts
        self.hitTarget = False
        self.hitWall = False

        self.currentDistanceToTarget = math.inf
        self.minimumDistanceToTarget = math.inf

        self.fitness = 0.0
    
    def thrust(self):
        thrustNumber = self.thrusters[numberOfRocketThrusts - self.health]
        thrustDirection = (math.pi * 2.0 / rocketThrusterCount) * thrustNumber
        thrustVector = Vector.fromAngle(thrustDirection + math.pi)
        thrustVector.mult(self.thrustAmount)

        self.acc.add(thrustVector)

    def move(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)

        self.vel.mult(globalDrag)
        self.acc.mult(0.0)
    
    def calculateDistanceToTarget(self):
        targetDx = self.pos.x - targetX
        targetDy = self.pos.y - targetY
        self.currentDistanceToTarget = math.sqrt((targetDx**2) + (targetDy**2))
        self.minimumDistanceToTarget = min(self.currentDistanceToTarget, self.minimumDistanceToTarget)

    def render(self, colour=(200, 200, 200), thickness=1):
        posX = int(self.pos.x)
        posY = int(self.pos.y)
        pygame.draw.circle(
            screen, colour,
            (posX, posY),
            rocketRadius, 
            thickness
        )

        heading = self.vel.heading()
        headingX = int(self.pos.x + (math.cos(heading) * rocketRadius) )
        headingY = int(self.pos.y + (math.sin(heading) * rocketRadius) )
        pygame.draw.line(
            screen, colour,
            (posX, posY),
            (headingX, headingY),
            thickness
        )

        if self.dead == False:
            for i in range(rocketThrusterCount):
                if (self.thrusters[numberOfRocketThrusts - self.health] == i):
                    angle = (math.pi * 2.0 / rocketThrusterCount) * i
                    thrusterX = int(self.pos.x + (math.cos(angle) * rocketRadius * 0.75))
                    thrusterY = int(self.pos.y + (math.sin(angle) * rocketRadius * 0.75))
                    pygame.draw.line(
                        screen, (150, 0, 0),
                        (posX, posY),
                        (thrusterX, thrusterY),
                        thickness
                    )
    
    def ranOutOfHealth(self):
        self.dead = True
        self.healthAtDeath = self.health
    
    def hitTargetMethod(self):
        self.hitTarget = True
        self.healthAtDeath = self.health
        self.dead = True
    
    def checkWallCollisions(self):
        if (
            (self.pos.x < rocketRadius) or 
            (self.pos.y < rocketRadius) or
            (self.pos.x > screenW - rocketRadius) or
            (self.pos.y > screenH - rocketRadius) ):
            self.hitWall = True
            self.dead = True
            self.healthAtDeath = self.health
    
    def checkTargetCollision(self):
        targetSelfDx = targetX - self.pos.x
        targetSelfDy = targetY - self.pos.y
        distanceToTarget = math.sqrt((targetSelfDx**2) + (targetSelfDy**2))
        if distanceToTarget < (rocketRadius + targetRadius):
            self.hitTargetMethod()
    
    def calculateFitness(self):
        
        if self.hitWall:
            self.fitness = 0
        else:

            totalDistanceTravelled = (numberOfRocketThrusts - self.health)

            if self.hitTarget:
                # self.fitness = int(math.pow(maxDist / self.healthAtDeath, 2.0) )
                self.fitness = int(math.pow((self.healthAtDeath+1), 2.0) )
            else:
                # self.fitness = int(maxDist - self.minimumDistanceToTarget)
                # self.fitness = int(math.pow(self.currentDistanceToTarget / (self.healthAtDeath+1), 0.5) )

        # if self.hitTarget:
        #     self.fitness = int(numberOfRocketThrusts)
        # else:
        #     if self.hitWall:
        #         self.fitness = 0
        #     else:
        #         self.fitness = int(numberOfRocketThrusts / (self.healthAtDeath+1))

    def mutate(self):
        for thr in range(rocketThrusterCount):
            if randomFloat() <= mutationChance:
                thruster = self.thrusters[thr]
                # self.thrusters[thr] = (self.thrusters[thr] + rocketThrusterCount + (((random.randint(0, 1) * 2) - 1) * int(rocketThrusterCount / 2)) ) % rocketThrusterCount
                # self.thrusters[thr] = (thruster + rocketThrusterCount + int(randomFloat(-0.5, 0.5) * rocketThrusterCount)) % rocketThrusterCount
                self.thrusters[thr] = (thruster + rocketThrusterCount + random.randint(-mutationStep, mutationStep)) % rocketThrusterCount
                
    
    def update(self):
        if self.dead == False:
            self.health = max(0, self.health - 1)
            if self.health == 0:
                self.ranOutOfHealth()
                return
            
            self.checkWallCollisions()
            self.checkTargetCollision()

            self.thrust()
            self.move()
            self.calculateDistanceToTarget()
            self.render()
        else:
            if self.hitTarget:
                self.render((0, 200, 0), 2)
            else:
                self.render((255, 100, 100), 2)
rockets = [Rocket(i) for i in range(rocketCount)]


def crossover(rocketA, rocketB, newID):

    childThrusters = []
    for thr in range(numberOfRocketThrusts):
        rAThr = rocketA.thrusters[thr]
        rBThr = rocketB.thrusters[thr]
        chThr = (rAThr + rBThr) / 2.0
        if (chThr - int(chThr) > 0.0):
            chThr += ((random.randint(0, 1) * 2) - 1) * 0.5
        childThrusters.append(int(chThr))

    # crossoverPoint = random.randint(0, rocketThrusterCount-1)
    # childThrusters = (rocketA.thrusters[:crossoverPoint] + rocketB.thrusters[crossoverPoint:])
    
    childRocket = Rocket(newID)
    childRocket.thrusters = childThrusters
    childRocket.mutate()

    return childRocket

while(True):

    # frameCount = 0
    numberOfDeadRockets = 0
    while(numberOfDeadRockets < rocketCount):
        screen.fill((50, 50, 100))

        drawTarget()

        minDistToTarget = math.inf
        for rocket in rockets:
            rocket.update()
            minDistToTarget = min(rocket.currentDistanceToTarget, minDistToTarget)

        minDistToTargetOverall = min(minDistToTarget, minDistToTargetOverall)
        
        drawMinCircles()

        
        pygame.display.flip()
        # frameCount += 1
        numberOfDeadRockets = sum([int(rocket.dead) for rocket in rockets])
        numberOfTargetRockets = sum([int(rocket.hitTarget) for rocket in rockets])
    print(f"Number of rockets which hit the target: {numberOfTargetRockets}")

    
    screen.fill((50, 50, 100))
    drawTarget()
    for rocket in rockets:
        rocket.render((255, 100, 100), 2)
    drawMinCircles()
    pygame.display.flip()
    
    # At this line, all rockets are dead

    matingPool = []
    for rocket in rockets:
        rocket.calculateFitness()
        if rocket.hitTarget:
            print(rocket.fitness)
        for _ in range(rocket.fitness):
            matingPool.append(rocket.id)
    # print(f"matingPool length: {len(matingPool)}")
    if len(matingPool) < rocketCount:
        for _ in range(len(matingPool), rocketCount):
            matingPool.append(random.randint(0, rocketCount-1))
    
    newPopulation = []
    for i in range(rocketCount):
        parentA = rockets[matingPool[random.randint(0, len(matingPool)-1)]]
        parentB = rockets[matingPool[random.randint(0, len(matingPool)-1)]]
        child = crossover(parentA, parentB, i)
        newPopulation.append(child)
    
    rockets = newPopulation
