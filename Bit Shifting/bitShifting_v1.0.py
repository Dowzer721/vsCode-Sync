
import matplotlib.pyplot as plt

n = 16
# n = 15

state = (0b1 << n) | 0b1

# Put inside the for loop to see an output to the terminal:
# formatString = "{:0" + str(n+1) + "b}"
# print(formatString.format(state))

finalBits = []

for i in range(2 ** n):

    finalBit = state & 0b1
    finalBits.append(finalBit)
    
    state = ( ((state >> 0 & 0b1) ^ (state >> 1 & 0b1)) << n) | (state >> 1)
    # state = ( ((state >> 0 & 0b1) ^ (state >> 2 & 0b1)) << n) | (state >> 1)

img = []

for r in range(2 ** (n // 2)):
    row = []
    for c in range(2 ** (n // 2)):
        i = c + (r * 2 ** (n // 2))
        row.append(finalBits[i])
    img.append(row)

plt.imshow(img, "gray")
plt.show()