
from os import getcwd
from PIL import Image

pcbImagePath = getcwd() + "\\Electronics Simulation\\v1\\"
pcbImageName = "sample pcb 1.jpg"
pcbImage = Image.open(pcbImagePath + pcbImageName, 'r')

pcbImageW, pcbImageH = pcbImage.size
pcbGreyImage = Image.new("RGB", (pcbImageW, pcbImageH))
pcbGreyPixels = pcbGreyImage.load()

rawPixelData = list(pcbImage.getdata())

brightnessThreshold = 110

for y in range(pcbImageH):
    for x in range(pcbImageW):
        i = x + (y * pcbImageW)
        r, g, b = rawPixelData[i]
        brightness = int((r+g+b)/3)

        if brightness <= brightnessThreshold:
            pcbGreyPixels[x,y] = (0,0,0) # (brightness, brightness, brightness)
        else:
            pcbGreyPixels[x,y] = (r,g,b)

pcbGreyImage.show()