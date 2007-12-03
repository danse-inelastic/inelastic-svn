"""
Prototype plotter for plottables based on matplotlib
"""

import wx
import vtk
from PlotItemRegistry import PlotItemRegistry
from graphics.utils import *
from graphics.movie import movie
from graphics.common import Figure #,use
# old way of doing this import  wx.lib.vtk  as vtk

from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
from graphics.wxVTKRenderWindowWrapper import wxVTKRenderWindowWrapper
import wxPython.wx
from graphics.VtkBackend import VtkBackend
#---------------------------------------------------------------------------


class VtkWrap(wx.Panel):#(wxVTKRenderWindow):
    """wraps matlab-like vtk window"""
    
    def __init__(self, parent, size=(500,500)):
        """
        Define the plotting panel for the graph.
        """
        wx.Panel.__init__(self, parent=parent, id=-1, size=size)
        self.parent=parent
        self.plotItems=parent.plotItems

        self._embedInWx()
        self.vtkBackend = VtkBackend(self) # Create backend instance
        #use(vtkBackend, globals()) # Export public namespace of vtkBackend to globals()

        # Add the plot widget
        self._add_plot_widget()
        
    def _embedInWx(self):
        self.wxRW = wxVTKRenderWindow(self, -1, size=(50,50)) # use the main frame as the parent 
        #self.wxRW = wxVTKRenderWindowWrapper(self, -1, size=(500,500)) # use the main frame as the parent 
        #self.wxRW.pack(expand='true', fill='both')
        self.renwin = self.wxRW.GetRenderWindow()  
        
    def addLine(self,x,y):
        line, = self.vtkBackend.plot(x,y)
        
        PlotItemRegistry.lines = PlotItemRegistry.lines + 1
        #self.plotItems.append(['line',line])   
        self.plotItems['line'+str(PlotItemRegistry.lines)] = line  
        # this method should be called anytime a new object is loaded into the plot
        self.parent.plotBrowser.updateList()  

    def _add_plot_widget(self):
        """Pop up the plotting widget"""
        # Put a figure on the panel, add some axes and put it on a canvas
        self.figure = Figure()
        self.axes   = self.figure.gca()
        #self.lines = None
        #self.plotItems.append(['figure',self.figure])
        #self.plotItems.append(['axes',self.axes])
        #self.plotItems['canvas']=self.canvas
        self.plotItems['figure'] = self.figure
        self.plotItems['axes'] = self.axes

        # Layout the window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.wxRW)#, 1, wx.LEFT|wx.TOP|wx.GROW)
        self.SetSizer(sizer)  
    
    def replot(self):
        handle=self.plotItems['axes']
        handle.draw()
        self.Refresh()
