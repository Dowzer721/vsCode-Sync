
import pygame
pygame.display.init()

def displayGrid(pyGameScreen, Grid, screenColour=(255, 255, 255)):
    
    screenW = pyGameScreen.get_width()
    screenH = pyGameScreen.get_height()

    cols = len(Grid[0])
    rows = len(Grid)

    # while(True): # Removed while loop so changes could be made externally to grid, and a redraw would show said changes.
    pyGameScreen.fill(screenColour)

    for r in range(rows):
        for c in range(cols):
            Grid[r][c].displayCell(pyGameScreen, screenW, screenH)

    pygame.display.flip()