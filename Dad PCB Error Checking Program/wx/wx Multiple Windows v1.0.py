
"""
If this runs without a hitch, but you have a load of red squiggles everywhere, I have a fix. 
It doesn't affect the execution of the program in any shape or form but it does get annoying to look at. 
It also is a pain in the ass to actually see proper errors over these BS errors. 

So yeah let me know if you get them and I'll tell you the fix I did. 
I believe it's to do with because wxPython comes from C++, and so there are issues with the IDE. 
I am on Visual Studio Code and had this problem.
"""


# wxPython
import wx

# This is the actual application behind the scenes. 
# This is not a visual thing, but instead is handling all the main functionality of the program.
application = wx.App(False)

# I created this class for handling any and all key pressed that happen upon a frame
class KeyHandler():
    # The parent here is whatever frame that will receive key presses of any kind
    def __init__(self, parent):
        self.parent = parent
    def handleKeyEvents(self, event):
        keyCode = event.GetKeyCode()

        if keyCode == wx.WXK_ESCAPE:
            # Tell the parent frame to close
            self.parent.Close()

# I created this class so that there is a fullscreen window, which cannot be closed out of. 
class mainFrame(wx.Frame):
    def __init__(self, title_="Default Frame Title"):
        wx.Frame.__init__(self, None, title=title_, size=(800, 600), style=wx.NO_BORDER)
        
        # self.ShowFullScreen(True)

        self.ShowFullScreen(not self.IsFullScreen(), wx.FULLSCREEN_NOCAPTION)

        self.Show(True)

        # I am giving it the ability to handle key presses, but realistically, this probably should happen. 
        # Currently it is used for debugging purposes, because without it, there is not proper way to end the 
        # program, without Alt-F4 or Alt-Tab. Neither of which are going for the user.
        self.keyHndr = KeyHandler(self)
        self.Bind(wx.EVT_KEY_DOWN, self.keyHndr.handleKeyEvents)

        # self.toolbar = wx.ToolBar(self, wx.ID_ANY)#, wx.Point(0, 0))
        # self.toolbar.AddControl(wx.Button)
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, "Quit", "Quit Application")
        menubar.Append(fileMenu, "&File")

        # editMenu = wx.Menu()
        # editItem = editMenu.Append(wx.ID_ANY, "Example", "Example Option")
        # menubar.Append(editMenu, "&Edit")

        minimiseMenu = wx.Menu()
        # minimiseMenu.SetBitmap(wx.Bitmap("minimise.bmp"))
        # maximiseMenu = wx.Menu()
        # quitMenu = wx.Menu()
        menubar.Append(minimiseMenu, "-")



        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
    
    def OnQuit(self, e):
        self.Close()

# I created this class as a means of having sub frames on top of the fullscreen "mainFrame" object. 
# They are other windows which can be dragged to anywhere on screen, and I assume to other monitors too. 
# I am unable to test this my end but if you want to test this that'd be very helpful.
class subFrame(wx.Frame):
    # The "pos_=(-1,-1)" here just sets position to the default position if no position is provided.
    def __init__(self, title_="", pos_=(-1,-1)):
        wx.Frame.__init__(self, None, title=title_, pos=pos_)
        self.Show(True)

        # Again, this key handler is currently here for debugging purposes, but in the case of this 
        # being a sub frame, it is not inconceivable that the frame might make use of key events other than escape.
        self.keyHndr = KeyHandler(self)
        self.Bind(wx.EVT_KEY_DOWN, self.keyHndr.handleKeyEvents)

# Terrible naming I know but the classes have the names I would've used so I need to make the necessary changes!
mF = mainFrame()

# This is just a shorthand for loop. Below is the exact same code but just expanded out.
# subFrames = [subFrame( ("Sub window %d" %i) ) for i in range(4)]
#
# subFrames = []
# for i in range(4):
#     subFrames.append( subFrame( ("Sub window %d" %i) ))

# Very similar to tkinter here. This tells the program to begin execution, without any exit parameters, so essentially forever. 
# This may be different to the tkinter version so need to read up on what this is doing before blindly using it.
application.MainLoop()
