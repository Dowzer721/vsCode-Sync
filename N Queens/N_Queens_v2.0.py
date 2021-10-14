
N = 46

grid = [
    [0 for _ in range(N)] for _ in range(N)
]

def valid(r, c):

    if grid[r][c] == 1: return False

    if r == 0: return True

    columnAboveValues = [grid[i][c] for i in range(r, -1, -1)]
    if 1 in columnAboveValues: return False

    
    diagonalValues = []
    for i in range(1, N):
        
        rp = r - i
        if rp < 0: break

        cp = c - i
        if cp >= 0: 
            diagonalValues.append(grid[rp][cp])
        
        cn = c + i
        if cn < N:
            diagonalValues.append(grid[rp][cn])

    if 1 in diagonalValues: return False

    return True



def solve(r=0):
    if r == N: return True

    for c in range(N):
        if valid(r, c):
            grid[r] = [0 for _ in range(N)]
            grid[r][c] = 1
            if solve(r + 1) == False:
                # The following row doesn't have any valid positions, so retry this row:
                grid[r] = [0 for _ in range(N)]
                continue
            
            # A valid position was found:
            return True
    
    # No valid position was found in the current row:
    return False

solve()

print([(i+1)%10 for i in range(N)])
print()
for row in grid:
    print(row)