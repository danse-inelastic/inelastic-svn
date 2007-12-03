#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import NetcdfTestFrame

modules ={u'NetcdfTestFrame': [1, 'Main frame of Application', u'NetcdfTestFrame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = NetcdfTestFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
