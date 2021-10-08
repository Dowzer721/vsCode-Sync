
# I need to implement pencil-lines. As in if a region has a number penciled in, in a line, 
# then the other regions in line with that line need to remove the number from their pencils too. 
# ...
# That makes sense to me. 

from time import time

# Easy Board:
# pens = [
#     [0,7,0,0,2,0,0,4,6], 
#     [0,6,0,0,0,0,8,9,0], 
#     [2,0,0,8,0,0,7,1,5], 
#     [0,8,4,0,9,7,0,0,0], 
#     [7,1,0,0,0,0,0,5,9], 
#     [0,0,0,1,3,0,4,8,0], 
#     [6,9,7,0,0,2,0,0,8], 
#     [0,5,8,0,0,0,0,6,0], 
#     [4,3,0,0,8,0,0,7,0]
# ]

# Medium Board:
# pens = [
#     [4,1,0,0,0,0,0,6,8],
#     [6,0,0,0,0,0,0,2,0],
#     [0,0,0,0,0,0,5,1,0],
#     [0,0,0,2,4,0,6,9,0],
#     [3,0,0,0,5,0,0,0,0],
#     [5,0,6,0,0,9,0,0,1],
#     [0,0,0,7,0,0,3,0,0],
#     [9,0,2,0,6,4,0,0,0],
#     [0,0,7,9,0,8,0,5,0]
# ]

# Hard Board:
# pens = [
#     [2,0,0,5,0,7,4,0,6],
#     [0,0,0,0,3,1,0,0,0],
#     [0,0,0,0,0,0,2,3,0],
#     [0,0,0,0,2,0,0,0,0],
#     [8,6,0,3,1,0,0,0,0],
#     [0,4,5,0,0,0,0,0,0],
#     [0,0,9,0,0,0,7,0,0],
#     [0,0,6,9,5,0,0,0,2],
#     [0,0,1,0,0,6,0,0,8]
# ]

# 03/10/21 Puzzle Page
pens = [
    [0,0,8,0,2,0,6,0,0],
    [1,7,0,0,0,0,0,0,3],
    [0,0,0,0,0,0,0,9,0],
    [0,0,5,0,6,3,4,0,8],
    [0,8,6,0,0,0,0,0,5],
    [0,0,0,0,0,2,7,0,0],
    [2,4,0,8,0,9,0,7,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,5,0,0]
]

pencils = [
    [[i for i in range(1, 10)] for _ in range(9)] for _ in range(9)
]

def calculateRegion(col_, row_):
    return int(col_ / 3) + (int(row_ / 3) * 3)

regions = [ [] for _ in range(9) ]
for r in range(9):
    for c in range(9):
        region = calculateRegion(c, r)
        regions[region].append((r, c))
# print(f"Regions: {regions}")

def setPencils(col_, row_):
    
    if pens[row_][col_] > 0: 
        pencils[row_][col_] = []
        return

    columnPens = [pens[r][col_] for r in range(9)]
    rowPens = pens[row_]

    regionNumber = calculateRegion(col_, row_)
    regionPens = []
    for pos in regions[regionNumber]:
        r, c = pos
        regionPens.append(pens[r][c])
    
    # for _ in range(9):
    #     try: columnPens.remove(0)
    #     except: pass

    #     try: rowPens.remove(0)
    #     except: pass

    #     try: regionPens.remove(0)
    #     except: pass
    
    for n in range(1, 10):
        if (n in columnPens) or (n in rowPens) or (n in regionPens):
            # try: pencils[row_][col_].remove(n)
            # except: pass
            pencils[row_][col_][n-1] = 0

