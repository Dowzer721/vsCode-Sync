
from Component import Component #as ComponentClass

import pygame

class Resistor(Component):
    def __init__(self, ID_, internalResistance_, nodePositions_=[[-1,-1], [-1,-1]]):
        Component.__init__(self, ID_, 2)
        self.ID = ID_

        possibleFinalCharacters = ['k', 'M', 'G']
        if any(char in internalResistance_ for char in possibleFinalCharacters):
            self.internalResistance = int(internalResistance_[:-1])
            if possibleFinalCharacters[0] in internalResistance_:
                self.internalResistance *= 1000
            elif possibleFinalCharacters[1] in internalResistance_:
                self.internalResistance *= 1000000
            elif possibleFinalCharacters[2] in internalResistance_:
                self.internalResistance *= 1000000000
        else:
            try:
                self.internalResistance = int(internalResistance_)
            except:
                raise Exception(f"{self.ID}: Unknown final character in 'internalResistance' ({internalResistance_[-1]})")
        
        self.Nodes[0].position = nodePositions_[0]
        self.Nodes[1].position = nodePositions_[1]
        
        # print(f"Resistor with ID {self.ID}: Internal Resistance: {self.internalResistance}")
    
    def render(self, display_):
        
        for n in self.Nodes:
            n.render(display_)

        pygame.draw.line(
            display_, (0, 0, 0),
            (
                int(self.Nodes[0].position[0]),
                int(self.Nodes[0].position[1])
            ),
            (
                int(self.Nodes[1].position[0]),
                int(self.Nodes[1].position[1])
            ),
            1
        )

        # pygame.draw.polygon(
        #     display_, (255, 150, 0),
        #     (

        #     )
        # )

# r = Resistor("R1", "1k") # >>> 1000
# r = Resistor("R2", "1M") # >>> 1000000
# r = Resistor("R3", "1G") # >>> 1000000000
# r = Resistor("R4", "1x") # >>> Error