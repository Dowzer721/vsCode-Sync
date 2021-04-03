
import math
import random
import matplotlib.pyplot as plt

def Matrix(cols, rows):
    mat = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            pixel = []
            # val = random.randint(0, 1000) / 1000.0
            for _ in range(3):
                # pixel.append(val)
                pixel.append(0)
            row.append(pixel)
        mat.append(row)

    return mat

def diag(matrix, start=0, step=1):

    rows = len(matrix)
    cols = len(matrix[0])

    i = start
    for n in range(min(cols, rows)):
        matrix[n][n] = []
        for _ in range(3):
            matrix[n][n].append(i)
        i += step

def matrixMaximum(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    maxVal = 0
    for r in range(rows):
        for c in range(cols):
            maxVal = max(maxVal, matrix[r][c][0])
    
    return maxVal



    

mat = Matrix(50, 50)
# print(mat)
# print("\n\n")

diag(mat, 1, 2)
# print(mat)

matMax = matrixMaximum(mat)
rows = len(mat)
cols = len(mat[0])
for r in range(rows):
    for c in range(cols):
        val = mat[r][c][0]
        mat[r][c] = []
        for _ in range(3):
            mat[r][c].append(val / matMax)

plt.imshow(mat)
plt.show()