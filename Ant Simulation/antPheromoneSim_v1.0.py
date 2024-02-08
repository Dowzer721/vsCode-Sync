
from math import atan2, cos, sin
import pygame
from random import randint

canvasW, canvasH = 500, 500
canvas = pygame.display.set_mode((canvasW, canvasH))

PheromoneDropFrame = 50
PheromoneFrameReduction = 0.01
# print(100 / (PheromoneDropFrame * PheromoneFrameReduction))

FoodHubCount = 3
FoodHubSpread = 20
FoodCountPerHub = 10

def rf(min_=-1.0, max_=1.0, dp_=3):
    _rng = max_ - min_
    _pct = randint(0, 10**dp_) / (10 ** dp_)
    return round(min_ + (_rng * _pct), dp_)

pToC = lambda pt, angle, radius: (int(pt[0]+cos(angle)*radius), int(pt[1]+sin(angle)*radius))

foodHubs = [
    pToC( (canvasW//2,canvasH//2), rf()*3.14*2, randint(int(canvasW*0.3), int(canvasW*0.5)) )
    for _ in range(FoodHubCount)
]
foodLocations = []
for hx,hy in foodHubs:
    for _ in range(FoodCountPerHub):
        fx = hx + randint(-FoodHubSpread//2, FoodHubSpread//2)
        fy = hy + randint(-FoodHubSpread//2, FoodHubSpread//2)
        foodLocations.append((fx, fy))

class Pheromone:
    def __init__(self, pos_, type_="explore"):
        self.pos = pos_
        self.type = type_
        self.potency = 100
    def render(self):
        renderColour = (0, 0, 0)
        transparencyValue = 255 - int(105 * self.potency / 100)
        if self.type == "explore":
            renderColour = (255, transparencyValue, transparencyValue)
        elif self.type == "return":
            renderColour = (transparencyValue, transparencyValue, 255)
        # print(renderColour)
        
        pygame.draw.circle(canvas, renderColour, self.pos, 4, 0)
Pheromones = []

class Ant:
    def __init__(self, startingPosition):
        self.pos = startingPosition
        self.vel = [0, 0]
        self.speed = 0.1
        
    def update(self):
        heading = atan2(self.vel[1], self.vel[0])
        newHeading = heading + (rf() * 0.1)
        self.vel = [cos(newHeading), sin(newHeading)]

        self.pos[0] += (self.vel[0] * self.speed)
        self.pos[1] += (self.vel[1] * self.speed)

        self.pos[0] = max(0, min(self.pos[0], canvasW))
        self.pos[1] = max(0, min(self.pos[1], canvasH))
        

    def render(self):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(canvas, (0,0,0), (x,y), 4, 0)

Population = [Ant([canvasW//2, canvasH//2]) for _ in range(1)]

simulationFrame = 0
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if ev.type == pygame.MOUSEBUTTONUP:
            print(len(Pheromones))
    
    canvas.fill((255, 255, 255))

    for F in foodLocations:
        pygame.draw.circle(canvas, (150, 255, 150), F, 4, 0)

    for A in Population:
        A.update()
        if simulationFrame % PheromoneDropFrame == 0:
            Pheromones.append(
                Pheromone((int(A.pos[0]), int(A.pos[1])))
            )
        A.render()
    
    for P in Pheromones:
        P.render()
        P.potency -= PheromoneFrameReduction
        if P.potency <= 0:
            Pheromones.remove(P)
    
    pygame.display.update()
    simulationFrame += 1
    # if simulationFrame % (PheromoneDropFrame+1) == 0:
    #     print(len(Pheromones))
