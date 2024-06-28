
"""
This doesn't currently work, because I am not sure how I actually want to go about testing each cell. 
But I have written the functions to allow for extracting a given column/row/segment from the Grid.

I don't think that it is a good idea to simply check the validity of every column/row/segment for 
each value tested in every empty cell, as I fear this will take ages. 

I would instead like to perform the same tests that a human does to solve the puzzle, but implementing 
these test in code has so far been challenging. I wonder if implementing the ability to "pencil" in 
numbers into the cells would be helpful...

"""

# Grid = [
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

Grid = [
  [4,3,0,0],
  [1,2,3,0],
  [0,0,2,0],
  [2,1,0,0]
]

colCount = rowCount = len(Grid[0])
print(f"c:{colCount}, r:{rowCount}")

segmentSize = int(colCount ** 0.5)
print(segmentSize)

def printGrid():
  print(" ", end='')
  for _ in range(segmentSize):
    print("_"*((segmentSize*2)+1), end=' ')
  print()
  
  for r in range(rowCount):
    print("|", end='')
    digitGap = ' '
    if r % segmentSize == segmentSize-1: digitGap = '_'
    
    for segmentColumn in range(segmentSize):
      startCol = segmentColumn*segmentSize
      endCol = (segmentColumn+1)*segmentSize
      print(digitGap + digitGap.join([str(n) for n in Grid[r][startCol:endCol]]) + digitGap, end='')
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
  return Grid[r]

def getCol(c):
  return [Grid[r][c] for r in range(rowCount)]

def getSegment(c,r):
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
    Segment.append(Grid[row][startColumn:endColumn])
  
  Segment = flatten(Segment)
  
  return Segment

seg = getSegment(0,0)
# segflat = [row for row in seg]
# segflat = flatten(seg)

print(seg)

def segmentValid(Segment):
  if Segment.count(0) > 0: return False

def rowValid(Row):
  ValueCounts = [Row.count(i) for i in range(1, colCount+1)]
  for Count in ValueCounts:
    if Count > 1: return False

def colValid(Column):
  ValueCounts = [Column.count(i) for i in range(1, rowCount+1)]
  for Count in ValueCounts:
    if Count > 1: return False

for r in range(rowCount):
  rowCopy = [v for v in getRow(r)]
  for c in range(colCount):
    colCopy = [v for v in getCol(c)]
    segmentCopy = [v for v in getSegment(c, r)]
    originalValue = Grid[r][c]
    for i in range(1, colCount+1):
      
      rowCopy[c] = i
      colCopy[r] = i
      segmentCopy[c + (r*segmentSize)] = i
      
      rv = rowValid(rowCopy)
      cv = colValid(colCopy)
      sv = segmentValid(segmentCopy)
      
      if (rv and cv and sv): continue
      
      rowCopy[c] = originalValue
      colCopy[r] = originalValue
      segmentCopy[c + (r*segmentSize)] = originalValue
      
    print(rowCopy)
