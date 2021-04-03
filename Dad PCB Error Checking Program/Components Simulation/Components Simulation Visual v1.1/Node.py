
import pygame

class Node:
    def __init__(self, parent_, position_, radius_=4):
        self.parent = parent_

        self.value = 0.0
        self.position = position_
        self.moving = False

        self.radius = int(radius_)
        self.renderColour = (0, 0, 0)
    
    def sendValue(self, recipient):
        recipient.receiveValue(self.value)
    
    def receiveValue(self, value_):
        self.value = value_
    
    def render(self, display_, fill_ = True, mousePos_ = (-1, -1)):
        pygame.draw.circle(
            display_, self.renderColour,
            (   int(self.position[0]),
                int(self.position[1])
            ),
            self.radius,
            int(not fill_)
        )

        # if not mousePos_ == (-1, -1):
        #     pygame.draw.line(
        #         display_, self.renderColour,
        #         (   int(self.position[0]),
        #             int(self.position[1])
        #         ),
        #         mousePos_,
        #         1
        #     )