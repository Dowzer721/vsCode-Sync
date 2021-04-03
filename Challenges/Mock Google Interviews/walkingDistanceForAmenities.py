
"""
I will include the link to the video this is from at some point.

The setup for the question is as follows:

Imagine there is a long street, and each block ALWAYS has one Apartment, in which you can live.
There also exists some of the following on each block:

Food Shop;
Gym;
Park;

Each block does not necessarily contain 1 of each, such as the following:

Block 0:
Apartment:  True
Food Shop:  True
Gym:        False
Park:       True

Block 1:
Apartment:  True
Food Shop:  False
Gym:        True
Park:       False

Block 2:
Apartment:  True
Food Shop:  False
Gym:        False
Park:       False

Question:
Find the best block to live in, so that all of the 
amenities you desire are as close as possible.

"""
from random import randint

class Block:
    def __init__(self, blockNum_):
        self.blockNumber = blockNum_
        self.Apartment  = True
        self.FoodShop   = randint(0, 1000) < 500
        self.Gym        = randint(0, 1000) < 500
        self.Park       = randint(0, 1000) < 500

        print(
            f"Num: {self.blockNumber}\n" + 
            f"A: {self.Apartment}\n" + 
            f"F: {self.FoodShop}\n" + 
            f"G: {self.Gym}\n" + 
            f"P: {self.Park}\n"
        )

streetLength = 5
street = [Block(b) for b in range(streetLength)]