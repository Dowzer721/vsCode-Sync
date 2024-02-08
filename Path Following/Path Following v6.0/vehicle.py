
import pygame

vehiclePosition = [0, 0]
vehicleVelocity = [0, 0]
vehicleHeading = 0

def renderVehicle(canvas, renderColour):
    pygame.draw.circle(canvas, renderColour, vehiclePosition, 8, 0)