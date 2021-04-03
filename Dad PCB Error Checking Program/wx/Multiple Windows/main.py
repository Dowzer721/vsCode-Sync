
import wx

from newFrame import *

mainFrame, editFrame, saveFrame = list(range(3))

Application = wx.App(False)

frames = [
    newFrame(newTitle_="mainFrame"),
    newFrame(newTitle_="editFrame")
]

frames[mainFrame].addControl(type_="button", label_="mainFrame Button")

frames[editFrame].addControl("staticText", "Select a file to load into program:")
frames[editFrame].addControl("filePicker", position_=wx.Point(-1, 16))

Application.MainLoop()