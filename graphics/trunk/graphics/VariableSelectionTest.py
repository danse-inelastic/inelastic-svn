#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1LISTVIEW1, wxID_FRAME1LISTVIEW2, 
 wxID_FRAME1LISTVIEW3, wxID_FRAME1XAXIS, wxID_FRAME1YAXES, 
] = [wx.NewId() for _init_ctrls in range(6)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(517, 300), size=wx.Size(1280, 733),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Variable Selection')
        self.SetClientSize(wx.Size(1280, 733))

        self.listView1 = wx.ListView(id=wxID_FRAME1LISTVIEW1, name='listView1',
              parent=self, pos=wx.Point(8, 24), size=wx.Size(208, 304),
              style=wx.LC_ICON)

        self.listView2 = wx.ListView(id=wxID_FRAME1LISTVIEW2, name='listView2',
              parent=self, pos=wx.Point(248, 48), size=wx.Size(200, 100),
              style=wx.LC_ICON)

        self.listView3 = wx.ListView(id=wxID_FRAME1LISTVIEW3, name='listView3',
              parent=self, pos=wx.Point(248, 192), size=wx.Size(200, 136),
              style=wx.LC_ICON)

        self.xAxis = wx.StaticText(id=wxID_FRAME1XAXIS, label=u'x axis',
              name=u'xAxis', parent=self, pos=wx.Point(248, 24),
              size=wx.Size(72, 17), style=0)

        self.yAxes = wx.StaticText(id=wxID_FRAME1YAXES, label=u'y axes',
              name=u'yAxes', parent=self, pos=wx.Point(248, 160),
              size=wx.Size(72, 24), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
