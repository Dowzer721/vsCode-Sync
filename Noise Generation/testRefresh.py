
import matplotlib.pyplot as plt
import random

resolution = 64
w, h = [resolution] * 2

for i in range(50):
    grid = [[i*c*r for c in range(w)] for r in range(h)]
    plt.plot(grid)
    plt.draw()
    plt.pause(0.1)
    plt.clf()