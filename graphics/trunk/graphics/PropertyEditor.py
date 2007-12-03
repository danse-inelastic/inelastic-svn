import wx
import wx.grid as gridlib
from graphics.MatplotlibPropertyTable import MatplotlibPropertyTable
from graphics.VtkPropertyTable import VtkPropertyTable
from graphics.PlotBrowser import PlotBrowser
from pylab import setp, getp
from numpy import array     

__doc__='''Expected behavior is that upon loading a certain data type a property editor panel will also be created
containing a copy of the types of properties and getting the initial values from that new data structure (usually the 
defaults).'''

class PropertyEditor(gridlib.Grid):
    
   # currentItem = PlotBrowser.currentItem
    
    def __init__(self, parent,size=(252,546)):
        gridlib.Grid.__init__(self, parent, -1, size=size)
        self.parent=parent
        #self.selectedItem = parent.plotBrowserController.selectedItem
        self.backendWrap = self.parent.backendWrap
        self.plotItems = self.parent.plotItems#mplibCon.matplotlib.plotItems
        from graphics.BackendModule import backend as MPWBackend
        self.backend = MPWBackend
        
        if self.backend=='matplotlib':
            self.table = MatplotlibPropertyTable(self)
        elif self.backend=='vtk':
            self.table = VtkPropertyTable(self)
        self.SetTable(self.table)
        self.setGridConditions()
        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)
        gridlib.EVT_GRID_CELL_CHANGE(self, self.OnCellChange)
        #self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        
    def setGridConditions(self):
        self.SetRowLabelSize(0)
        self.SetColLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(True)
        self.setMaxColWidth(200)
        self.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        #self.SetColAttr(1,)

        #do something like set maximum column width
        
    def setMaxColWidth(self,maxWidth):
        #numCols=self.table.GetNumberCols()
        # resize the columns smaller if twoo big
                # resize the columns smaller if twoo big
        col1Size=self.GetColSize(0)
        if col1Size>maxWidth:
            self.SetColSize(0,maxWidth)
        col2Size=self.GetColSize(1)
        if col2Size>maxWidth:
            self.SetColSize(1,maxWidth)
        
        
    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if evt.GetCol()==1:
            self.EnableCellEditControl()
            
    def OnCellChange(self, evt):
        row=evt.GetRow()
        value = self.GetCellValue(row, evt.GetCol())
        #exec(apiMethod+'('+str(value)+')')
        if self.backend=='matplotlib':
            if PlotBrowser.currentItem!='plottable':
                self.matplotlibChange(row, value)
            elif PlotBrowser.currentItem=='plottable':
                self.plottableChange(value)
            self.backendWrap.replot()
        elif self.backend=='vtk':
            self.vtkChange(row, value)
        
    def matplotlibChange(self, row, value):
        apiKeyword = self.table.properties[row][3]
        objectReference = self.plotItems[PlotBrowser.currentItem]
        #first take care of some special cases:
        #from decimal import Decimal
        #getcontext().prec = 2
        sequence2String=['xlim','ylim']
        array2String=['xticks','yticks','xdata','ydata']
        textBox2String=['xticklabels','yticklabels']
        if apiKeyword in sequence2String:
            value=eval(value)
        elif apiKeyword in array2String:
            value=eval(value)
            value=array(value)
        elif apiKeyword in textBox2String:
            #first get the Text instances
            listOfTexts=getp(objectReference, apiKeyword, value)
            #then set them
            strings=eval(value)
            for i in range(len(listOfTexts)):
                listOfTexts[i].set_text(strings[i])
            value=listOfTexts
        #set the new property    
        setp(objectReference, apiKeyword, value)
        #refresh all properties
        self.table.loadModel(PlotBrowser.currentItem)
        
    def vtkChange(self, row, value):
        apiKeyword = self.table.properties[row][0]
        objectReference = self.plotItems[PlotBrowser.currentItem]
        
        #first take care of some special cases:
        #from decimal import Decimal
        #getcontext().prec = 2
#        sequence2String=['xlim','ylim']
#        array2String=['xticks','yticks','xdata','ydata']
#        textBox2String=['xticklabels','yticklabels']
#        if apiKeyword in sequence2String:
#            value=eval(value)
#        elif apiKeyword in array2String:
#            value=eval(value)
#            value=array(value)
#        elif apiKeyword in textBox2String:
#            #first get the Text instances
#            listOfTexts=getp(objectReference, apiKeyword, value)
#            #then set them
#            strings=eval(value)
#            for i in range(len(listOfTexts)):
#                listOfTexts[i].set_text(strings[i])
#            value=listOfTexts
            
        #set the new property    
        objectReference.set(apiKeyword=value)
        #refresh all properties
        self.table.loadModel(PlotBrowser.currentItem)
        
    def plottableChange(self, value):
        #mp.graph.set(eval(apiKeyword+"='"+value+"'"))
        keys = self.mplibCon.graph.plottables.keys()
        self.mplibCon.graph.plottables[keys[0]] = int(value)
        
    def changeModel(self,type):
        self.table.loadModel(type)
        self.SetTable(self.table)
        self.ForceRefresh()    
        #self.parent.Refresh()
        self.setGridConditions()
            
#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "", size=(640,480))
        p = wx.Panel(self, -1, style=0)
        grid = PropertyEditor(p, log)
        bs = wx.BoxSizer(wx.VERTICAL)
        bs.Add(grid, 1, wx.GROW|wx.ALL, 5)
        p.SetSizer(bs)

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


            

