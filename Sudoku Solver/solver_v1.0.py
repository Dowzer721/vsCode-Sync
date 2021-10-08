
# BOARD
#               COLUMNS
#o---o---o---o---o---o---o---o---o---o
#CELL|   |   |   |   |   |   |   |   |
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |  REGION   |   |   |   |
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |   |   |   |   |   |   |
#o---o---o---o---o---o---o---o---o---o
#|   |   |   |   |   |   |   |   |   |
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |   |   |   |   |   |   | ROWS
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |   |   |   |   |   |   |
#o---o---o---o---o---o---o---o---o---o
#|   |   |   |   |   |   |   |   |   |
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |   |   |   |   |   |   |
#o---+---+---o---+---+---o---+---+---o
#|   |   |   |   |   |   |   |   |   |
#o---o---o---o---o---o---o---o---o---o




from os import system
from time import time

# def delay(secs):
#     now = time()
#     while (now + secs) > time():
#         pass


cellPenValues = [
    [0, 7, 0, 0, 2, 0, 0, 4, 6], 
    [0, 6, 0, 0, 0, 0, 8, 9, 0], 
    [2, 0, 0, 8, 0, 0, 7, 1, 5], 
    [0, 8, 4, 0, 9, 7, 0, 0, 0], 
    [7, 1, 0, 0, 0, 0, 0, 5, 9], 
    [0, 0, 0, 1, 3, 0, 4, 8, 0], 
    [6, 9, 7, 0, 0, 2, 0, 0, 8], 
    [0, 5, 8, 0, 0, 0, 0, 6, 0], 
    [4, 3, 0, 0, 8, 0, 0, 7, 0]
]
# regionValues = [
#     [70, 20, 46],
#     [60, 0, 890],
#     [200, 800, 715],
#     [84, 97, 0],
#     [710, 0, 59],
#     [0, 130, 480],
#     [697, 2, 8],
#     [58, 0, 60],
#     [430, 80, 70]
# ]


# # Convert 'regionValues' from integers to individual cell values:
# cellPenValues = []
# for row in regionValues:
#     rowValues = []
#     for val in row:
#         if val == 0: 
#             rowValues.extend([0, 0, 0])
#         elif val < 10: 
#             rowValues.extend( [0, 0, val] )
#         elif val < 100:
#             rowValues.extend( [0] + [int(n) for n in list(str(val))] )
#         else:
#             rowValues.extend( [int(n) for n in list(str(val))] )
    
#     cellPenValues.append(rowValues)

cellPencilValues = []
for r in range(9):
    row = []
    for c in range(9):
        if cellPenValues[r][c] == 0: 
            row.append([i for i in range(9)])
        else:
            row.append([])
    
    cellPencilValues.append(row)

# print(cellPenValues)
# print(cellPencilValues)
        





board = []
class Cell:
    def __init__(self, _column, _row, _value=0):
        self.pen = _value
        self.pencil = [_value for _ in range(9)]

        self.col = _column
        self.row = _row
        self.region = (int(_column / 3) * 3) + (int(_row / 3) * 3)
    
    def setPencils(self):

        columnPens = []
        for r in range(9):
            columnPens.append(cellPenValues[r][self.col])
            # try: columnPens.remove(0) 
            # except Exception: pass

        # rowPens = []
        # for c in range(9):
        #     rowPens.append(cellPenValues[self.row][c])
            # try: rowPens.remove(0)
            # except Exception: pass
        rowPens = cellPenValues[self.row]
        
        # regionPens = []
        # for r in range(9):
        #     for c in range(9):
        #         if (c==self.col) and (r==self.row): continue
        #         i = c + (r * 9)
        #         if board[i].region != self.region: continue
        #         regionPens.append()

        for i in range(1, 10):
            if (i in columnPens) or (i in rowPens): # or (i in regionPens): 
                self.pencil[i-1] = 0



for r in range(9):
    for c in range(9):
        board.append(Cell(c, r, cellPenValues[r][c]))

def boardComplete():
    pennedNumbersCount = sum([ int(cell.pen > 0) for cell in board ])
    return pennedNumbersCount == (9 * 9)

startTime = time()
conceedTime = 5
conceeded = False

while (not boardComplete()) and (not conceeded):

    if (startTime + conceedTime) <= time():
        conceeded = True
        continue

    for cell in board:
        cell.setPencils()
    
    for cell in board:
        if cell.pencil.count(0) == 8:
            a = [cell.pencil[i] > 0 for i in range(9)]
            cell.pen = a.index(True) + 1
            cellPenValues[cell.row][cell.col] = a.index(True) + 1

print(cellPenValues)
    



