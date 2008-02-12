import wx



ID_ChangePlotObject=wx.NewId()

#class PlotBrowser(wx.Panel):#wx.ListBox):
class PlotBrowser(wx.ListCtrl):
    
    currentItem='figure' #default value
    
    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 choices=[], style=0, validator=wx.DefaultValidator):
        self.parent = parent
        
        #wx.Panel.__init__(self, parent=parent, id=-1)
        wx.ListCtrl.__init__(self, parent, id=-1)#, choices=[])
        self.InsertColumn(0, "plot item")

        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.listCtrl, 1, wx.EXPAND)#wx.LEFT|wx.TOP|wx.GROW)
        #self.SetSizer(sizer) 
        #self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnChangePlotObject)
        
        #self.plotItems = MainPlotWindow.matplotlibController.matplotlib.plotItems
        self.plotItems = self.parent.plotItems
        
    def OnChangePlotObject(self, event):
        #currentItem = self.plotItems[event.m_itemIndex]
        PlotBrowser.currentItem = event.GetText()
        self.parent.propertyEditor.changeModel(PlotBrowser.currentItem)
        
    def updateList(self):
        keys=self.plotItems.keys()
        keys.sort()
        self.ClearAll()
        for i in range(len(keys)):
            self.InsertStringItem(i,str(keys[i]))
        self.Refresh()     
#        i=0
#        for item in self.plotItems:
#            self.InsertStringItem(i,str(item[0]))
#            i=+1
#        self.Refresh()
#        wxListCtrl::RefreshItems
#
#        void RefreshItems(long itemFrom, long itemTo)
#
#        Redraws the items between itemFrom and itemTo. The starting item must be less than or equal to the ending one.
       
       
#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "", size=(640,480))
        p = PlotBrowser(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(p, 1, wx.EXPAND)#wx.LEFT|wx.TOP|wx.GROW)
        self.SetSizer(sizer)

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop() 
