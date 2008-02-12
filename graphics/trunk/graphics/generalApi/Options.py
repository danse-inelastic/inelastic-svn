import  wx
import  wx.lib.scrolledpanel as scrolled

# Window functions

ID_TEXT = 10000
ID_TEXTCTRL = 10001

class Options(scrolled.ScrolledPanel):
    '''takes a list of label/default text box options in the 
[(,),(,),...] format'''
    def __init__(self, parent, options):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        vbox = wx.BoxSizer( wx.VERTICAL )
        gridSizer = wx.GridSizer( 0, 2, 0, 0 )
        for pair in options:
            label = wx.StaticText( parent, ID_TEXT, pair[0], wx.DefaultPosition, wx.DefaultSize, 0 )
            gridSizer.Add( label, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
            text = wx.TextCtrl( parent, ID_TEXTCTRL, pair[1], wx.DefaultPosition, [160,-1], 0 )
            gridSizer.Add( text, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

        vbox.Add( gridSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        self.SetSizer(vbox)
        self.SetAutoLayout(1)
        self.SetupScrolling()

#        sizer = wx.GridBagSizer(vgap = 10, hgap = 5)
#
#        for pair in options:
#            label = wx.StaticText(self, -1, pair[0])
#            sizer.Add( label, pos=(row,0), flag = wx.ALIGN_RIGHT|wx.GROW|wx.ALL)
#            text = wx.TextCtrl(self, -1, pair[1], size=(125, -1))
#            sizer.Add( text, pos=(row, 1), flag = wx.GROW)
            
            #wx.CallAfter(t1.SetInsertionPoint, 0)
            #self.tc1 = t1

if __name__=='__main__':
    # Make a frame to show it
    options=[('axes','straight'),('something','something else')]
    app = wx.PySimpleApp()
    frame = wx.Frame(None,-1,'Test')
    options = Options(frame,options)
    frame.Show()
    app.MainLoop()