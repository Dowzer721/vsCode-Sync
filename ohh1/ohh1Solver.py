
"""
This is currently working, though I am yet to implement:
	findMatchingRowOrCol('c', ...)

Once this is implemented, I believe it will work for any size puzzle.

I would also like to alter the method of inputting the puzzle, as it is quite slow and easy to make mistakes.
"""

import os, time

knownValues = [
    "r-------r-b-",
    "--bb---b-rr-",
    "------------",
    "---b--r-bb--",
    "---bb-------",
    "--r---------",
    "-----r-r---r",
    "--------b---",
    "---b--r---rb",
    "b-b-b-r-----",
    "--b-------bb",
    "---r--bb-r--"
]

# knownValues = [
#     "-----r-----r",
#     "-bb----r----",
#     "-b-r--b---b-",
#     "-----rb-----",
#     "b--r--------",
#     "---r-r-r-b--",
#     "-r----b--b--",
#     "--b-bb------",
#     "-r----b----b",
#     "r---b----r--",
#     "b--r--------",
#     "----b-r-r--r"
# ]

# knownValues = [
#     "---r------------",
#     "b----r-----rr--r",
#     "b-r-b-r---------",
#     "------r---rr----",
#     "-r------r--r-r-b",
#     "b-b-------b-----",
#     "---------------r",
#     "--r-r----------r",
#     "----------------",
#     "--r--b--r--r----",
#     "--r----b----b---",
#     "---------b--b--b",
#     "b--b--b----r--r-",
#     "--r-r------r----",
#     "-----b-r----rr--",
#     "r-r---r--b------"
# ]

gridSize = len(knownValues) # int(input("Enter size of grid (4, 6, 8, 10, 12): "))

grid = [
	[' ' if val == '-' else val for val in row]
	for row in knownValues
]

# for row in range(gridSize):
# 	#knownValues = ''
# #	while len(knownValues) < gridSize:
# #		knownValues = input(f"Enter any known values for row {row}: ")
# 	for col in range(gridSize):
# 		#if knownValues[col] == 'r' or knownValues[col] == 'b':
# #			grid[row][col] = knownValues[col]
# 		if knownValues[row][col] == 'r' or knownValues[row][col] == 'b':
# 			grid[row][col] = knownValues[row][col]

def delay(secs):
	start = time.time()
	while start + secs > time.time(): pass
	

def showGrid():
	
	print(' ' + ' '.join(str(i) for i in range(gridSize)))
	print(' ' + ("_ "*gridSize))
	
	for r in grid:
		print('|' + ' '.join(r) + " -" + str(grid.index(r)) )

# showGrid()

def neighbourValues(row_, col_):
	return [
		' ' if row_ == 0 else grid[row_-1][col_],
		' ' if col_ == gridSize-1 else grid[row_][col_+1],
		' ' if row_ == gridSize-1 else grid[row_+1][col_],
		' ' if col_ == 0 else grid[row_][col_-1]
	]
	#print(f"{row_},{col_}: {values}")
	#return values

def solveCellExtensions(row_, col_):#, grid_):
	# At grid[row_][col_], look at neighbours, and solve any empty spaces if possible.
	
    currentCellValue = grid[row_][col_]
    if currentCellValue == ' ': return False
	
    oppositeCellValue = 'r' if currentCellValue == 'b' else 'b'

	# directions:
		# up 0
		# right 1
		# down 2
		# left 3
		
    neighbours = neighbourValues(row_, col_)
	
    if row_ > 1:
        #print(f"r{row_} > 1")
        if currentCellValue == neighbours[0]:
            if neighbourValues(row_-1, col_)[0] == ' ':
                grid[row_ -2][col_] = oppositeCellValue

    if col_ < gridSize - 2:
        #print(f"c{col_} < {gridSize - 2}")
        if currentCellValue == neighbours[1]:
            if neighbourValues(row_, col_+1)[1] == ' ':
                grid[row_][col_ +2] = oppositeCellValue

    if row_ < gridSize - 2:
        #print(f"r{row_} < {gridSize - 2}")
        if currentCellValue == neighbours[2]:
            if neighbourValues(row_+1, col_)[2] == ' ':
                grid[row_+2][col_] = oppositeCellValue

    if col_ > 1:
        #print(f"c{col_} > 1")
        if currentCellValue == neighbours[3]:
            if neighbourValues(row_, col_-1)[3] == ' ':
                grid[row_][col_ -2] = oppositeCellValue

