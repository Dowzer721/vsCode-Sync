
"""
I would instead like to perform the same tests that a human does to solve the puzzle, but implementing these tests in code has so far been challenging. I wonder if implementing the ability to "pencil" in numbers into the cells would be helpful...
---
I have now implemented the same basic tests as a human would do, using the ability to "pencil" in numbers into each cell. 
Currently, each cell has a list of pencil numbers, which get removed if they appear in the adjacent column/row/segment, and then if there is only one pencil number remaining, it is set as the Penned number.

This works, but next, I would like to begin checking for single occurrences of each Pencilled number within each column/row/segment, and then setting the Pen number to that single occurrence.

"""


Pens = [
  [4,3,0,0],
  [1,2,3,0],
  [0,0,2,0],
  [2,1,0,0]
]

# Pens = [
#   [9,0,0,2,0,0,0,0,0],
#   [0,0,0,8,4,0,2,6,0],
#   [0,0,7,0,0,3,0,5,0],
#   [0,3,0,0,0,7,6,0,0],
#   [0,0,4,0,0,0,0,0,9],
#   [0,0,0,0,0,0,0,2,4],
#   [0,9,0,0,6,0,8,0,0],
#   [0,5,0,7,0,0,0,4,0],
#   [0,0,0,0,0,8,3,0,0]
# ]

gridSize = len(Pens[0])

segmentSize = int(gridSize ** 0.5)
# print(segmentSize)

Pencils = []
for r in range(gridSize):
  PencilRow = []
  for c in range(gridSize):
    PencilRow.append([i for i in range(1, gridSize+1)])
  Pencils.append(PencilRow)

def printPens():
  print(" ", end='')
  for _ in range(segmentSize):
    print("_"*((segmentSize*2)+1), end=' ')
  print()
  
  for r in range(gridSize):
    print("|", end='')
    digitGap = ' '
    if r % segmentSize == segmentSize-1: digitGap = '_'
    
    for segmentColumn in range(segmentSize):
      startCol = segmentColumn*segmentSize
      endCol = (segmentColumn+1)*segmentSize
      print(digitGap + digitGap.join([str(n) for n in Pens[r][startCol:endCol]]) + digitGap, end='')
      if endCol % segmentSize == 0: print('|', end='')
      if endCol % (segmentSize**2) == 0: print()
  
  print()
  print()


def flatten(list_):
  flat = []
  for row in list_:
    flat.extend(row)
  return flat

def getRow(r):
  return Pens[r]

def getCol(c):
  return [Pens[r][c] for r in range(gridSize)]

def getSeg(r,c):
  # If the grid is divided into segments, which column is the segment in?
  segmentColumn = int(c / segmentSize)
  
  # If the grid is divided into segments, which row is the segment in?
  segmentRow = int(r / segmentSize)
  
  # return (segmentColumn, segmentRow)
  
  startColumn = segmentColumn * segmentSize
  endColumn = (segmentColumn+1) * segmentSize
  
  startRow = segmentRow * segmentSize
  endRow = (segmentRow+1) * segmentSize
  
  Segment = []
  for row in range(startRow, endRow):
    Segment.append(Pens[row][startColumn:endColumn])
  
  Segment = flatten(Segment)
  
  return Segment

def updatePencils(r, c):
  if Pens[r][c] > 0: 
    Pencils[r][c] = [0 for _ in range(gridSize)]
    return
  
  Row = getRow(r)
  Col = getCol(c)
  Seg = getSeg(r, c)

  for i in range(1, gridSize+1):
    if (i in Row) or (i in Col) or (i in Seg):
      Pencils[r][c][i-1] = 0




print("Starting Grid:")
printPens()
# for Row in Pencils:
#   print(Row)
# print()

# How many penned numbers need to be written into the grid:
PensToWrite = sum([Row.count(0) for Row in Pens])

for _ in range(PensToWrite):
  
  for r in range(gridSize):
    for c in range(gridSize):
      updatePencils(r, c)
      if Pencils[r][c].count(0) == (gridSize-1):
        Pens[r][c] = [v for v in Pencils[r][c] if v > 0][0]
    

print("Final Grid:")
printPens()

# for Row in Pencils:
#   print(Row)
# print()









