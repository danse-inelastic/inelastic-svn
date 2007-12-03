#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description: Plotting class using Matplotlib. This is a pyre component class
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pygtk
pygtk.require('2.0')
import gtk
import graphics.plot2D.common.Gtkinit 

from pylab import *
from graphics.plot2D.Plot2D import Plot2D

class MatPlot(Plot2D):
    """Class plot curves using MatPlotLib"""
    def __init__(self, name = 'MatPlot'):
        Plot2D.__init__(self,name)
        
        # Create window and record the window manager for future use.
        self.window = figure(1)
        self.manager = get_current_fig_manager()
        self.manager.window.title('MatPlot')
        grid(True)
    
    def setLabels(self, t, x, y ):
        # call superclass.setLabels
        Plot2D.setLabels(self,t,x,y)
        
        #function to set label and title
        xlabel(x)
        ylabel(y)
        title(t)
        
    def setSize(self, width, height):
        gtk.threads_enter()
        self.manager.canvas.set_size_request(width,height)
        gtk.threads_leave()
        
        Plot2D.setSize(self, width, height)

    def display(self):
        show()
    
    def _insert(self, data, style):
        curveRef = plot(data['x'], data['y'],':')[0]
        self.__setCurveStyles(curveRef, style)
        self.redraw()
        return curveRef
    
    def _updateData(self, curveRef, data):
        curveRef.set_data(data['x'],data['y'])
        
        # automatically expand or contract if upper and lower limit of curve changes.
        gca().update_datalim_numerix(curveRef.get_xdata(),
                                     curveRef.get_ydata())
        gca().autoscale_view()
        self.redraw()
    
    def _changeStyle(self, curveRef, style):
        self.__setCurveStyles(curveRef, style)
        self.redraw()
        
    def _remove(self, curveRef):
        pass
        
    def __setCurveStyles(self, curveRef, style):
        """Private function to translate general probabilities to 
        Matplotlib specific ones"""
        #Translation dictionary
        lineStyleDict ={'solid':'-','dash':'--','dot':':','dashDot':'-.'}
        symbolDict ={'diamond':'d','square':'s','circle':'o',
        'cross':'+','xCross':'x','triangle':'^'}
        colorDict = {'blue':'b','green':'g','red':'r','cyan':'c',
        'magenta':'m','yellow':'y','black':'k'}
        
        color = colorDict.get(style['color'], 'k')
        symbolColor = colorDict.get(style['symbolColor'], 'k')
        lineStyle = lineStyleDict.get(style['line'],'-') #prefer solid
        lineWidth = style['width']
        symbol = symbolDict.get(style['symbol'],'s') # prefer square
        symbolSize = style['symbolSize']
        label = style['legend']
        
        properties = {'label':label} 
        if style['with'] in ( 'points', 'linespoints'):
            properties.update({'linewidth':0.0,'markerfacecolor':symbolColor,
                              'markeredgecolor':color,
                             'marker':symbol,'markersize':symbolSize})
        if style['with'] != 'points':
            properties.update({'color':color,'linestyle':lineStyle,
                             'linewidth':lineWidth})

        setp((curveRef,), **properties )
        legend(loc='best')
        
    def redraw(self):
        gtk.threads_enter()
        self.manager.canvas.draw()
        gtk.threads_leave()
    
if __name__ == '__main__': 
    g = MatPlot('test')
    g.display()
    
#version
__id__ = '$Id: matplot.py,v 1.8 2005/09/01 14:47:20 jwliu Exp $'
