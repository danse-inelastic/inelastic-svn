# Vimm: Visual Interface to Materials Manipulation
#
# Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government
# retains certain rights in this sofware.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
# USA


import wx

class Measurements(wx.Frame):
    def __init__(self, parent, id, **kwds):
        kwds['style'] = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION
        wx.Frame.__init__(self, parent, id, "Measurement Options", **kwds)

        self.parent = parent

        self.color = (1.0, 1.0, 1.0)
        self.weight = 2

        self.create_widgets()
        self.layout_page()
        return

    def create_widgets(self):
        self.btnColor = wx.Button(self, -1, "Change Line Color")
        self.btnWeight = wx.Button(self, -1, "Change Line Weight")
        self.btnClear = wx.Button(self, -1, "Clear Distances from Screen")
        self.btnClose = wx.Button(self, -1, "Close")

        wx.EVT_BUTTON(self, self.btnColor.GetId(), self.change_color)
        wx.EVT_BUTTON(self, self.btnWeight.GetId(), self.change_width)
        wx.EVT_BUTTON(self, self.btnClear.GetId(), self.clear)
        wx.EVT_BUTTON(self, self.btnClose.GetId(), self.close)

        return

    def layout_page(self):
        szrMain = wx.BoxSizer(wx.VERTICAL)
        szrTop = wx.BoxSizer(wx.HORIZONTAL)
        szrBottom = wx.BoxSizer(wx.HORIZONTAL)

        szrTop.Add(self.btnColor, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrTop.Add(self.btnWeight, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        szrBottom.Add(self.btnClear, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrBottom.Add(self.btnClose, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        szrMain.Add(szrTop, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        szrMain.Add(szrBottom, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        
        self.SetAutoLayout(1)
        self.SetSizer(szrMain)
        szrMain.Fit(self)
        szrMain.SetSizeHints(self)
        self.Layout()
        self.Centre()
        return

    def change_color(self, *args):
        d = wx.ColourDialog(self)
        d.GetColourData().SetChooseFull(True)
        if d.ShowModal() == wx.ID_OK:
            data = d.GetColourData()
            r,g,b = data.GetColour().Get()
            self.color = r/255.,g/255.,b/255.
        return

    def change_width(self, *args):
        widthDlg = wx.TextEntryDialog(self, "Enter Line Weight", "Enter Line Weight")
        if widthDlg.ShowModal() == wx.ID_OK:
          self.weight = float(widthDlg.GetValue())
        return

    def clear(self, *args):
        self.parent.canvas.shapes.distances = []
        self.parent.canvas.InitGL()
        self.parent.canvas.Refresh()
        return

    def close(self, *args):
        self.clear()
        self.parent.canvas.set_measure(False)
        self.Close(True)
        return
