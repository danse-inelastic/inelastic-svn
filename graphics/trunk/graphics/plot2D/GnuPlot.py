#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description: Plotting class using Gnuplot. This is a pyre component class
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import Gnuplot
from graphics.plot2D.Plot2D import Plot2D

class GnuPlot(Plot2D):
    """Class plot data by using python binding to gnuplot.
    This will start a new process"""
    def __init__(self,name= None):
        if name is None: name = 'GnuPlot'
        
        Plot2D.__init__(self, name)
        self.gplt = Gnuplot.Gnuplot()
        
        # Gnuplot doesn't have a good internal reference for the curve added.
        # We need maintain our own list
        self.refDict = {}
        self.currRef = 0
    
    def display(self):
        # Use console to control
        #raw_input('Hit return to exit\n')
        
        # Use Gui to control
        import Tkinter,Tkconstants
        window=Tkinter.Tk()
        window.title("Gnuplot Control")
        frame = Tkinter.Frame(window,bg='white')
        frame.pack()
        label=Tkinter.Label(frame, fg='black',bg='white',text ="Click Quit to terminate Gnuplot and exit!")
        label.pack(side=Tkconstants.TOP)
        def _exitplot():
          frame.quit()
        button=Tkinter.Button(frame, text= "Quit",command=_exitplot )

        button.pack(side=Tkconstants.BOTTOM)
        window.mainloop()
        
    def _insert ( self, data, style):     
        self.currRef += 1
        styleStr = self.__buildOptions(style)
        item = Gnuplot.Data(data['x'],data['y'],
                            with = styleStr,
                            title = style['legend'])
        self.gplt.replot(item)
        self.refDict[self.currRef] = item
        return self.currRef
        
    def _updateData ( self, curveRef, data):
        # Gnuplot.py doesn't provide a way to erase the previous curve
        # Neither plot ( which will rebuild the item list ) nor replot (which will simply add an item 
        # can do an update. We need make our own function call to the self.gplt.itemlist.
        item = self.refDict[curveRef]
        self.gplt.itemlist.remove(item)
        titleStr = item.get_option('title')
        styleStr = item.get_option('with')
        
        # Reconstruct another item.
        newItem = Gnuplot.Data(data['x'],data['y'],
              title = titleStr,
              with = styleStr )
        self.gplt.replot(newItem)
        self.refDict[curveRef] = newItem
        
    def _changeStyle( self, curveRef, style):
        item = self.refDict[curveRef]
        styleStr = self.__buildOptions(style)
        titleStr = style['legend']
        item.set_option(with=styleStr, title=titleStr)
        
        # refresh will do the real change ( plot and replot call refresh as well )
        self.gplt.refresh()
    
    def _remove(self, curveRef):
        item = self.refDict[curveRef]
        self.gplt.itemlist.remove(item)
        self.gplt.refresh()
        self.refDict.pop(curveRef,None)
        
    def __buildOptions(self,style):
        """Translate from the general way of specifying plotting option to the 
        way that the Gnuplot is using."""
        # gnuplot 4.0 supported
        colorDict = { 'black':'0', 'red':'1', 'green':'2', 'blue':'3',
                'magenta':'4', 'cyan':'5', 'brown':'6', 'yellow':'7'}
        symbolDict = { 'cross':'1', 'xcross':'2', 'star':'3', 
                       'square':'5', 'circle':'7','triangle':'9',
                       'diamond':'13' }

        lineColor = colorDict.get( style['color'], '0' )
        symbolColor = colorDict.get( style['symbolColor'], '0')
        symbol = symbolDict.get( style['symbol'], '5') # square
        # Neglect line style which can't be supported
        
        with = style['with'][:]
        if with == 'sticks':
            with = 'impulses' # Gnuplot uses impulses for sticks
            
        styleStr =  with
        
        if with in ( 'points', 'linespoints'):
            # only in this two cases can we specify the point and point size.
            styleStr += ' linetype ' + symbolColor
            styleStr += ' pointtype ' + symbol
            styleStr += ' pointsize ' + str(style['symbolSize']/5.0)
            if with == 'linespoints':
                styleStr += ' linewidth ' + str(style['width'])
        else:
            styleStr += ' linetype ' + lineColor
            styleStr += ' linewidth ' + str(style['width'])
        
        return styleStr
    
    def setLabels(self,title,x,y):
        # call superclass.setLabels
        Plot2D.setLabels(self,title,x,y)
        
        # draw labels
        self.gplt.xlabel(self.xlabel)
        self.gplt.ylabel(self.ylabel)
        self.gplt.title(self.title)
        
    
if __name__ == '__main__':
    g = GnuPlot('Test')
    g.gplt.plot('sin(x)')
    g.display()

#version
__id__ = '$Id: gnuplot.py,v 1.8 2005/09/01 14:45:57 jwliu Exp $'
