
from Node import Node 

class Component:
    def __init__(self, ID_, nodeCount_):
        self.ID = ID_

        self.Nodes = [
            Node(self, [0, 0])
            for _ in range(nodeCount_)
        ]