def fillLineWithOppositeColour(rowOrCol, index):
	# rowOrCol = 'r' or 'c'
	
	if rowOrCol == 'r':
		currentRow = grid[index]
		valueCount = (
			sum(int(v == 'r') for v in currentRow),
			sum(int(v == 'b') for v in currentRow)
		)
		#print(valueCount)
		
		if valueCount[0] == gridSize//2:
			for c in range(gridSize):
				if grid[index][c] == ' ':
					grid[index][c] = 'b'
			return True
		if valueCount[1] == gridSize//2:
			for c in range(gridSize):
				if grid[index][c] == ' ':
					grid[index][c] = 'r'
			return True
	
	if rowOrCol == 'c':
		currentCol = [grid[r][index] for r in range(gridSize)]
		valueCount = (
			sum(int(v == 'r') for v in currentCol),
			sum(int(v == 'b') for v in currentCol)
		)
		
		if valueCount[0] == gridSize//2:
			for r in range(gridSize):
				if grid[r][index] == ' ':
					grid[r][index] = 'b'
			return True
		if valueCount[1] == gridSize//2:
			for r in range(gridSize):
				if grid[r][index] == ' ':
					grid[r][index] = 'r'
			return True
	
	return False

def solveNeighbourGaps(row_, col_):
	# This solves the following scenario:
	# R _ R -> R B R
	
	if grid[row_][col_] != ' ': return False
	
	neighbours = neighbourValues(row_, col_)
	
	if neighbours[0] != ' ' and neighbours[2] != ' ' and neighbours[0] == neighbours[2]:
		grid[row_][col_] = 'r' if neighbours[0] == 'b' else 'b'
		return True
	
	if neighbours[1] != ' ' and neighbours[3] != ' ' and neighbours[1] == neighbours[3]:
		grid[row_][col_] = 'r' if neighbours[1] == 'b' else 'b'
		return True
	
	return False

def findMatchingRowOrCol(rowOrCol, currentIndex):
	if rowOrCol == 'r':
		currentRow = grid[currentIndex]
		valueCount = sum(
			int(v != ' ') for v in currentRow
		)
		# This solve is only possible with 2 missing values:
		if valueCount != gridSize - 2: 
			#input('a')
			return False
		
		for r in range(gridSize):
			if currentIndex == r: continue
			
			otherRow = grid[r]
			otherValueCount = sum(
				int(v != ' ') for v in otherRow
			)
			
			# Solve is only possible if other row is complete:
			if otherValueCount < gridSize: 
				#input(f"b: {r} {otherValueCount}")
				continue
				#return False
			
			# Next we check if the filled values in currentRow match those in otherRow:
			
			matchingValueCount = 0
			for c in range(gridSize):
				if currentRow[c] == ' ': continue
				matchingValueCount += int(currentRow[c] == otherRow[c])
			
			if matchingValueCount != gridSize - 2: continue
			
			# Finally we place 'r' and 'b' into currentRow in opposite places to otherRow:
			
			currentRowEmptySpaces = [i for i,val in enumerate(currentRow) if val==' ']
			if len(currentRowEmptySpaces) < 2: continue
			
			grid[currentIndex][currentRowEmptySpaces[0]] = 'b' if otherRow[currentRowEmptySpaces[0]] == 'r' else 'r'
			
			grid[currentIndex][currentRowEmptySpaces[1]] = 'b' if otherRow[currentRowEmptySpaces[1]] == 'r' else 'r'
			
			# input(f"switching")

	elif rowOrCol == 'c':
		currentCol = [grid[r][currentIndex] for r in range(gridSize)]
		valueCount = sum(
			int(v != ' ') for v in currentCol
		)
		if valueCount != gridSize - 2: return False
		
		for c in range(gridSize):
			if currentIndex == c: continue
			
			otherCol = [grid[r][c] for r in range(gridSize)]
			otherValueCount = sum(
				int(v != ' ') for v in otherCol
			)
			
			# Solve is only possible if other row is complete:
			if otherValueCount < gridSize: 
				#input(f"b: {r} {otherValueCount}")
				continue
				#return False
			
			# Next we check if the filled values in currentCol match those in otherCol:
			
			matchingValueCount = 0
			for r in range(gridSize):
				if currentCol[r] == ' ': continue
				matchingValueCount += int(currentCol[r] == otherCol[r])
			
			if matchingValueCount != gridSize - 2: continue
			
			currentColEmptySpaces = [i for i,val in enumerate(currentCol) if val == ' ']
			
			grid[currentColEmptySpaces[0]][currentIndex] = 'b' if otherCol[currentColEmptySpaces[0]] == 'r' else 'r'
			
			grid[currentColEmptySpaces[1]][currentIndex] = 'b' if otherCol[currentColEmptySpaces[1]] == 'r' else 'r'
			
	

# fillLineWithOppositeColour('r', 0)
# input()

def allCellsFilled():
	total = 0
	for r in range(gridSize):
		for c in range(gridSize):
			total += int(grid[r][c] != ' ')
	
	return total == (gridSize * gridSize)


while allCellsFilled() == False:
	for r in range(gridSize):
		fillLineWithOppositeColour('r', r)
		findMatchingRowOrCol('r', r)
		for c in range(gridSize):
			fillLineWithOppositeColour('c', c)
			findMatchingRowOrCol('c', c)
			
			solveCellExtensions(r, c)
			solveNeighbourGaps(r, c)
	
	# print()
	# showGrid()
	
	# delay(1)
	# os.system("clear")
			
	
print("All cells filled: ")
showGrid()





#for r in range(gridSize):
#	for c in range(gridSize):
#		neighbourValues(r, c)