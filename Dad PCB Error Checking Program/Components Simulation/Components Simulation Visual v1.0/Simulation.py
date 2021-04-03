
"""
The final part of this that needs to be implemented is the actual maths to work 
out the values of the resistors, which I have on my phone to compare against. 
But that is going to require programming in behaviour into each component, and 
also adding in interaction between components. 

I think I am going to use the locations of the nodes to work out if components are interacting 
with one another. Although that might cause issues. I am not sure as of yet. 

Whatever happens, remember to video the output and send it to Dad. 
He isn't relying on me sending it to him but I think it'll be good to show him.
"""

from Resistor import Resistor
from Wire import Wire
from Cell import Cell

import pygame
screenW, screenH = (500, 500)
screen = pygame.display.set_mode((screenW, screenH))

resistors = [
    Resistor("R0", "100k", (screenW * 0.1, screenH * 0.9), (screenW * 0.1, screenH * 0.1)),
    Resistor("R1", "22k" , (screenW * 0.1, screenH * 0.1), (screenW * 0.9, screenH * 0.1)),
    Resistor("R2", "50k" , (screenW * 0.9, screenH * 0.1), (screenW * 0.9, screenH * 0.9))
]

wires = [
    Wire( newNodePositions_=[(screenW*0.9, screenH*0.9), (screenW*0.6, screenH*0.9)] ),
    Wire( newNodePositions_=[(screenW*0.4, screenH*0.9), (screenW*0.1, screenH*0.9)] )
]

cells = [
    Cell(startPosition_=wires[0].nodePositions[-1], endPosition_=wires[1].nodePositions[0])
]

global Flag # Declaration of variable
def updateFlag(newFlag):
    global Flag # Reference of variable
    Flag = newFlag

    if newFlag == "Moving Node":
        pygame.display.set_caption("Click to move node, ESC to cancel, A to add node")
    else:
        # newFlag == "Listening" or "Cancel Node Move" or "Add Node"
        pygame.display.set_caption("Basic Components Simulation - Dowzer721 c.2021")
        

updateFlag("Listening")

while(True):
    screen.fill((200, 200, 200))
    
    for r in resistors:
        r.render(screen)
        if Flag == "Cancel Node Move":
            r.nodeMoving = [False, False]
    
    for w in wires:
        if Flag == "Add Node":
            if True in w.nodeMoving:
                w.addNode()
                updateFlag("Cancel Node Move")
                

        w.render(screen)
        if Flag == "Cancel Node Move":
            w.nodeMoving = [False for _ in range(w.nodeCount)]
        
    
    for c in cells:
        c.render(screen)
        if Flag == "Cancel Node Move":
            c.nodeMoving = [False, False]
    
    if Flag == "Cancel Node Move":
        updateFlag("Listening")

    
    if Flag == "Listening":
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                # print(mouseX, mouseY)
                for r in resistors:
                    for node in range(2):
                        pos = r.nodePositions[node]
                        dx = abs(pos[0] - mouseX)
                        dy = abs(pos[1] - mouseY)
                        dist = ((dx**2) + (dy**2)) ** 0.5
                        if dist <= 4:
                            r.nodeMoving[node] = True
                            updateFlag("Moving Node")
                            break
                    else:
                        continue
                    # break

                for w in wires:
                    for node in range(w.nodeCount):
                        pos = w.nodePositions[node]
                        dx = abs(pos[0] - mouseX)
                        dy = abs(pos[1] - mouseY)
                        dist = ((dx**2) + (dy**2)) ** 0.5
                        if dist <= 4:
                            w.nodeMoving[node] = True
                            updateFlag("Moving Node")
                            break
                    else:
                        continue
                    # break
                
                for c in cells:
                    for node in range(2):
                        pos = c.nodePositions[node]
                        dx = abs(pos[0] - mouseX)
                        dy = abs(pos[1] - mouseY)
                        dist = ((dx**2) + (dy**2)) ** 0.5
                        if dist <= 4:
                            c.nodeMoving[node] = True
                            updateFlag("Moving Node")
                            break
                    else:
                        continue
                    # break
    
    if Flag == "Moving Node":
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                pressedKeys = pygame.key.get_pressed()
                if pressedKeys[pygame.K_ESCAPE]:
                    updateFlag("Cancel Node Move")
                    break
                elif pressedKeys[pygame.K_a]:
                    updateFlag("Add Node")
                    break
        
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for r in resistors:
                    for node in range(2):
                        if r.nodeMoving[node]:
                            r.nodePositions[node] = [mouseX, mouseY]
                            r.nodeMoving[node] = False
                            r.updateNodePositions()
                            updateFlag("Listening")
                            break
                    else:
                        continue
                    # break
                
                for w in wires:
                    for node in range(w.nodeCount):
                        if w.nodeMoving[node]:
                            w.nodePositions[node] = [mouseX, mouseY]
                            w.nodeMoving[node] = False
                            # w.updateNodePositions()
                            updateFlag("Listening")
                            break
                    else:
                        continue
                    # break

                for c in cells:
                    for node in range(2):
                        if c.nodeMoving[node]:
                            c.nodePositions[node] = [mouseX, mouseY]
                            c.nodeMoving[node] = False
                            updateFlag("Listening")
                            break
                    else:
                        continue
                    # break
                    
    
    pygame.display.flip()