
from copy import deepcopy

columnCounts = [int(count) for count in list(input("Enter the counts along the top, without any gaps: "))]
numberOfColumns = len(columnCounts)

rowCounts = [int(count) for count in list(input("Enter the counts down the side, without any gaps: "))]
numberOfRows = len(rowCounts)

grid = [
    ['g', 'b', 'b', 't', 'b', 'g', 'g', 'b'], 
    ['b', 't', 'b', 'b', 't', 'b', 'b', 't'], 
    ['t', 'b', 'g', 'g', 'b', 'b', 't', 'b'], 
    ['b', 't', 'b', 'g', 'b', 't', 'b', 'b'], 
    ['g', 'b', 't', 'b', 'g', 'b', 'b', 't'], 
    ['b', 'g', 'b', 'g', 'b', 'g', 'g', 'b'], 
    ['t', 'b', 'g', 'b', 't', 'b', 'b', 't'], 
    ['b', 't', 'b', 'b', 't', 'b', 'g', 'b']
]

# grid = [[] for _ in range(numberOfRows)]

# print("\nEnter the values for each row, using the following legend:\nTree: 't'\nGrass: 'g'\nBlank: 'b'\nExample: gbbtbggb")
# for row in range(numberOfRows):
#     while len(grid[row]) != numberOfColumns:
#         grid[row] = list(input(f"Row {row}: "))

# # print(grid)
# while True:
#     print("\n")
#     for row in grid:
#         print(''.join(row) )

#     userInput = input("\nPlease confirm the grid is correct with 'y', otherwise enter the row to change: ")
#     if userInput == 'y': break

#     rowToChange = int(userInput)

#     print(f"Enter the new values for Row {rowToChange}")
#     grid[rowToChange] = list(input(f"Row {rowToChange}: "))

# print("Grid confirmed, solving....")


# If there are any columns or rows which have a count of zero, fill in the blanks as grass
# print(grid)
for c, count in enumerate(columnCounts):
    if count == 0:
        for r in range(numberOfRows):
            if grid[r][c] == 'b': grid[r][c] = 'g'
for r, count in enumerate(rowCounts):
    if count == 0:
        for c in range(numberOfColumns):
            if grid[r][c] == 'b': grid[r][c] = 'g'
# print(grid)



"""
This current method I've started is not solving it recursively, but instead with the method that I, the player, would play it. 

First off, I should check if there are any invalid columns/rows. I can do this by adding the number of placed tents with the number of 
blank spaces in each column/row, then comparing that number to the count for that column/row. 
If the calculated number is less than the count, it is an invalid column/row, otherwise continue. 
If invalid, backtrack one step, and restart. 
If valid, search for the next blank position and place a Tent.

Each time a Tent is placed, any surrounding NESW blanks are changed to grass too. 

Instead, I think that I should just search for the next blank spot, and place a tent, then set any surrounding (NESW) blanks to grass, 
then repeat. 

Then once 

"""

# def recursiveSolve(previousGrid):
    
#     currentGrid = deepcopy(previousGrid)

#     # Loop through each row
#     for row in range(numberOfRows):
#         # Loop through each column
#         for col in range(numberOfColumns):
            
#             # If the current position has anything other than a blank space, skip it
#             if currentGrid[row][col] != 'b': continue

#             # Get the current neighbours of the position
#             currentNeighbours = [
#                 currentGrid[row-1][col] if row > 0 else -1,
#                 currentGrid[row][col+1] if col < numberOfColumns-1 else -1,
#                 currentGrid[row+1][col] if row < numberOfRows-1 else -1,
#                 currentGrid[row][col-1] if col > 0 else -1
#             ]

#             # If there are no trees around the current spot, set it as grass
#             if currentNeighbours.count('t') == 0:
#                 currentGrid[row][col] = 'g'
