
import wx
from wx.lib.splitter import MultiSplitterWindow

from graphics.FileIO import FileIO
from graphics.MatplotlibWrap import MatplotlibWrap
#from graphics.GnuplotWrap import GnuplotWrap
from graphics.VtkWrap import VtkWrap
from graphics.PlotBrowser import PlotBrowser
from graphics.PropertyEditor import PropertyEditor
from graphics.BackendModule import backend

class IntegratedWindowPanel(wx.Panel):
    
    def __init__(self, parent):#, log):
        #self.log = log
        wx.Panel.__init__(self, parent, -1)

        #cp = ControlPane(self)
        
        splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer.Add(cp)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.plotItems={}

        self.plotBrowser = PlotBrowser(self,-1, size=(100,546))
        splitter.AppendWindow(self.plotBrowser, 100)

        self.backendWrap = MatplotlibWrap(self,-1, size=(600,546))
        #self.backendWrap = VtkWrap(self, size=(70,546))
        splitter.AppendWindow(self.backendWrap, 700)

        self.propertyEditor = PropertyEditor(self,size=(125,546))
        splitter.AppendWindow(self.propertyEditor, 125)
        
        self.io=FileIO(self)
        #self.testSqomega()

    def testColumnInput(self):
        x,y=self.io.extractColumns('/home/jbk/DANSE/graphics/trunk/tests2/api/DOS_Al6x6x6-10.plot')
        self.backendWrap.addLine(x, y)
        
    def testNetcdfInput(self):
        file1='/home/jbk/DANSE/graphics/trunk/tests2/api/ISF_graphite.nc'
        from Scientific.IO.NetCDF import NetCDFFile 
        file = NetCDFFile(file1, 'r')
        vars = file.variables.keys()
        sf=file.variables['sf'].getValue() #Numeric array
        q=file.variables['q'].getValue()
        time=file.variables['time'].getValue()
        for t in range(len(time)):
            self.backendWrap.addLine(q,sf[:,t]) 
            
    def testSqomega(self):
        file1='/home/jbk/gulp3.0/incom6x3sup10K100ps/ISF_graphite.nc'
        from Scientific.IO.NetCDF import NetCDFFile 
        file = NetCDFFile(file1, 'r')
        vars = file.variables.keys()
        sf=file.variables['dsf'].getValue() #Numeric array
        q=file.variables['q'].getValue()
        time=file.variables['frequency'].getValue()
        for t in range(len(time)):
            self.backendWrap.addLine(q,sf[:,t]) 

ID_ColumnFile = wx.NewId()
ID_NetcdfFile = wx.NewId()
ID_ScatteringFile = wx.NewId()
ID_SavePlot = wx.NewId()

class IntegratedWindowFrame(wx.Frame):
    
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Graphics", size=(1110, 590))
        # create menu
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(ID_ColumnFile, "Load File: Column Data")
        file_menu.Append(ID_ScatteringFile, "Load Scattering File")
        file_menu.Append(ID_NetcdfFile, "Load Netcdf File")
        file_menu.Append(ID_SavePlot, "Save Plot")
        file_menu.Append(wx.ID_EXIT, "Exit")
        mb.Append(file_menu, "File")
        self.SetMenuBar(mb)
        
        self.panel = IntegratedWindowPanel(self)
        
        self.Bind(wx.EVT_MENU, self.panel.io.OnLoadColumnFile, id=ID_ColumnFile)
        self.Bind(wx.EVT_MENU, self.panel.io.OnLoadScatteringFile, id=ID_ScatteringFile)
        self.Bind(wx.EVT_MENU, self.panel.io.OnLoadNetcdfFile, id=ID_NetcdfFile)
        self.Bind(wx.EVT_MENU, self.panel.io.OnSavePlot, id=ID_SavePlot)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

    def OnExit(self, event):
        self.Close()
        

def runGraphics():
    # Make a frame to show it
    app = wx.PySimpleApp()
    frame = IntegratedWindowFrame(None)
    frame.Show()
    app.MainLoop()
    frame.testColumnInput()
    #self.testNetcdfInput()

if __name__ == "__main__":
    runGraphics()
