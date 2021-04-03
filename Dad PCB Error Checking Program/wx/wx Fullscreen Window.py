
import wx

application = wx.App(False)

mainFrame = wx.Frame(
    None, 
    title="TITLE", 
    size=(400, 500), 
    style=
        wx.MINIMIZE_BOX
        # | wx.MAXIMIZE_BOX
        | wx.CLOSE_BOX
        | wx.RESIZE_BORDER
        | wx.SYSTEM_MENU
        | wx.CAPTION
        | wx.CLIP_CHILDREN
)
mainFrame.Show()

menubar = wx.MenuBar()
fileMenu = wx.Menu()

menubar.Append(fileMenu, "&File")

mainFrame.SetMenuBar(menubar)

application.MainLoop()