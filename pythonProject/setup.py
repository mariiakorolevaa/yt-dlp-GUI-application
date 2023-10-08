import os
import sys
from threading import Thread

import wx.adv
import wx.lib.newevent
import yt_dlp


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        self.OnChoose = self.OnChooseHandler
        self.OnDownload = self.OnDownloadHandler
        self.OnClose = self.OnCloseHandler
        self.Center()
        self.SetSize((700, 450))
        self.SetBackgroundColour('#7a4e71')
        self.SetIcon(wx.Icon(resource_path('icon.ico'), wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # create a panel
        self.panel = wx.Panel(self)

        # create a menu bar
        self.menubar = wx.MenuBar()
        self.filemenu = wx.Menu()
        self.filemenu.AppendSeparator()
        self.filemenu.Append(wx.ID_EXIT, '&Exit', 'Exit the program')
        self.SetMenuBar(self.menubar)

        # create a status bar as a text field
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')
        # set height of the status bar
        self.SetStatusBarPane(-1)

        # destination folder - name
        self.destination = wx.TextCtrl(self.panel, pos=(10, 10), size=(500, 25))
        self.destination.SetHint('Enter a destination folder')
        self.destination.SetBackgroundColour('#e4dbe2')
        self.destination.SetForegroundColour('#000000')
        self.destination.SetValue('C:\\Users\\kiris\\Videos')
        self.destination.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # set current directory as a default value
        # current_folder = os.path.dirname(os.path.realpath(__file__))

        # self.destination.SetValue(current_folder)

        # create a button to choose a destination folder
        self.choose = wx.Button(self.panel, label='Choose directory', pos=(520, 10), size=(120, 25))
        self.choose.SetBackgroundColour('#bd92a5')
        self.choose.SetForegroundColour('#f1e9ed')
        self.choose.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.choose.Bind(wx.EVT_BUTTON, self.OnChoose)
        self.choose.SetWindowStyle(wx.BORDER_NONE)

        # create a text field for a link to a video
        self.link = wx.TextCtrl(self.panel, pos=(10, 40), size=(500, 25))
        self.link.SetHint('Enter a link to a video')
        self.link.SetBackgroundColour('#e4dbe2')
        self.link.SetForegroundColour('#000000')
        # test value
        self.link.SetValue('https://www.youtube.com/watch?v=lM1DI5oeOcQ')
        self.link.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # create a button to download a video
        self.download = wx.Button(self.panel, label='Download', pos=(200, 70), size=(120, 25))
        self.download.SetBackgroundColour('#bd92a5')
        self.download.SetForegroundColour('#f1e9ed')
        self.download.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.download.Bind(wx.EVT_BUTTON, self.OnDownload)
        self.download.SetWindowStyle(wx.BORDER_NONE)

        # choose quality of a video
        self.quality = wx.Choice(self.panel, pos=(520, 40), size=(50, 25))
        self.quality.SetForegroundColour('#bd92a5')

        self.quality.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.quality.Append('best')
        self.quality.Append('worst')
        self.quality.SetSelection(0)

        # add gif animation to the right side of the window
        self.gif = wx.adv.AnimationCtrl(self.panel, pos=(10, 100), size=(10, 10))
        self.gif.LoadFile(resource_path('loading.gif'))
        self.gif.SetBackgroundColour('#7a4e71')
        # make it small
        self.gif.Play()

    # event handlers
    def OnDownloadHandler(self, event):
        self.statusbar.SetStatusText('Downloading...')
        try:
            thread = Thread(target=self.ThreadedDownload, args=[])
            thread.start()
            self.statusbar.SetStatusText('Downloaded')

        except Exception as e:
            self.statusbar.SetStatusText('Error: ' + str(e))

    def ThreadedDownload(self):
        with (yt_dlp.YoutubeDL({'format': 'best', 'outtmpl': self.destination.GetValue() + '/%(title)s.%(ext)s'})
              as ydl):
            ydl.download([self.link.GetValue()])

    def OnChooseHandler(self, event):
        self.statusbar.SetStatusText('Choosing...')
        # open an explorer to choose a folder
        dialog = wx.DirDialog(self, 'Choose a folder', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.destination.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.statusbar.SetStatusText('Chosen')

    def OnCloseHandler(self, event):
        self.Destroy()


class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.frame = None

    def OnInit(self):
        self.frame = MyFrame(None, title='Download videos')
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
