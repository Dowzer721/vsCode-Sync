
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
# import LukeLibrary as LL
from LukeLibrary import colours
WHITE = colours["WHITE"]
BLACK = colours["BLACK"]
GREY = colours["LIGHT_GREY"]
RED = colours["RED"]

import pygame
# pygame.init()

# from event import *
# from path import *
# from vehicle import *
import event, path, vehicle

canvasW, canvasH = 600, 400
canvas = pygame.display.set_mode((canvasW, canvasH))

path.setVertices(canvas)

vehicle.vehiclePosition = [int(path.vertices[0][0]), int(path.vertices[0][1])]

while True:
    event.checkEvents()
    canvas.fill(WHITE)

    path.renderPath(canvas, GREY, RED, 16)
    vehicle.renderVehicle(canvas, BLACK)

    pygame.display.update()