
"""
This script works, but I am sure there are some bottlenecks and places which I could 
speed up the process. 
I think it could also be helpful to replace the percentage counter with a progressbar, 
which is probably a lot more resource efficient too. 


"""
from math import exp

N = 9
queenCharacter = ' Q '
spaceCharacter = ' - '
showFirstOnly = True
estimateTime = True

if estimateTime:
    # Found using: https://www.dcode.fr/function-equation-finder
    
    # # Equation:
    # # "PARABOLA/HYPERBOLA USING CURVE FITTING"
    # # t ~= (14.4525*(N**2)) - (152.422*N) + 386.814
    # # t ~= (a) - (b) + (c)
    # a = 14.4525 * (N**2)
    # b = 152.422 * N
    # c = 386.814
    # estimate = a-b+c # Function can produce negative values
    # if estimate < 0: estimate = "< 1"
    
    # Equation:
    # "EXPONENTIAL USING CURVE FITTING"
    # t ~= (7.622x10^-8 * e^(2.628*N)) - 0.989
    # t ~= (a * b) - c
    a = 7.621972640703 * (10**-8)
    b = exp(2.62803*N)
    c = 0.989087
    estimate = (a * b) - c

    # I want this to be formatted better, but also be dynamic. So any amount of time will be formatted correctly into hh:mm:ss.
    if estimate >= 3600:
        h = int(estimate / 3600)
        estimate /= 3600
        print(f"Estimated completion time: {round(estimate,2)} hours")
    elif estimate >= 60:
        m = int(estimate / 60)
        s = int( ((estimate / 60) - m) * 60 )
        print(f"Estimated completion time: {m}m {s}s")
    else:
        print(f"Estimated completion time: {round(estimate,2)} seconds")
    

    
    
    


gridRowIndexes = [N-1 for _ in range(N)]

def decrementRowIndexes():
    global gridRowIndexes
    gridRowIndexes[-1] -= 1
    for row in range(N-2, -1, -1):
        if gridRowIndexes[row+1] == -1:
            gridRowIndexes[row] -= 1
    
    gridRowIndexes = [index if index >= 0 else N-1 for index in gridRowIndexes]

validGridsFound = []

for binaryCounter in range((N**N)-1):
    decrementRowIndexes()

    rowsValid = True
    columnsValid = [(gridRowIndexes.count(indexCounter)==1) for indexCounter in range(N)].count(True) == N
    # columnsValid = not (True in [gridRowIndexes[binaryCounter] == gridRowIndexes[indexCounter] for indexCounter in range(N)])
    
    # Check the diagonals:
    diagonalsValid = True
    for currentRowStep in range(N): # 0, 1, 2, 3
        currentRowValue = 2 ** gridRowIndexes[currentRowStep]
        for adjacentRowStep in range(1, N):
            denominator_or_multiplier = 2 ** adjacentRowStep
            
            # Check above:
            aboveRowIndex = currentRowStep - adjacentRowStep
            if aboveRowIndex >= 0:
                aboveRowValue = 2 ** gridRowIndexes[aboveRowIndex]
                if aboveRowValue == (currentRowValue / denominator_or_multiplier):
                    diagonalsValid = False
                    break
                if aboveRowValue == (currentRowValue * denominator_or_multiplier):
                    diagonalsValid = False
                    break
            
            # Check below:
            belowRowIndex = currentRowStep + adjacentRowStep
            if belowRowIndex < N:
                belowRowValue = 2 ** gridRowIndexes[belowRowIndex]
                if belowRowValue == (currentRowValue / denominator_or_multiplier):
                    diagonalsValid = False
                    break
                if belowRowValue == (currentRowValue * denominator_or_multiplier):
                    diagonalsValid = False
                    break
                
        

    if rowsValid and columnsValid and diagonalsValid:
        indexesToGrid = [] #[bin(2**index)[2:] for index in gridRowIndexes]
        for index in gridRowIndexes:
            preceedingZeroCount = N - 1 - index
            followingZeroCount = N - 1 - preceedingZeroCount

            #indexesToGrid.append(('0'*preceedingZeroCount) + bin(2**index)[2:])
            indexesToGrid.append(
                (spaceCharacter*preceedingZeroCount) + 
                queenCharacter + 
                (spaceCharacter*followingZeroCount)
            )

        validGridsFound.append(indexesToGrid)
        
        if showFirstOnly:
            print('\n'.join(indexesToGrid) + '\n')
            break

    if not showFirstOnly:
        print(f"{round(binaryCounter * 100 / (N**N), 2)}% Complete")

if not showFirstOnly:
    for grid in validGridsFound:
        print('\n'.join(grid) + '\n')

if len(validGridsFound) == 0:
    print(f"\n!!! No valid grids found for N={N} !!!\n")