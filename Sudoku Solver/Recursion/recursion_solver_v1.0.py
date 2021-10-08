
from time import time

def delay(secs_):
    now = time()
    while (now + secs_) > time():
        pass

# board = [
#     [0,0,8,0,2,0,6,0,0],
#     [1,7,0,0,0,0,0,0,3],
#     [0,0,0,0,0,0,0,9,0],
#     [0,0,5,0,6,3,4,0,8],
#     [0,8,6,0,0,0,0,0,5],
#     [0,0,0,0,0,2,7,0,0],
#     [2,4,0,8,0,9,0,7,0],
#     [0,0,0,0,0,0,0,0,0],
#     [0,0,3,0,0,0,5,0,0]
# ]

board = [
    [0,0,1,3,0,2,0,0,0],
    [0,0,3,0,0,7,0,4,5],
    [0,0,7,0,0,0,0,0,9],
    [0,0,6,5,0,0,0,7,0],
    [2,0,0,0,0,0,0,0,1],
    [0,9,0,0,0,1,4,0,0],
    [5,0,0,0,0,0,9,0,0],
    [6,1,0,2,0,0,8,0,0],
    [0,0,0,9,0,8,5,0,0]
]

regionPositions = [[] for _ in range(9)]
def calculateRegion(r_, c_):
    # r_: row
    # c_: column
    return int(c_ / 3) + (int(r_ / 3) * 3)

for r in range(9):
    for c in range(9):
        regionPositions[ calculateRegion(r, c) ].append((r, c))

def valid(r_, c_, n_):
    # r_: row
    # c_: column
    # n_: number to check validity

    # The pens in the current row, excluding all the zeroes:
    rowPens = [pen for pen in board[r_] if pen > 0]

    # The pens in the current column, excluding all the zeroes:
    columnPens = [board[i][c_] for i in range(9) if board[i][c_] > 0]

    # The pens in the current region, excluding all the zeroes:
    regionPens = [ board[r][c] for r, c in regionPositions[calculateRegion(r_, c_)] if board[r][c] > 0 ]
    
    # print(
    #     f"row:{rowPens} \n" + 
    #     f"col:{columnPens} \n" +
    #     f"reg:{regionPens}"
    # )

    return not ( (n_ in rowPens) or (n_ in columnPens) or (n_ in regionPens) )

def solve():
    global board

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for n in range(1, 10):
                    if valid(r, c, n):
                        board[r][c] = n
                        if solve() == False:
                            board[r][c] = 0
                        else:
                            # I honestly don't get why this works:
                            solve()
                            return True
                            
                # One of the previous cells is wrong:
                return False
    

solve()

print("_ "*12)
for r in range(9):
    row = ""
    for c in range(9):
        if board[r][c] > 0:
            row += str(board[r][c]) + ' '
        else:
            row += "  "

        if (c + 1) % 3 == 0:
            row += "| "
    
    print(row)
    if (r + 1) % 3 == 0:
        print("_ "*12)

# correct = [
#     [8, 7, 5, 9, 2, 1, 3, 4, 6],
#     [3, 6, 1, 7, 5, 4, 8, 9, 2],
#     [2, 4, 9, 8, 6, 3, 7, 1, 5],
#     [5, 8, 4, 6, 9, 7, 1, 2, 3],
#     [7, 1, 3, 2, 4, 8, 6, 5, 9],
#     [9, 2, 6, 1, 3, 5, 4, 8, 7],
#     [6, 9, 7, 4, 1, 2, 5, 3, 8],
#     [1, 5, 8, 3, 7, 9, 2, 6, 4],
#     [4, 3, 2, 5, 8, 6, 9, 7, 1]
# ]

# if board == correct:
#     print("BOARD CORRECT")
# else:
#     print("BOARD NOT CORRECT")

# Check all of the rows are valid:
rowsValid = columnsValid = regionsValid = True
for row in range(9):
    rowPens = board[row]
    numberCounts = [ rowPens.count(i) for i in range(1, 10) ]
    if numberCounts != [1 for _ in range(9)]:
        rowsValid = False
        break

# Check all of the columns are valid:
for col in range(9):
    colPens = [board[i][col] for i in range(9)]
    numberCounts = [ colPens.count(i) for i in range(1, 10) ]
    if numberCounts != [1 for _ in range(9)]:
        columnsValid = False
        break

# Check all of the regions are valid:
for region in range(9):
    
    regionPens = [ board[r][c] for r, c in regionPositions[region] ]
    numberCounts = [ regionPens.count(i) for i in range(1, 10) ]
    if numberCounts != [1 for _ in range(9)]:
        regionsValid = False
        break

print(
    "SOLVE IS " +
    ("NOT " * int(not (columnsValid and rowsValid and regionsValid)) ) +
    "VALID"
)
