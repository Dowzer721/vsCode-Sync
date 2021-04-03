
# This version will allow for the SVG to be scaled via a function, 
# so that the window can be resized and the svg will scale accordingly.

import os
from PIL import Image, ImageTk
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import tkinter
import tkinter.font as tkFont

workingFolder = "C:/Users/Luke/Documents/Learning Python/Dad TKinter Program/"
originalDrawingName = "PA-122 AB.svg"
originalDrawingPath = workingFolder + originalDrawingName

# Getting the size of the original SVG:
originalSVGLoaded = svg2rlg(originalDrawingPath)
renderPM.drawToFile(originalSVGLoaded, workingFolder + "temp files/originalSVGTemp.png", fmt="PNG")
originalDrawingImage = Image.open(workingFolder + "temp files/originalSVGTemp.png")
originalDrawingW, originalDrawingH = originalDrawingImage.size # Got W x H
# print(f"oriW: {originalDrawingW}, oriH: {originalDrawingH}")
originalDrawingImage.close()

# Deleting the temp file as to keep folders clean. 
# Not required but the point of a temp file is that it is TEMPORARY, 
# and therefore is not needed later on, so why not delete it?
os.remove(workingFolder + "temp files/originalSVGTemp.png")

# Lots of other code uses root instead of window, but I feel like window makes the most 
# sense because the window is what you see. And it is what all the widgets get added to:
window = tkinter.Tk()
window.title("TKinter SVG Viewer v1.2 - Luke Shears 2021")
windowStartingWidth = 300
windowStartingHeight= 100
window.geometry(str(windowStartingWidth) + 'x' + str(windowStartingHeight))

SVGCanvas = tkinter.Canvas(window, width=windowStartingWidth, height=windowStartingHeight//2)
SVGCanvas.pack()

def createPNGfromScaledSVG(pathToSVGFile, widthPercent, heightPercent):
    # All three arguments should be strings

    # SVG_CodeFile = open(pathToSVGFile, 'r')
    # SVG_Code = SVG_CodeFile.readlines()
    # SVG_CodeFile.close()
    with open(pathToSVGFile, 'r') as SVG_CodeFile:
        SVG_Code = SVG_CodeFile.readlines()

    svgWidthHeightSetLineIndex = 0 # The index of the line which is used to set the size of the SVG
    layerCount = 0
    for line in range(len(SVG_Code)):
        codeLine = SVG_Code[line]

        if ("<svg" in codeLine):
            svgWidthHeightSetLineIndex = line
        
        # Crude approach to count layers, until I can see how SVG's are actually created. 
        # There must be a better to specify if something is a layer, 
        # and not just another <g> tag (group). 
        # Because I have manually added these "visibility" options to the file after being sent it:
        if ("visibility=" in codeLine): 
            layerCount += 1

    # The line of code that is used to set the size of the SVG:
    svgWidthHeightSetLine = SVG_Code[svgWidthHeightSetLineIndex] 
    # print(svgWidthHeightSetLine)

    svgWidthSetIndex  = svgWidthHeightSetLine.index("width=")

    editedWidthHeightSetLine = (
        svgWidthHeightSetLine[:svgWidthSetIndex] +
        "width="  + widthPercent + " " +
        "height=" + heightPercent + " " +
        svgWidthHeightSetLine[svgWidthHeightSetLine.index("viewBox="):]
    )
    # print(editedWidthHeightSetLine)

    SVG_Code[svgWidthHeightSetLineIndex] = editedWidthHeightSetLine

    newDrawingName = "Scaled " + originalDrawingName
    scaledSVG = open(workingFolder + newDrawingName, 'w')
    for codeLine in SVG_Code:
        scaledSVG.write(str(codeLine) )
    scaledSVG.close()

    scaledSVGPath = workingFolder + newDrawingName
    renderPM.drawToFile(svg2rlg(scaledSVGPath), workingFolder + "temp files/scaled temp.png", fmt="PNG")
    return Image.open(workingFolder + "temp files/scaled temp.png")

    

def drawPNGToCanvas(PNGToDraw):
    PHO_Img = ImageTk.PhotoImage(PNGToDraw)
    SVGCanvas.create_image(0, 0, anchor="nw", image=PHO_Img)
    

# This function is called whenever the window is resized.
# I have done this so that resizing the window also resizes the SVG to fit on screen. 
# There may be a better, more efficient method but this is just me playing around.
def resizeEvent(event):
    window.update()
    
    # A string of the window geometry; size then position: "WxH+x+y"
    dimensionInfo = window.winfo_geometry()
    # print(dimensionInfo)
    
    # The points in the "dimensionInfo" string that contain either an 'x' or '+',
    # using a list comprehension:
    dimensionPoints = [
        i for i in range(len(dimensionInfo))
        if (dimensionInfo[i] == 'x') or (dimensionInfo[i] == '+')
    ]
    # print(dimensionPoints)
    
    # The width, height, x and y of the window, taken from the "dimensionInfo" string.
    windowW = int( dimensionInfo[:dimensionPoints[0]])
    windowH = int( dimensionInfo[ dimensionPoints[0]+1 : dimensionPoints[1]]  )
    windowX = int( dimensionInfo[ dimensionPoints[1]+1 : dimensionPoints[2]]  )
    windowY = int( dimensionInfo[ dimensionPoints[2]+1 :]                     )
    # print(f"w:{windowW}, h:{windowH}, x:{windowX}, y:{windowY}")

    newSVGScale = chr(34) + str(round(100 * (windowW / originalDrawingW), 2) ) + "%" + chr(34)
    # print(newSVGScale)

    scaledPNG = createPNGfromScaledSVG(originalDrawingPath, newSVGScale, newSVGScale)
    PNGw, PNGh = scaledPNG.size
    # adjust the size of the SVGCanvas so that it fits in the newly sized window.
    

    drawPNGToCanvas(scaledPNG)


    #
window.bind("<Configure>", resizeEvent)

window.mainloop()

# while True:

#     # widthString = str(randint(300, 500))
#     # heightString= str(randint(200, 400))
#     # geometryString = widthString + "x" + heightString
#     # window.geometry(geometryString)
    
#     window.update_idletasks()
#     window.update()