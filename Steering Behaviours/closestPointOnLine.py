
from LukeLibrary import Vector

def getClosestPointAlongLine(start, end, point, stickToEnds=True):
    """
    This function assumes that "start", "end" and "point" are Vectors; having their own x and y location.
    
    "stickToEnds" is a boolean of whether or not to return the ends of the line if the closest point 
    is beyond the limits of the line.

    This is also not my code, because I don't fully understand the mathematics behind it.
    """

    vectorAP = (point.x - start.x, point.y - start.y)
    vectorAB = (end.x - start.x, end.y - start.y)

    magAB = (vectorAB[0]**2) + (vectorAB[1]**2)

    ABAPproduct = (vectorAB[0] * vectorAP[0]) + (vectorAB[1] * vectorAP[1])

    normalisedDistance = ABAPproduct / magAB

    
    if normalisedDistance < 0:
        if stickToEnds:
            return start
        else:
            return None

    if normalisedDistance > 1:
        if stickToEnds:
            return end
        else:
            return None

    return Vector(
        start.x + (vectorAB[0] * normalisedDistance),
        start.y + (vectorAB[1] * normalisedDistance)
    )
