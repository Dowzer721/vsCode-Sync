
# Need to sort out the flashing. I think this could be solved with multi-threading, but that's scary and 
# I'm tired rn. I also want to rewrite this file as it is ugly and damn confusing. 

import wx
import wx.svg

application = wx.App(False)

workingFolder = "C:/Users/Luke/Documents/Learning Python/Dad PCB Error Checking Program/" 
svg_filename = workingFolder + "TKinter/PA-122 AB.svg"

global svg_codeLines
svg_codeLines = open(svg_filename, 'r').readlines()
# print(len(svg_codeLines))

def createPCBSVG(new_codeLines_ = svg_codeLines):
    tempSVGFile = open(workingFolder + "wx/temp files/editedSVG.svg", 'w')
    tempSVGFile.writelines(new_codeLines_)
    tempSVGFile.close()
    # print("created")

    return wx.svg.SVGimage.CreateFromFile(workingFolder + "wx/temp files/editedSVG.svg")
createPCBSVG()

layerCount = 0
layerNames = []
for line in svg_codeLines:
    if "visibility=" in line:
        layerCount += 1
        # print(line)
        IDstart = line.find("id=") + 4
        IDend = line.find(" ", IDstart) - 1
        layerID = line[IDstart : IDend]
        layerNames.append(layerID)
# print(f"layerCount: {layerCount}")
# print(layerNames)




class Button(wx.Button):
    def __init__(self, parent_, id_=wx.ID_ANY, label_="", pos_=wx.Point(0, 0), size_=(-1, -1)):
        wx.Button.__init__(self, parent=parent_, id=id_, label=label_, pos=pos_, size=size_)

        self.Bind(wx.EVT_BUTTON, self.buttonPressed)
    
    def buttonPressed(self, event):

        svg_codeLines = open(workingFolder + "wx/temp files/editedSVG.svg", 'r').readlines()
        
        buttonLabel = self.GetLabel()
        lineNumber = 0
        for line in svg_codeLines:
            if str(self.GetLabel()) in line:
                # print(f"{buttonLabel} found in line")
                visibilityIndex = line.find("visibility")
                visibleHiddenIndexStart = line.find('"', visibilityIndex)+1
                visibleHiddenIndexEnd = line.find('"', visibleHiddenIndexStart+3)
                
                isVisible = str(line[visibleHiddenIndexStart : visibleHiddenIndexEnd]) == "visible"
                visibleHiddenSwitchString = "hidden" if isVisible else "visible"
                newLine = line[:visibleHiddenIndexStart] + visibleHiddenSwitchString + line[visibleHiddenIndexEnd:]
                # print(line)
                # print(newLine)

                new_codeLines = []
                for index in range(len(svg_codeLines)):
                    if not index == lineNumber:
                        new_codeLines.append(svg_codeLines[index])
                    else:
                        new_codeLines.append(newLine)
                # print(len(new_codeLines))
                # svg_codeLines = new_codeLines
                
                mainFrame.img = createPCBSVG(new_codeLines)
                mainFrame.Refresh()
                
                return
                
                # print(line)
                # print(line[visibleHiddenIndexStart : visibleHiddenIndexEnd])

            lineNumber += 1

class Frame(wx.Frame):
    def __init__(self, size_=(-1, -1)):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, size=size_)

        self.img = createPCBSVG()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.updateButtons)
        
        self.Buttons = []
        buttonSize = (int(self.Size.width / layerCount), -1)
        for i in range(layerCount):
            buttonLabel = layerNames[i]
            buttonPosition = wx.Point(i * buttonSize[0], -1)

            self.Buttons.append(Button(
                self, 
                wx.ID_ANY, 
                buttonLabel, 
                buttonPosition, 
                buttonSize
            ))

        self.Show()
    
    def updateButtons(self, event):
        
        buttonSize = (int(self.Size.width / layerCount), -1)
        for i in range(layerCount):
            self.Buttons[i].Hide()

            buttonLabel = layerNames[i]
            buttonPosition = wx.Point(i * buttonSize[0], -1)

            self.Buttons[i] = Button(
                self, wx.ID_ANY, buttonLabel, buttonPosition, buttonSize
            )

            self.Buttons[i].Show()

        self.Refresh()
    
    def OnPaint(self, event):
        # self.img = createPCBSVG()
        deviceContext = wx.PaintDC(self)
        deviceContext.SetBackground(wx.Brush("white"))
        deviceContext.Clear()
    
        deviceContextSize = (self.Size.width, self.Size.height)
        imageSize = (self.img.width, self.img.height)
        xScale = deviceContextSize[0] / imageSize[0]
        yScale = deviceContextSize[1] / imageSize[1]


        # width = int(self.img.width * xScale)
        # height = int(self.img.height * yScale)

        context = wx.GraphicsContext.Create(deviceContext)
        self.img.RenderToGC(context, min(xScale, yScale))

mainFrame = Frame()

application.MainLoop()