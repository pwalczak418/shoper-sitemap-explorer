import wx
from gui.main_frame import MainFrame

if __name__ == "__main__":
    app = wx.App()
    main_frame = MainFrame()
    app.MainLoop()