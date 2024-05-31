
from math import pi, cos, sin, atan2

import pygame
canvasW, canvasH = 400, 600
canvas = pygame.display.set_mode((canvasW, canvasH))

from random import randint, sample
rf = lambda: randint(0, 1000) / 1000.

from time import time
def delay(secs):
  start = time()
  while start + secs > time(): pass

rocketRadius = 16
targetRadius = rocketRadius * 3
dnaLength = 100
populationSize = 500
mutationRate = 0.05

frame = 0

class Vector:
  def __init__(self, x_=0, y_=0):
    self.x = x_
    self.y = y_
  
  @staticmethod
  def fromAngle(angle):
    return Vector(cos(angle), sin(angle))
  
  def mult(self, val):
    self.x *= val
    self.y *= val
  
  def add(self, vec):
    self.x += vec.x
    self.y += vec.y
  
  def heading(self):
    return atan2(self.y, self.x)
  
  def xy(self):
    return (self.x, self.y)
  
  def dist(self, vec):
    dx = self.x - vec.x
    dy = self.y - vec.y
    return ((dx**2) + (dy**2)) ** 0.5
  
  def copy(self):
    return Vector(self.x, self.y)
    
targetPosition = Vector(canvasW//3, targetRadius)

gene = lambda: rf() * 2 * pi # pi + (rf() * pi) # (3*pi/2) - 0.3 + (rf() * 0.3 * 2)
class DNA:
  def __init__(self):
    self.genes = [gene() for _ in range(dnaLength)]

class Rocket:
  def __init__(self, passedDownGenes_=None):
    
    self.DNA = DNA()
    if passedDownGenes_ != None:
      self.DNA.genes = passedDownGenes_
    
    self.pos = Vector(canvasW//2, canvasH)
    self.vel = Vector()
    self.acc = Vector.fromAngle(self.DNA.genes[0])
    
    self.path = []
    
    self.dead = False
    self.deathFrame = 0
    
    
    heading = self.vel.heading()
    self.renderAngles = [0, 2*pi/3, 0, 4*pi/3]
    self.renderDistances = [1, 0.6, 0, 0.6]
    self.renderVertices = [
      ( self.pos.x + (cos(heading+self.renderAngles[i])*rocketRadius*self.renderDistances[i]), 
        self.pos.y + (sin(heading+self.renderAngles[i])*rocketRadius*self.renderDistances[i])
      )
      for i in range(4)
    ]
  
  def kill(self):
    if self.deathFrame == 0:
      self.dead = True
      self.deathFrame = frame
  
  def mutate(self):
    for g in self.DNA.genes:
      if rf() <= mutationRate:
        g = gene()
  
  def move(self):
    self.vel.add(self.acc)
    # self.vel.mult(0.1)
    self.pos.add(self.vel)
    self.acc.mult(0)
    
    self.path.append(self.pos.xy())
  
  def updateRenderVertices(self):
    # heading = self.vel.heading()
    # self.renderVertices = [
    #   ( self.pos.x + (cos(heading+self.renderAngles[i])*rocketRadius*self.renderDistances[i]), 
    #     self.pos.y + (sin(heading+self.renderAngles[i])*rocketRadius*self.renderDistances[i])
    #   )
    #   for i in range(4)
    # ]
    pass
    
  def render(self):
    # pygame.draw.polygon(canvas, (0,0,0), self.renderVertices, 0)

    # Drawing a dick because I'm a dick
    heading = self.vel.heading()
    shaft = [
      (self.pos.x + (cos(heading + (pi*1.1))*rocketRadius), self.pos.y + (sin(heading+(pi*1.1))*rocketRadius)),
      (self.pos.x + (cos(heading + (pi*0.9))*rocketRadius), self.pos.y + (sin(heading+(pi*0.9))*rocketRadius)),
      (self.pos.x + (cos(heading + (pi*0.1))*rocketRadius), self.pos.y + (sin(heading+(pi*0.1))*rocketRadius)),
      (self.pos.x + (cos(heading + (pi*1.9))*rocketRadius), self.pos.y + (sin(heading+(pi*1.9))*rocketRadius)),
    ]
    pygame.draw.circle(canvas, (0,0,0), shaft[0], rocketRadius//3, 0)
    pygame.draw.circle(canvas, (0,0,0), shaft[1], rocketRadius//3, 0)
    pygame.draw.circle(canvas, (0,0,0), ((shaft[2][0] + shaft[3][0])//2, (shaft[2][1] + shaft[3][1])//2 ), rocketRadius//2, 0)
    pygame.draw.polygon(canvas, (0,0,0), shaft, 0)
  
  def update(self):
    if self.dead == False:
      self.move()
      self.updateRenderVertices()
    self.render()



Population = [Rocket() for _ in range(populationSize)]
# bestRocketFinalPosition = Population[0].pos
bestRocketPath = [(0,0) for _ in range(dnaLength)]


# tS = target_Start
tS_dx = (canvasW//2) - targetPosition.x
tS_dy = canvasH - targetPosition.y
tS_theta = atan2(tS_dy, tS_dx)

tX, tY = targetPosition.xy()
cX = tX + (cos(tS_theta) * targetRadius)
cY = tY + (sin(tS_theta) * targetRadius)
closestTargetPointToStart = Vector(cX, cY)

print("Black bar is progress through this epoc.")
print("Large green circle is the target.")
print("Small green circle is the closest target edge.")
print("Green line is optimal path.")
print("Blue dots are best path.")



while True:
  # for ev in pygame.event.get():
  #   if ev.type == pygame.MOUSEBUTTONUP:
  #     Population[0].move()
  #     print(Population[0].pos.xy())
      
      
  canvas.fill((255,255,255))
  
  # Draw target:
  pygame.draw.circle(canvas, (100,255,100), targetPosition.xy(), targetRadius, 0)
  pygame.draw.line(canvas, (100,255,100), (canvasW//2,canvasH), targetPosition.xy(), 2)
  pygame.draw.circle(canvas, (100,255,100), closestTargetPointToStart.xy(), targetRadius//4, 0)
  
  # Draw best Individual:
  # pygame.draw.circle(canvas, (100,100,255), bestRocketFinalPosition.xy(), rocketRadius, 0)
  for pathPt in bestRocketPath:
    pygame.draw.circle(canvas, (100,100,255), pathPt, rocketRadius//4, 0)
  
  
  # Draw progress bar:
  pygame.draw.line(canvas, (0,0,0), (0,10), (frame*canvasW/dnaLength,10), 10)
  
  allDead = True
  for R in Population:
    R.acc = Vector.fromAngle(R.DNA.genes[frame])
    R.update()
    
    if  ((R.pos.y < 0) or
        (R.pos.y > canvasH + rocketRadius) or
        (R.pos.x < 0) or
        (R.pos.x > canvasW) or
        (R.pos.dist(targetPosition) <= targetRadius)):
      R.kill()
    
    if R.dead == False: allDead = False
  


  pygame.display.update()
  frame += 1
  
  if (frame == dnaLength) or allDead:
    # Spawn new population
    
    matingPool = []
    
    closestDistance = float("inf")
    closestDistancePath = []
    
    for Ri in range(populationSize):
      R = Population[Ri]
      # if R.dead: continue
      
      # R = Population[Ri]
      # if R.targetReachedFrame == 0: R.targetReachedFrame = dnaLength
      
      targetDistance = R.pos.dist(targetPosition) + R.pos.dist(closestTargetPointToStart)
      additionCount = (dnaLength - R.deathFrame) - targetDistance
      for _ in range(int(additionCount)): matingPool.append(Ri)
      
      if targetDistance < closestDistance:
        closestDistance = targetDistance
        closestDistancePath = R.path
    
    # print(matingPool)
    if len(matingPool) < populationSize: matingPool = [i for i in range(populationSize)]
    
    childrenOfPopulation = []
    for _ in range(populationSize):
      parentA_Genes = Population[sample(matingPool, 1)[0]].DNA.genes
      parentB_Genes = Population[sample(matingPool, 1)[0]].DNA.genes
      crossoverPoint= randint(0, dnaLength-1)
      child = Rocket(parentA_Genes[0:crossoverPoint] + parentB_Genes[crossoverPoint:])
      child.mutate()
      childrenOfPopulation.append(child)
    
    Population = childrenOfPopulation
    
    frame = 0
    
    bestRocketPath = closestDistancePath
    
    pass
  
  frame %= dnaLength

  delay(0.1)
  # print(frame)
















