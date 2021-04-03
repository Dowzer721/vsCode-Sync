
from Resistor import Resistor #as ResistorClass
from Cell import Cell

from math import atan2, cos, sin
import pygame

screenW, screenH = (500, 500)
screen = pygame.display.set_mode((screenW, screenH))

circuitOffset = (0.1, 0.9)
components = [
    Resistor("R1", "100k", [[screenW * circuitOffset[0], screenH * circuitOffset[1]], [screenW * circuitOffset[0], screenH * circuitOffset[0]]]),
    Resistor("R2", "22k" , [[screenW * circuitOffset[0], screenH * circuitOffset[0]], [screenW * circuitOffset[1], screenH * circuitOffset[0]]]),
    Resistor("R3", "50k" , [[screenW * circuitOffset[1], screenH * circuitOffset[0]], [screenW * circuitOffset[1], screenH * circuitOffset[1]]]),
    Cell("C1", 9, [[screenW * circuitOffset[0], screenH * circuitOffset[1]], [screenW * circuitOffset[1], screenH * circuitOffset[1]]])
]

# for res in resistors:
#     print(f"{res.ID}: {res.internalResistance}, {len(res.Nodes)}")

# global mainFlag
mainFlag = "Listening"

mouseX, mouseY = (-1, -1)
while(True):
    screen.fill((100, 255, 100))

    # Separate any overlapping nodes:
    for comp1 in components:
        for node1 in comp1.Nodes:
            for comp2 in components:
                if comp1.ID == comp2.ID:
                    continue

                for node2 in comp2.Nodes:
                    x1 = node1.position[0]
                    y1 = node1.position[1]
                    x2 = node2.position[0]
                    y2 = node2.position[1]
                    dx = x2 - x1
                    dy = y2 - y1
                    dist = ((dx**2)+(dy**2)) ** 0.5
                    if dist <= (node1.radius + node2.radius):
                        overlapAmount = (node1.radius + node2.radius) - dist
                        theta = atan2(dy, dx)
                        node1.position[0] -= (cos(theta) * overlapAmount * 0.5)
                        node1.position[1] -= (sin(theta) * overlapAmount * 0.5)
                        node2.position[0] += (cos(theta) * overlapAmount * 0.5)
                        node2.position[1] += (sin(theta) * overlapAmount * 0.5)

    if mainFlag == "Listening":
        pygame.display.set_caption("Basic Components Simulation - Dowzer721 c.2021")
    else:    
        pygame.display.set_caption(mainFlag + " (ESCAPE TO CANCEL EVENT)")

    for comp in components:
        comp.render(screen)
    
    for ev in pygame.event.get():
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()

            if mainFlag == "Listening":
                mainFlag = "Mouse pressed"
            elif mainFlag == "Node selected":
                for comp in components:
                    for node in comp.Nodes:
                        if node.moving:
                            node.position = [mouseX, mouseY]
                            node.moving = False
                            node.renderColour = (0, 0, 0)
                            mainFlag = "Listening"
                            break
                    else:
                        continue
                    break
            
        elif ev.type == pygame.KEYDOWN:
            keyStates = pygame.key.get_pressed()
            if keyStates[pygame.K_ESCAPE]:
                mainFlag = "Listening"
                # mainFlag = "Cancel event"
    
    if mainFlag == "Mouse pressed":
        for comp in components:
            for node in comp.Nodes:
                mouseDx = node.position[0] - mouseX
                mouseDy = node.position[1] - mouseY
                mouseDist = ((mouseDx**2)+(mouseDy**2)) ** 0.5
                if mouseDist <= node.radius:
                    mainFlag = "Node selected"
                    node.moving = True
                    node.renderColour = (200, 200, 200)
                    break
            else:
                continue
            break
        

    

            
    
    # if not (mouseX, mouseY) == (-1, -1):
    #     pygame.draw.circle(
    #         screen, (0, 0, 0),
    #         (mouseX, mouseY),
    #         8, 0
    #     )



    if mainFlag == "Listening":
        pass

    pygame.display.flip()