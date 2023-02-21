
N = 4

maximumBinaryValue = 2 ** (N ** 2)

def gridIsValid(grid):
    for r in range(N):
        if grid[r].count('1') != 1: 
            # input(grid[r])
            return False
    
    for c in range(N):
        col = [grid[r][c] for r in range(N)]
        if col.count('1') != 1: 
            # input(col)
            return False
    
    # Check diagonals:
    diagonalAdditions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    for queenRow in range(N):
        queenCol = grid[queenRow].index('1')

        for direction in range(4):
            for i in range(1, N+1):
                nextRow = queenRow + (diagonalAdditions[direction][0] * i)
                nextCol = queenCol + (diagonalAdditions[direction][1] * i)
                if nextRow >= N or nextRow < 0 or nextCol >= N or nextCol < 0:
                    #print(f"nextRow: {nextRow}, nextCol: {nextCol}")
                    break

                if grid[nextRow][nextCol] == '1': return False
    
    return True

startingValue = int( (('0'*(N-1)) + '1') * N, 2) # int("0001" * N, 2)
# input(f"{startingValue}: {bin(startingValue)} -> {maximumBinaryValue}")

for i in range(startingValue, maximumBinaryValue):
    binaryString = bin(i)[2:]
    preceedingZeroCount = (N**2) - len(binaryString)
    binaryString = ('0'*preceedingZeroCount) + binaryString
    
    rows = [list(binaryString[r*N : (r+1)*N]) for r in range(N)]
    # input(f"{binaryString}: {rows}")


    if gridIsValid(rows):
        # print(rows)

        rowString = ""
        for r in range(N):
            rowString += ''.join(rows[r]) + '\n'
        
        print(rowString)

        break
else:
    print("Valid grid not found")


    # print(f"{i}: {binaryString}: {rows}")