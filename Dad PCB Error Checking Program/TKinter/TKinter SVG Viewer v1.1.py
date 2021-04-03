# Just cleaning up v1.0... as it was icky
# ===>
# It's still quite messy even after attempting to clean it up, but that's because of 
# bad variable naming and not fully understanding the libraries that I am using. 
# Once I get a better grasp on exactly what is happening, I should be able to beautify this file.

from PIL import Image, ImageTk
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import tkinter
import tkinter.font as tkFont

workingFolder = "C:/Users/Luke/Documents/Learning Python/Dad TKinter Program/"
originalDrawingName = "PA-122 AB.svg"

originalDrawingPath = workingFolder + originalDrawingName

originalDrawing_CodeFile = open(originalDrawingPath, 'r')
originalDrawing_Code = originalDrawing_CodeFile.readlines()
originalDrawing_CodeFile.close()

# Getting the size of the original SVG:
originalSVGLoaded = svg2rlg(originalDrawingPath)
renderPM.drawToFile(originalSVGLoaded, workingFolder + "temp files/originalSVGTemp.png", fmt="PNG")
originalDrawingImage = Image.open(workingFolder + "temp files/originalSVGTemp.png")
originalDrawingW, originalDrawingH = originalDrawingImage.size # Got W x H

# newWidth = 700
# originalToNewScaleFactor = newWidth / originalDrawingW
while True:
    try:
        newWidth = input("Original width was %d, please enter new width (blank for same): " %originalDrawingW)
        
        if newWidth == "":
            originalToNewScaleFactor = 1.0
        else:
            originalToNewScaleFactor = int(newWidth) / originalDrawingW
        
        break
    except: 
        print("Invalid input. Please enter the new width as an integer without any other characters.\n")


svgWidthHeightSetLineIndex = 0 # The index of the line which is used to set the size of the SVG
layerCount = 0
for line in range(len(originalDrawing_Code)):
    codeLine = originalDrawing_Code[line]

    if ("<svg" in codeLine):
        svgWidthHeightSetLineIndex = line
    
    # Crude approach to count layers, until I can see how SVG's are actually created. 
    # There must be a better to specify if something is a layer, 
    # and not just another <g> tag (group). 
    # Because I have manually added these "visibility" options to the file after being sent it:
    if ("visibility=" in codeLine): 
        layerCount += 1

# The line of code that is used to set the size of the SVG:
svgWidthHeightSetLine = originalDrawing_Code[svgWidthHeightSetLineIndex] 
# print(svgWidthHeightSetLine)

svgWidthSetIndex  = svgWidthHeightSetLine.index("width=")
svgHeightSetIndex = svgWidthHeightSetLine.index("height=")

# Creating string versions of the scale factor for writing to the new drawing file:
# newDrawingWidth = str(round(100 * originalToNewScaleFactor, 2) ) + '%'
# newDrawingHeight = str(round(100 * originalToNewScaleFactor, 2) ) + '%'
scaleFactorString = str(round(100 * originalToNewScaleFactor, 2) ) + '%'

editedWidthHeightSetLine = (
    svgWidthHeightSetLine[:svgWidthSetIndex] +
    # "width="  + chr(34) + newDrawingWidth + chr(34) + " " +
    # "height=" + chr(34) + newDrawingHeight + chr(34) + " " + 
    "width="  + chr(34) + scaleFactorString + chr(34) + " " +
    "height=" + chr(34) + scaleFactorString + chr(34) + " " + 
    svgWidthHeightSetLine[svgWidthHeightSetLine.index("viewBox="):]
)
# print(editedWidthHeightSetLine)

originalDrawing_Code[svgWidthHeightSetLineIndex] = editedWidthHeightSetLine

newDrawingName = "Scaled " + originalDrawingName
scaledSVG = open(workingFolder + newDrawingName, 'w')
for codeLine in originalDrawing_Code:
    scaledSVG.write(str(codeLine) )
scaledSVG.close()

newDrawingPath = workingFolder + newDrawingName

loadedSVG = svg2rlg(newDrawingPath)
renderPM.drawToFile(loadedSVG, workingFolder + "temp files/temp.png", fmt="PNG")

window = tkinter.Tk()
window.title("TKinter SVG Viewer v1.1 - Luke Shears 2021")
window.after(1, lambda: window.focus_force()) # Don't love this but it semi-works for now...

PNG_Img = Image.open(workingFolder + "temp files/temp.png")
PHO_Img = ImageTk.PhotoImage(PNG_Img)
PNG_imageSize = PNG_Img.size

canvasWidth = PNG_imageSize[0]
canvasHeight = PNG_imageSize[1]
PCB_Frame = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight)
PCB_Frame.pack()
PCB_Frame.create_image(0, 0, anchor="nw", image=PHO_Img)

img = Image.open(workingFolder + "Example Schematic.png")
img = img.resize(
    (newWidth, int(float(img.size[1]) * float(newWidth / img.size[0]) ) ),
    Image.ANTIALIAS
)
img.save(workingFolder + "temp files/Scaled Example Schematic.png")

SCH_PNG_Img = Image.open(workingFolder + "temp files/Scaled Example Schematic.png")
SCH_PHO_Img = ImageTk.PhotoImage(SCH_PNG_Img)

SCH_Frame = tkinter.Canvas(window, width=canvasWidth, height=canvasHeight)
SCH_Frame.pack()
SCH_Frame.create_image(0, 0, anchor="nw", image=SCH_PHO_Img)

# textSize = canvasHeight // 16
# SCH_Frame.create_text(
#     textSize//4, textSize, 
#     anchor="nw", text="This is where the schematic will go", 
#     font=tkFont.Font(family="Helvetica", size=str(textSize))
# )

tkinter.mainloop()