def removePencilsAfterLines(startingRegion_, numberToRemove_):
    # print(f"removePencilsAfterLines({startingRegion_}, {numberToRemove_})")

    # def list_rindex(list, obj):

    #     for i in reversed(range(len(list))):
    #         if list[i] == obj:
    #             return i
        
    #     # return -1
    #     raise ValueError(f"{obj} is not in list")

    regionPencils = []
    for r, c in regions[startingRegion_]:
        regionPencils.append(pencils[r][c])
    # print(regionPencils)

    # for pencilNumber in range(1, 10):
        # occurenceCountInRegion = 0
        # for cellPencils in regionPencils:
        #     occurenceCountInRegion += int(pencilNumber in cellPencils)
        
    occurenceCountInRegion = sum(
        [int(numberToRemove_ in cellPencils) for cellPencils in regionPencils]
    )
    # print(f"{numberToRemove_} count: {occurenceCountInRegion}")

    if occurenceCountInRegion == 2:
        # Check for them being in the same column or row:
        firstOccurenceColumn = firstOccurenceRow = lastOccurenceColumn = lastOccurenceRow = None

        for i in range(9):
            if (numberToRemove_ in regionPencils[i]):
                # print(f"First Occurence cell: {i}")
                firstOccurenceRow = int(i / 3)
                firstOccurenceColumn = i % 3 # [(pencil == numberToRemove_) for pencil in regionPencils[i]].index(True)
                # print(f"First Occurence col: {firstOccurenceColumn}, row: {firstOccurenceRow}")

                break
        
        for i in range(8, -1, -1):
            if (numberToRemove_ in regionPencils[i]):
                # print(f"Last Occurence cell: {i}")
                lastOccurenceRow = int(i / 3) # i % 3
                lastOccurenceColumn = i % 3 # [(pencil == numberToRemove_) for pencil in regionPencils[i]].index(True)
                # print(f"Last Occurence col: {lastOccurenceColumn}, row: {lastOccurenceRow}")
                
                break
        
        if firstOccurenceColumn == lastOccurenceColumn:
            # The columns match for the two occurences, so remove the pencil 
            # number from the other regions in line with these two occurences:
            
            # Get the other two regions in the vertical axes:
            # print(f"Number to remove: {numberToRemove_}")
            # print(f"GET TWO VERTICAL REGIONS, IN LINE WITH REGION {startingRegion_}")

            verticalRegionGroups = [
                [0, 3, 6],
                [1, 4, 7],
                [2, 5, 8]
            ]

            verticalGroupRegionIsIn = [(startingRegion_ in group) for group in verticalRegionGroups].index(True)
            verticalRegionGroups[verticalGroupRegionIsIn].remove(startingRegion_)

            # input(f"OTHER TWO VERTICAL REGIONS ARE: {verticalRegionGroups[verticalGroupRegionIsIn][0]}, {verticalRegionGroups[verticalGroupRegionIsIn][1]}")

            # Remove the pencils of the numberToRemove in those other regions' cells:
            for otherRegionNumber in verticalRegionGroups[verticalGroupRegionIsIn]:
                for r, _ in regions[otherRegionNumber]:
                    # try: pencils[r][firstOccurenceColumn].remove(numberToRemove_)
                    # except: pass

                    try: pencils[r][firstOccurenceColumn][numberToRemove_] = 0
                    except: pass

                    # pencils[r][firstOccurenceColumn].remove(numberToRemove_)
        


        if firstOccurenceRow == lastOccurenceRow:
            # The rows match for the two occurences, so remove the pencil 
            # number from the other regions in line with these two occurences:
            
            # Get the other two regions in the horizontal axes:
            # print(f"Number to remove: {numberToRemove_}")
            # print(f"GET TWO HORIZONTAL REGIONS, IN LINE WITH REGION {startingRegion_}")

            horizontalRegionGroups = [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]
            ]

            horizontalGroupRegionIsIn = [(startingRegion_ in group) for group in horizontalRegionGroups].index(True)
            horizontalRegionGroups[horizontalGroupRegionIsIn].remove(startingRegion_)

            # input(f"OTHER TWO HORIZONTAL REGIONS ARE: {horizontalRegionGroups[horizontalGroupRegionIsIn][0]}, {horizontalRegionGroups[horizontalGroupRegionIsIn][1]}")

            # Remove the pencils of the numberToRemove in those other regions' cells:
            for otherRegionNumber in horizontalRegionGroups[horizontalGroupRegionIsIn]:
                for _, c in regions[otherRegionNumber]:
                    # try: pencils[r][firstOccurenceColumn].remove(numberToRemove_)
                    # except: pass

                    try: pencils[firstOccurenceRow][c][numberToRemove_] = 0
                    except: pass

                    # pencils[r][firstOccurenceColumn].remove(numberToRemove_)




        

# for r in range(9):
#     for c in range(9):
#         setPencils(c, r)




def boardComplete():
    cellsFilled = 0
    for r in range(9):
        for c in range(9):
            cellsFilled += int(pens[r][c] > 0)
    return (cellsFilled == 81), cellsFilled

startTime = time()
quitTime = 3
conceeded = False

while (not boardComplete()[0]) and (not conceeded):

    ellapsedTime = (time() - startTime)

    if ellapsedTime > quitTime: 
        conceeded = True
        continue

    completeCount = boardComplete()[1]
    # print(f"Percentage Complete: {round(100 * completeCount / 81)}%")
    print(f"Remaining Time: {round(quitTime - ellapsedTime, 1)}s, Completion: {round(100 * completeCount / 81)}%")
    
    for r in range(9):
        for c in range(9):
            # print(f"{c}{r}")
            setPencils(c, r)
    
    # If more than half the allotted time has passed, whip out the big guns. 
    # I feel that doing this allows for the basic technique to attempt the solve first, 
    # then if it hasn't solved it fast enough, the more advanced technique can be carried out. 
    if ellapsedTime >= (quitTime / 2):
        for region in range(9):
            for n in range(1, 10):
                removePencilsAfterLines(region, n)
    
    
    
    for r in range(9):
        for c in range(9):
            if pencils[r][c].count(0) == 8: # There's only one valid pencil number: 
                # a = [(pencils[r][c][i] > 0) for i in range(9)]
                # pens[r][c] = a.index(True) + 1
                pens[r][c] = [(pencils[r][c][i] > 0) for i in range(9)].index(True) + 1
                pencils[r][c] = [] # [a.index(True) + 1 for _ in range(9)]

def printBoard():
    print("_ "*12)
    for r in range(9):
        row = ""
        for c in range(9):
            if pens[r][c] > 0:
                row += str(pens[r][c]) + ' '
            else:
                row += "  "

            if (c + 1) % 3 == 0:
                row += "| "
        
        print(row)
        if (r + 1) % 3 == 0:
            print("_ "*12)

if not conceeded:
    totalTime = time() - startTime
    print(f"Solved in {round(totalTime, 3)} seconds ({float(quitTime)}s allowed).")
    printBoard()

else:

    print(f"Unsolved within {quitTime} seconds, conceeding.")
    print(f"This is as far as the solver got ({round(100*completeCount/81)}% completion):")
    printBoard()
