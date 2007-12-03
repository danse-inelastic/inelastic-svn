"""
Prototype plotter for plottables based on matplotlib
"""

import wx
import matplotlib
matplotlib.use("WX")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure as MFigure

import matplotlib.numerix as nx
from PlotItemRegistry import PlotItemRegistry

     
class MatplotlibWrap(wx.Panel):#Plotter):
    """Plotter for matplotlib wrapped in a wx panel

    All plotter rendering will consist of the following steps:
plot.clear()
plot.properties()
plot.points()/plot.curve()/...
plot.render()
"""
    
    def __init__(self,parent, id,size):
        """
        Define the plotting panel for the graph.
        """
        wx.Panel.__init__(self, parent=parent, id=id, size=size)
        self.parent=parent
        self.plotItems=parent.plotItems

        # Add the plot widget
        self._add_plot_widget()
        
    def addLine(self,x,y):
        # TODO: eventually will specify which figure and axes we want to add to
        line, = self.axes.plot(x,y)
        
        PlotItemRegistry.lines = PlotItemRegistry.lines+1
        #self.plotItems.append(['line',line])   
        self.plotItems['line'+str(PlotItemRegistry.lines)] = line  
        # this method should be called anytime a new object is loaded into the plot
        self.parent.plotBrowser.updateList()  

    def _add_plot_widget(self):
        """
        Add the plotting widget to the panel
        """
        # for now make it interactive, although in a real gui one will want to toggle this with a button
        matplotlib.interactive(True)
        # Put a figure on the panel, add some axes and put it on a canvas
        self.figure = MFigure()
        self.axes   = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self,-1,self.figure)
        #self.lines = None
        #self.plotItems.append(['figure',self.figure])
        #self.plotItems.append(['axes',self.axes])
        #self.plotItems['canvas']=self.canvas
        self.plotItems['figure']=self.figure
        self.plotItems['axes']=self.axes

        # On Windows, default frame size behaviour is incorrect
        # you don't need this under Linux
        if False:
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            self.toolbar.SetSize(wx.Size(fw, th))

        # Layout the window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
        self.SetSizer(sizer)  
    
    def replot(self):
#        if PlotBrowser.currentItem=='line':
#            handle=self.matplotlib.plotItems['line']
#            handle.draw()
#        elif PlotBrowser.currentItem=='plottable':
#            self.graph.render(self.matplotlib)
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
