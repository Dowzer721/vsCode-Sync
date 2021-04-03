
# Put this at the top of other files:
# from Component import Component
# or:
# from Component import *

class Component:
    def __init__(self, ID_="", pinCount=2): #, corners_=-1):
        # The string ID of the component:
        self.ID = ID_
        # print(f"ID: {self.ID}")

        # The voltage at each pin gets set to 0 to begin with:
        self.pins = [0.0] * pinCount 

        # I am treating all components as if they are a chip.
        # This means a resistor would be a component with 2 pins, 
        # while an AND gate would be a component with 3 pins. 
        # I am doing this as hopefully it'll be easier to program 
        # in any logic for each component.

        self.nodePositions = []

        self.nodeMoving = [False, False]
    
    
    