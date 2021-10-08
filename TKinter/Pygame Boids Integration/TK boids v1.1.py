
from math import pi, cos, sin, atan2
import os
import pygame
from random import randint
import tkinter as tk
from tkinter import *

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

window = tk.Tk()
windowWidth, windowHeight = 500, 500
window.minsize(windowWidth, windowHeight)
window.title("TK boids v1.1")

pygameCanvasWidth, pygameCanvasHeight = int(windowWidth * 0.5), int(windowHeight * 0.9)

# pygameFrame = tk.Frame(window, width = 500, height = 500) #creates pygameFrame frame for pygame window
# pygameFrame.grid(columnspan = (600), rowspan = 500) # Adds grid

pygameFrame = tk.Frame(window, width = pygameCanvasWidth, height = pygameCanvasHeight)
pygameFrame.grid(columnspan = int(pygameCanvasWidth * 1.2), rowspan = pygameCanvasHeight)

pygameFrame.pack(side = LEFT) #packs window to the left


buttonFrameWidth = windowWidth - pygameCanvasWidth
buttonFrameHeight= windowHeight
buttonFrame = tk.Frame(window, width = buttonFrameWidth, height = buttonFrameHeight)
buttonFrame.pack(side = LEFT)

os.environ['SDL_WINDOWID'] = str(pygameFrame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

canvas = pygame.display.set_mode((pygameCanvasWidth, pygameCanvasHeight))
canvas.fill(pygame.Color(255,255,255))
pygame.display.init()
pygame.display.update()

# boidRadius = 10
# boidCount = 1
# class Boid:
#     def __init__(self, id_):
#         self.id = id_

#         self.position = LL.Vector(
#             pygameCanvasWidth * 0.4,
#             pygameCanvasHeight* 0.5
#         )

#         self.velocity = LL.Vector().fromAngle(
#             LL.randomFloat(0.0, pi * 2.0, 3)
#         )
    
#     def render(self, renderColour=(0,0,0), renderThickness=1):
#         x1, y1, _ = self.position.toInt()
#         pygame.draw.circle(
#             canvas, renderColour,
#             (x1, y1), 10,
#             renderThickness
#         )

#         if renderThickness > 0:
#             dir = self.velocity.heading()
#             x2 = x1 + (cos(dir) * boidRadius)
#             y2 = y1 + (sin(dir) * boidRadius)
#             pygame.draw.line(
#                 canvas, renderColour,
#                 (x1, y1), (x2, y2),
#                 renderThickness
#             )
# boids = [Boid(i) for i in range(boidCount)]

global x, y
x, y = pygameCanvasWidth // 2, pygameCanvasHeight // 2

def draw():
    # pass
    
    # for b in boids:
    #     b.render()

    global x, y
    x = (x + 3) % pygameCanvasWidth
    y = (y + 2) % pygameCanvasHeight

    r = min([
        x,
        pygameCanvasWidth - x,
        y,
        pygameCanvasHeight - y
    ])

    canvas.fill(pygame.Color(255,255,255))
    pygame.draw.circle(
        canvas, 
        (0,0,0), 
        (int(x), int(y)), 
        int(r)
    )
    pygame.display.update()

    # print(x, y)

drawButton = Button(buttonFrame,text = 'Draw',  command=draw)
drawButton.pack(side=LEFT)
window.update()

while True:
    draw()
    pygame.display.update()
    window.update()

# window.mainloop()