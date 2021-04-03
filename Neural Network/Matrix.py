"""Create matrices and manipulate them.

Functions:

    Create empty matrix, of size (width, height),
    Create randomly sampled matrix, of size (width, height),
"""
from random import randint

def newMatrix(width, height, defaultValue = 0.0):
    """
    Create a new matrix of size (width, height), with value defaultValue.
    """
    return [
        [defaultValue] * width
    ] * height

def randomSample(width, height, randMin = -1.0, randMax = 1.0, decimalPlaces = 3):
    """Create a new matrix of size (width, height).
    Each item in matrix is a random floating point number between randMin and randMax.
    Each item in matrix is also rounded to decimalPlaces.
    """
    def randomFloat(min_ = -1.0, max_ = 1.0, dec_ = 2):
        rng = max_ - min_
        pct = randint(0, 10 ** dec_) / float(10 ** dec_)
        return round(min_ + (rng * pct), dec_)

    return [
        [randomFloat(randMin, randMax, decimalPlaces) for _ in range(width)]
        for _ in range(height)
    ]