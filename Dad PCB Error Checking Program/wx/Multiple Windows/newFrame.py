
import wx

class newFrame(wx.Frame):
    def __init__(self, newTitle_ = "TITLE UNSET", newBorders_ = (-1, -1, -1, -1), show_ = True ):

        self.controls = []

        # If the borders are default, just create a default frame:
        if newBorders_ == (-1, -1, -1, -1):
            wx.Frame.__init__(self, None, id=-1, title=newTitle_)

            self.framePosition = self.Position
            self.frameSize = self.Size

            self.Show(show_)
            return

        
        # Unpacking values in "newBorders_" for easier understanding:
        LEFT_BORDER, RIGHT_BORDER, TOP_BORDER, BOTTOM_BORDER = list(newBorders_)

        # Get the display width and height of the primary computer screen:
        _, _, clientWidth, clientHeight = wx.Display().GetClientArea().Get()
        # print(f"w: {clientWidth}, h: {clientHeight}")

        # Calculate the width and height of the frame:
        frameWidth = clientWidth - (LEFT_BORDER + RIGHT_BORDER)
        frameHeight = clientHeight - (TOP_BORDER + BOTTOM_BORDER)

        self.framePosition = wx.Point(
            LEFT_BORDER if not (newBorders_[0] == -1) else -1, 
            TOP_BORDER if not (newBorders_[2] == -1) else -1
        )
        self.frameSize = wx.Size(frameWidth, frameHeight)

        # (parent, id=ID_ANY, title=””, pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
        # DefaultSize >> wx.Size(-1, -1)
        # DefaultPosition >> wx.Position(-1, -1)
        wx.Frame.__init__(self, None, id=-1, title=newTitle_, pos=self.framePosition, size=self.frameSize)
        self.Show(show_)
    
    def addControl(self, type_, label_="", position_ = wx.Point(-1, -1), size_ = wx.Size(-1, -1)):
        if type_ == "button":
            # print(f"BUTTON @ ({position_.x}, {position_.y}) : {size_[0]}x{size_[1]}")
            newButton = wx.Button(self, id=-1, label=label_, pos=position_, size=size_)
            self.controls.append(newButton)
        elif type_ == "filePicker":
            newFilePicker = wx.FilePickerCtrl(self, id=-1, message=label_, pos=position_, size=size_)
            self.controls.append(newFilePicker)
        elif type_ == "staticText":
            newStaticText = wx.StaticText(self, -1, label_, position_, size_)
            self.controls.append(newStaticText)
        else:
            raise Exception(f"Unknown type passed to addControl method ({chr(34) + type_ + chr(34)})")