"""
Prototype plotter for plottables based on matplotlib
"""

import wx
import vtk
from PlotItemRegistry import PlotItemRegistry
from graphics.vtk_ import *
from graphics.utils import *
from graphics.movie import movie
from graphics.common import Figure
# old way of doing this import  wx.lib.vtk  as vtk

#from vtk.wx import wxVTKRenderWindow
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import wxPython.wx
#---------------------------------------------------------------------------


class VtkWrap(wx.Panel):#(wxVTKRenderWindow):
    """wraps matlab-like vtk window"""
    
    def __init__(self, parent, id):
        """
        Define the plotting panel for the graph.
        """
        wx.Panel.__init__(self, parent=parent, id=id)
        self.parent=parent
        self.plotItems=parent.plotItems

        self._embedInWx()
        plt = VtkBackend(self) # Create backend instance
        use(plt, globals()) # Export public namespace of plt to globals()

        # Add the plot widget
        self._add_plot_widget()
        
    def _embedInWx(self):
        self.wxRW = wxVTKRenderWindow(self.parent, -1, size=(50,50)) # use the main frame as the parent 
        #self.ren = vtk.vtkRenderer()
        #wx.GetRenderWindow().AddRenderer(self.ren)
        #self.wxRW.pack(expand='true', fill='both')
        self.renwin = self.wxRW.GetRenderWindow()
        #renwin.SetSize(width, height)
        #renwin.SetSize(width+1, height+1)
        #renwin.LineSmoothingOn()
        #tkw.UpdateRenderer(0.0, 0.0)
        #renwin.Render()        
        
    def addLine(self,x,y):
        line, = plot(x,y)
        
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
        self.plotItems['figure']=self.figure
        self.plotItems['axes']=self.axes

        # Layout the window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.wxRW, 1, wx.LEFT|wx.TOP|wx.GROW)
        self.SetSizer(sizer)  
    
    def replot(self):
        handle=self.plotItems['axes']
        handle.draw()
        self.Refresh()
    
#    
#    def connect(self,trigger,callback):
#        if trigger == 'xlim': self._connect_to_xlim(callback)
#
#    def points(self,x,y,dx=None,dy=None,color=0,symbol=0,label=None):
#        """Draw markers with error bars"""
#        # Convert tuple (lo,hi) to array [(x-lo),(hi-x)]
#        if dx != None and type(dx) == type(()):
#            dx = nx.vstack((x-dx[0],dx[1]-x)).transpose()
#        if dy != None and type(dy) == type(()):
#            dy = nx.vstack((y-dy[0],dy[1]-y)).transpose()
#
#        if True or dx is None and dy is None:
#            self.lines = self.axes.plot(x,y,color=self._color(color),
#                                   marker=self._symbol(symbol))
#        else:
#            self.lines, hcap, hbar = self.axes.errorbar(x,y,dy,color=self._color(color),
#                                             marker=self._symbol(symbol), 
#                                             linestyle='None',
#                                             label=label,picker=5)
#
#    def curve(self,x,y,dy=None,color=0,symbol=0,label=None):
#        """Draw a line on a graph, possibly with confidence intervals."""
#        c = self._color(color)
#        hlist = self.axes.plot(x,y,color=c,marker='',linestyle='-',label=label)
#        if False and dy != None:
#            if type(dy) == type(()):
#                self.axes.plot(x,dy[0],color=c,
#                               marker='',linestyle='--',label='_nolegend_')
#                self.axes.plot(x,dy[1],color=c,
#                               marker='',linestyle='--',label='_nolegend_')
#            else:
#                self.axes.plot(x,y+dy,color=c,
#                               marker='',linestyle='--',label='_nolegend_')
#                self.axes.plot(x,y-dy,color=c,
#                               marker='',linestyle='--',label='_nolegend_')
#
#    def _color(self,c):
#        """Return a particular colour"""
#        return self.colorlist[c%len(self.colorlist)]
#
#    def _symbol(self,s):
#        """Return a particular symbol"""
#        return self.symbollist[s%len(self.symbollist)]
