
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

workingFolder = "C:/Users/Luke/Documents/Learning Python/Dad TKinter Program/"
drawingPath = workingFolder + "PA-122 AB.svg"

drawingNewWidth = [0.5]
drawingNewWidth.append(str(100 * drawingNewWidth[0]) + "%")

drawingNewHeight = [0.25]
drawingNewHeight.append(str(100 * drawingNewHeight[0]) + "%")

svgWidthHeightSetLine = 0
svgWidthHeightSetLineIndex = 0

loadedDrawingCode = open(drawingPath, 'r')
codeLines = loadedDrawingCode.readlines()
loadedDrawingCode.close()

topLayerCount = 0
for i in range(len(codeLines)):
    line = codeLines[i]
    if ("<svg" in line):
        svgWidthHeightSetLine = line
        svgWidthHeightSetLineIndex = i
    if ("visibility=" in line):
        topLayerCount += 1
# For "PA-122 AB.svg", this should print 6
# print(topLayerCount)


print(svgWidthHeightSetLine)

svgWidthSetLocation = svgWidthHeightSetLine.index("width=")
svgHeightSetLocation = svgWidthHeightSetLine.index("height=")
editedWidthHeightSetLine = (
    svgWidthHeightSetLine[:svgWidthSetLocation] + 
    "width=" + chr(34) + drawingNewWidth[1] + chr(34) + " " +
    "height=" + chr(34) + drawingNewHeight[1] + chr(34) + " " +
    svgWidthHeightSetLine[svgWidthHeightSetLine.index("viewBox=") :]
)

print(editedWidthHeightSetLine)
# input()

codeLines[svgWidthHeightSetLineIndex] = editedWidthHeightSetLine
tempSVG = open(workingFolder + "Rescaled PA-122 AB.svg", 'w')
for line in codeLines:
    tempSVG.write(str(line) )
tempSVG.close()

drawingPath = workingFolder + "Rescaled PA-122 AB.svg"

# input()


loadedDrawing = svg2rlg(drawingPath)
# loadedDrawing = svg2rlg(workingFolder + "PA-122 AB.svg")
renderPM.drawToFile(loadedDrawing, "temp.png", fmt="PNG")


import tkinter
window = tkinter.Tk()
window.title("TKinter SVG Viewer v1.0 - Luke Shears 2021")


from PIL import Image, ImageTk
img = Image.open("temp.png")
pimg = ImageTk.PhotoImage(img)
imageSize = img.size

canvasWidth = imageSize[0] * drawingNewWidth[0] # Change this final integer to any number to affect how much of the image is drawn.
canvasHeight= imageSize[1] * drawingNewHeight[0]
frame = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight)
frame.pack()
frame.create_image(0, 0, anchor="nw", image=pimg)

tkinter.mainloop()