
from math import pi, cos, sin, atan2
import os
import pygame
from random import randint
import tkinter as tk

import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

windowWidth, windowHeight = 700, 500
window = tk.Tk()
window.title("TK Boids v1.0")
window.minsize(windowWidth, windowHeight)

canvasWidth, canvasHeight = int(windowWidth * 0.75), windowHeight
# canvasFrame = tk.Frame(window, width=windowWidth, height=windowHeight)
canvasFrame = tk.Frame(window, width=canvasWidth, height=canvasHeight)
canvasFrame.grid(column=0, row=0)
# canvasFrame.pack(side = tk.LEFT)
window.update()

os.environ["SDL_WINDOWID"] = str(canvasFrame.winfo_id())
os.environ["SDL_VIDEODRIVER"] = "windib"

pygame.display.init()
# canvasWidth, canvasHeight = int(windowWidth * 0.75), windowHeight
canvas = pygame.display.set_mode((canvasWidth, canvasHeight))
pygame.display.flip()

# def randomFloat(mn=0.0, mx=1.0, dP=2):
#     rng = mx - mn
#     pct = randint(0, 10**dP) / float(10**dP)
#     return round(mn + (rng * pct), dP)

# boidCount = 1
# boidRadius = 10

# class Boid:
#     def __init__(self, id_):
#         self.id = id_

#         x = randint(int(canvasWidth * 0.25), int(canvasWidth * 0.75))
#         y = randint(int(canvasHeight * 0.25), int(canvasHeight * 0.75))
#         self.position = LL.Vector(x, y)

#         self.velocity = LL.Vector().fromAngle(
#             randomFloat(0.0, pi * 2.0, 3)
#         )
    
#     def render(self, renderColour=(0,0,0), thickness=1):
#         x1, y1, _ = self.position.toInt()
#         pygame.draw.circle(
#             canvas, renderColour,
#             (x1, y1), boidRadius,
#             thickness
#         )

#         if thickness > 0:
#             dir = self.velocity.heading()
#             x2 = x1 + (cos(dir) * boidRadius)
#             y2 = y1 + (sin(dir) * boidRadius)
#             pygame.draw.line(
#                 canvas, renderColour,
#                 (x1, y1), (x2, y2),
#                 thickness
#             )

# boids = [Boid(i) for i in range(boidCount)]


while True:
    canvas.fill((200, 200, 200))
    
    # for b in boids:
    #     b.render()

    pygame.display.flip()
    window.update()


# canvasWidth, canvasHeight = int(windowWidth * 0.6), int(windowHeight * 0.8)
# canvasFrame = tk.Frame(window, width=canvasWidth, height=canvasHeight)
# canvasFrame.grid(column=0, row=0)

# pygame.display.init()

# canvas = pygame.display.set_mode((canvasWidth, canvasHeight))
# canvas.fill((255, 0, 0))

# pygame.display.update()





# window.mainloop()

# # import sys
# # sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# # import LukeLibrary as LL

# # from math import pi, cos, sin

# # import tkinter as tk
# from tkinter import *

# # from random import randint
# import random
# # def rF(mn, mx, dP=3): # max, min, decimalPlaces
# #     rng = mx - mn 
# #     pct = randint(0, 10**dP) / float(10**dP)
# #     return round(mn + (rng * pct), dP)

# import pygame
# import os

# windowWidth, windowHeight = 700, 500

# root = Tk()
# root.title("Boids v1.0")
# root.minsize(windowWidth, windowHeight)

# canvasW, canvasH = int(windowWidth * 0.75), int(windowHeight * 0.5)

# # embed = Frame(root, width=640, height=480)
# # # pygameFrame.grid(columnspan = canvasW, rowspan = canvasH)
# # embed.grid(row=0, column=2)
# # # pygameFrame.pack(side = LEFT)
# # root.update()

# window = Frame(root, width=windowWidth, height=windowHeight)
# window.grid(row=0, column=0)
# root.update()

# # canvasW, canvasH = 
# # pygameFrame = Frame(root, width=640, height=480)
# # pygameFrame.grid(row=0, column=0)
# # root.update()

# # interactFrame = Frame(window, width = windowWidth-canvasW, height = windowHeight)
# # interactFrame.pack(side = RIGHT)

# # print(
# #     f"windowWidth: {windowWidth}, windowHeight: {windowHeight} \n" +
# #     f"canvasWidth: {canvasW}, canvasHeight: {canvasH} \n" +
# #     f"interactWidth: {windowWidth-canvasW}, interactHeight: {windowHeight} \n"
# # )

# # root.update()
# os.environ["SDL_WINDOWID"] = str(window.winfo_id())
# os.environ["SDL_VIDEODRIVER"] = 'windib'

# pygame.display.init()
# screen = pygame.display.set_mode((canvasW, canvasH))#, pygame.NOFRAME)
# # canvas.fill(pygame.Color(255, 255, 255))
# # pygame.display.flip()

# # pygame.display.update()
# # root.update()

# # boidCount = 1
# # boidRadius = 10
# # attractionSettings = [0.1, boidRadius * 1.5]
# # repulsionSettings = [1.0, boidRadius * 1.25]
# # matchingSettings = [0.0, boidRadius * 2.0]

# # embed = tk.Frame(root, width = 500, height = 500)
# # embed.grid(columnspan = (500), rowspan = 500)
# # embed.pack(side = LEFT)
# # buttonwin = tk.Frame(root, width = 75, height = 500)
# # buttonwin.pack(side = LEFT)


