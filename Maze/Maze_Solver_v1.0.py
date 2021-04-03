
import pygame
pygame.display.init()

import Maze_Generator_v1_0 as Gen
import Maze_Display as Disp

screenW = 500
screenH = 500
screen = pygame.display.set_mode((screenW, screenH))

cols = 6
rows = 8
Grid = Gen.generateMaze(cols, rows)

while(True):
    Disp.displayGrid(screen, Grid)

