
from copy import copy

N = 6
queenCharacter = ' Q '
spaceCharacter = ' - '
findFirstOnly = False


possibleRows = []
for row in range(N):
    leadingZeroCount = row
    binaryString = ('0'*leadingZeroCount) + bin(2 ** (N-1-row))[2:]
    possibleRows.append([int(b) for b in list(binaryString)])
# print(possibleRows)

def listHasRepeatedValue(checkList_):
    for value in checkList_:
        if checkList_.count(value) != 1:
            return True
    
    return False

queenIndexInRows = [N-1 for _ in range(N)]
def decrementQueenIndexes(currentIndexes_):
    currentIndexes_[-1] -= 1
    for row in range(N-2, -1, -1):
        if currentIndexes_[row+1] == -1:
            currentIndexes_[row+1] = N - 1
            currentIndexes_[row] -= 1
    

    return currentIndexes_

# print(queenIndexInRows)
valids = []
for _ in range(N**N):
    queenIndexInRows = decrementQueenIndexes(queenIndexInRows)

    # If an index is repeated, then the Queen will be placed in the same column, and therefore is not a valid position:
    if listHasRepeatedValue(queenIndexInRows): continue

    # Checking the diagonal neighbours of the Queen. If the binary representation of a row is equal to the binary representation 
    # of the distance it is away from the starting row, then the Queen will be diagonally aligned, which is not a valid position:
    queenIndexesAreDiagonallyValid = True
    for currentQueenRow in range(N):
        currentQueenIndex = queenIndexInRows[currentQueenRow]

        for otherQueenRow in range(N):
            if currentQueenRow == otherQueenRow: continue

            otherQueenIndex = queenIndexInRows[otherQueenRow]

            columnDifference = abs(currentQueenIndex - otherQueenIndex)
            rowDifference = abs(currentQueenRow - otherQueenRow)

            if columnDifference == rowDifference:
                queenIndexesAreDiagonallyValid = False
                break

        if queenIndexesAreDiagonallyValid == False: break
    if queenIndexesAreDiagonallyValid == False: continue

    
    valids.append(queenIndexInRows.copy())
    if findFirstOnly: break

if findFirstOnly: 
    print(f"With N={N}, First valid grid found: ")
else:
    print(f"With N={N}, {len(valids)}x valid grids found.")
    input("Enter to display: ")

for validIndexes in valids:
    validGridString = ""
    for index in validIndexes:
        for rowValue in possibleRows[index]:
            if rowValue == 1: 
                validGridString += queenCharacter
            else:
                validGridString += spaceCharacter
        validGridString += '\n'
    print(validGridString)