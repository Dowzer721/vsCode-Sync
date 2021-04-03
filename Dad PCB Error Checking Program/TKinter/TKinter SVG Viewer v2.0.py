
# So, in v1.2, I was creating a new SVG and PNG every single time the window size changed, 
# which caused mega lag. This version set (2.x) I am going to create an SVG which is 
# much much larger, say 1000%, and then create a PNG from that, as shrinking the image 
# shouldn't cause distortion, unlike stretching the image. That is theoretical so this might 
# not work either!

import os
from PIL import Image, ImageTk
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import tkinter
import tkinter.font as tkFont

workingFolder = "C:/Users/Luke/Documents/Learning Python/Dad PCB Error Checking Program/TKinter"
originalSVGName = "PA-122 AB.svg"
originalSVGPath = workingFolder + originalSVGName

def createScaledSVGFromOriginal(SVGPath, newSVGScale = "1000%", outputPath="temp files/", fileFormat="png"):
    """
    This function takes: 
    SVGPath: string 
    newSVGSCale: string
    outputPath: string
    fileFormat: string

    """
    
    with open(SVGPath, 'r') as SVG_CodeFile:
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

    svgWidthSetIndex = svgWidthHeightSetLine.index("width=")

    editedWidthHeightSetLine = (
        svgWidthHeightSetLine[:svgWidthSetIndex] +
        "width="  + chr(34) + newSVGScale + chr(34) + " " +
        "height=" + chr(34) + newSVGScale + chr(34) + " " +
        svgWidthHeightSetLine[svgWidthHeightSetLine.index("viewBox="):]
    )
    # print(editedWidthHeightSetLine)

    SVG_Code[svgWidthHeightSetLineIndex] = editedWidthHeightSetLine

    # [:-4] gets rid of the .svg at the end of the filename
    newDrawingName = ("Scaled (%s) " %newSVGScale) + originalSVGName
    scaledSVGPath = workingFolder + "temp files/" + newDrawingName
    # print(scaledSVGPath)
    scaledSVG = open(scaledSVGPath, 'w')
    for codeLine in SVG_Code:
        scaledSVG.write(str(codeLine) )
    scaledSVG.close()

    
    outputLocation = workingFolder + outputPath + ("%s.%s" %(str(newDrawingName[:-4]), fileFormat) )
    # print(outputLocation)

    renderPM.drawToFile(svg2rlg(scaledSVGPath), outputLocation, fmt="PNG")
    os.remove(scaledSVGPath)
    return outputLocation

createScaledSVGFromOriginal(originalSVGPath, newSVGScale = "10%")
scaledPNGLocation = createScaledSVGFromOriginal(originalSVGPath, newSVGScale = "250%")
# print(scaledPNGLocation)