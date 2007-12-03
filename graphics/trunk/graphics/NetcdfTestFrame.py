#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BROWSEBUTTON, wxID_FRAME1NETCDFFILE, 
] = [wx.NewId() for _init_ctrls in range(3)]

class Frame1(wx.Frame):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(None, 0, border=0, flag=0)
        parent.AddWindow(None, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(444, 266), size=wx.Size(1280, 733),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(1280, 733))

        self.NetcdfFile = wx.TextCtrl(id=wxID_FRAME1NETCDFFILE,
              name=u'NetcdfFile', parent=self, pos=wx.Point(96, 104),
              size=wx.Size(208, 27), style=0, value=u'')

        self.BrowseButton = wx.Button(id=wxID_FRAME1BROWSEBUTTON,
              label=u'Browse', name=u'BrowseButton', parent=self,
              pos=wx.Point(320, 104), size=wx.Size(85, 32), style=0)
        self.BrowseButton.Bind(wx.EVT_BUTTON, self.OnBrowse,
              id=wxID_FRAME1BROWSEBUTTON)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBrowse(self, event):
        event.Skip()