# # class Boid:
# #     def __init__(self, id_):
# #         self.id = id_

# #         self.position = LL.Vector(
# #             randint(int(canvasW*0.1), int(canvasW*0.9)), 
# #             randint(int(canvasH*0.1), int(canvasH*0.9))
# #         )
# #         self.velocity = LL.Vector().fromAngle(
# #             rF(0.0, pi * 2.0)
# #         )

# #     def render(self, renderColour=(0,0,0), thickness=1):
# #         x1, y1, _ = self.position.toInt()
# #         pygame.draw.circle(
# #             canvas, renderColour,
# #             (x1, y1), boidRadius, 1
# #         )
# #         dir = self.velocity.heading()
# #         x2 = x1 + (cos(dir) * boidRadius)
# #         y2 = y1 + (sin(dir) * boidRadius)
# #         pygame.draw.line(
# #             canvas, renderColour,
# #             (x1, y1), (x2, y2),
# #             thickness
# #         )
# # boids = [Boid(i) for i in range(boidCount)]

# while True:
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     screen.fill((r, g, b))

#     # for b in boids:
#     #     b.render()

#     # pygame.display.update()
#     pygame.display.flip()
#     root.update()
    
    
#     # try:
#     #     root.update()
#     # except:
#     #     break

# # attLabel = Label(root, text = "ATT: " + str(attractionMultiplier))
# # repLabel = Label(root, text = "REP: " + str(repulsionMultiplier))
# # matLabel = Label(root, text = "MAT: " + str(matchingMultiplier))

# # attLabel.grid(column = 0, row = 0)
# # repLabel.grid(column = 0, row = 1)
# # matLabel.grid(column = 0, row = 2)

# # attTextVar = tk.StringVar()
# # repTextVar = tk.StringVar()
# # matTextVar = tk.StringVar()

# # def changeAttractionMultiplier():
# #     global attractionMultiplier
# #     attractionMultiplier = attEntry.get()
# #     attLabel.configure(text = "ATT: " + str(attractionMultiplier))


# # def changeRepulsionMultiplier():
# #     global repulsionMultiplier
# #     repulsionMultiplier = repEntry.get()
# #     repLabel.configure(text = "REP: " + str(repulsionMultiplier))

# # def changeMatchingMultiplier():
# #     global matchingMultiplier
# #     matchingMultiplier = matEntry.get()
# #     matLabel.configure(text = "MAT: " + str(matchingMultiplier))

# # def confirmValues():
# #     print(
# #         f"ATT: {attractionMultiplier} \n" + 
# #         f"REP: {repulsionMultiplier} \n" + 
# #         f"MAT: {matchingMultiplier} \n"
# #     )

# # def resetValues():
# #     global attractionMultiplier, repulsionMultiplier, matchingMultiplier
# #     attractionMultiplier = 0.1
# #     repulsionMultiplier = 1.0
# #     matchingMultiplier = 0.05

# #     attLabel.configure(text = "ATT: " + str(attractionMultiplier))
# #     repLabel.configure(text = "REP: " + str(repulsionMultiplier))
# #     matLabel.configure(text = "MAT: " + str(matchingMultiplier))

# #     attEntry.delete(0, "end")
# #     repEntry.delete(0, "end")
# #     matEntry.delete(0, "end")

# #     confirmValues()

# # attEntry = ttk.Entry(root, width = 15, textvariable = attTextVar)
# # repEntry = ttk.Entry(root, width = 15, textvariable = repTextVar)
# # matEntry = ttk.Entry(root, width = 15, textvariable = matTextVar)

# # attEntry.grid(column = 0, row = 5)
# # repEntry.grid(column = 0, row = 6)
# # matEntry.grid(column = 0, row = 7)

# # # attSetButton = ttk.Button(root, text = "Set ATT", command = changeAttractionMultiplier)
# # # attSetButton.grid(column = 1, row = 5)

# # # repSetButton = ttk.Button(root, text = "Set REP", command = changeRepulsionMultiplier)
# # # repSetButton.grid(column = 1, row = 6)

# # # matSetButton = ttk.Button(root, text = "Set MAT", command = changeMatchingMultiplier)
# # # matSetButton.grid(column = 1, row = 7)

# # # confirmButton = ttk.Button(root, text = "Confirm", command = confirmValues)
# # # confirmButton.grid(column = 0, row = 10)

# # # resetButton = ttk.Button(root, text = "Reset Values", command = resetValues)
# # # resetButton.grid(column = 0, row = 11)

# # buttons = {
# #     "attractionSet": ttk.Button(root, text = "Set ATT", command = changeAttractionMultiplier),
# #     "repulsionSet": ttk.Button(root, text = "Set REP", command = changeRepulsionMultiplier),
# #     "matchSet": ttk.Button(root, text = "Set MAT", command = changeMatchingMultiplier),
# #     "confirm": ttk.Button(root, text = "Confirm", command = confirmValues),
# #     "reset": ttk.Button(root, text = "Reset Values", command = resetValues)
# # }

# # buttons["attractionSet"].grid(column = 1, row = 5)
# # buttons["repulsionSet"].grid(column = 1, row = 6)
# # buttons["matchSet"].grid(column = 1, row = 7)

# # buttons["confirm"].grid(column = 0, row = 10)
# # buttons["reset"].grid(column = 0, row = 11)




# # root.mainloop()