#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#Created by:  Jiwu Liu (jliu@pa.msu.edu)
#description: Plotting class using Qwt lib. This is a pyre component class
#<LicenseText>
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


from qt import *

import graphics.plot2D.common.Qtinit 

from graphics.plot2D.Plot2D import Plot2D

class QwtPlot(Plot2D):
    """Plotting with Qwt module
    Unfortunately, it happens to have the same class name with qwt.QwtPlot
    But no clash really take place"""
    def __init__(self, name = None):
        if name is None: name = 'QwtPlot'
        
        Plot2D.__init__ (self, name)
        from graphics.plot2D.qwt.PQwtView import PQwtView    
        self.window = PQwtView(name=name)
        
        #self.width = self.window.size().width()
        #self.height = self.window.size().height()
        
    def setLabels(self, title, x, y ):
        # call superclass.setLabels
        Plot2D.setLabels(self,title,x,y)
        
        # Really set the window
        self.window.qwtPlot1.setTitle(title)
        import qwt
        self.window.qwtPlot1.setAxisTitle(qwt.QwtPlot.xBottom, x)
        self.window.qwtPlot1.setAxisTitle(qwt.QwtPlot.yLeft, y)
    
    def setSize(self, width, height):        
        #call superclass.setSize
        Plot2D.setSize(self, width, height)
        
        qApp.lock()
        self.window.resize(QSize(width,height))
        qApp.unlock()        


    def display(self):
        qApp.setMainWidget(self.window)
        self.window.show()
        qApp.exec_loop()
        
    def _insert(self,data,style ):
        curveRef = self.window.qwtPlot1.insertCurve(style['legend'])
        self.__setCurveStyles(curveRef,style)
        self.window.qwtPlot1.setCurveData(curveRef, data['x'], data['y'])
        self.redraw()
        return curveRef
    
    def _updateData(self, curveRef, data):
        self.window.qwtPlot1.setCurveData(curveRef, data['x'], data['y'])
        self.redraw()
       
    def _changeStyle(self, curveRef, style):
        self.__setCurveStyles(curveRef, style)
        self.redraw()
        
    def _remove(self, curveRef):
        self.window.qwtPlot1.removeCurve(curveRef)
        self.redraw()
        
    def __setCurveStyles(self, curveRef, style):
        """Function to deal with various plotting options"""
        #Convert the initial character to upper case which is Qwt's convention
        def I2U(s):
            # Special code for symbol='square'
            if s=='square': return 'Rect'
            return s[:1].upper() + s[1:] 

        # For now, we parse only simple properties
        import qwt
        color = getattr(Qt, style['color'], Qt.black)
        width = style['width']
        line = getattr(Qt, I2U(style['line'])+'Line',Qt.SolidLine) 
        symbol = getattr(qwt.QwtSymbol, I2U(style['symbol']), qwt.QwtSymbol.Diamond )
        symbolSize = style['symbolSize']
        symbolColor = getattr(Qt,style['symbolColor'],Qt.black)
        with = getattr(qwt.QwtCurve, I2U(style['with']), qwt.QwtCurve.Lines)
        legend = style['legend']
        
        #Speical code to deal with option-"with":
        if style['with'] == 'points':
            with = qwt.QwtCurve.NoCurve
        else: 
            if style['with'] != 'linespoints':
                symbol = qwt.QwtSymbol.None
                
        #Allocate a  Pen
        pen = QPen (color,width,line)
        brush = QBrush (symbolColor )
        size = QSize ( symbolSize,symbolSize)
        qSymbol = qwt.QwtSymbol(symbol, brush, pen, size )
        
        #Set pen, style and symbol
        qApp.lock()
        #self.window.qwtPlot1.enableLegend(curveRef)
        self.window.qwtPlot1.setCurvePen(curveRef, pen)
        self.window.qwtPlot1.setCurveStyle(curveRef, with)
        self.window.qwtPlot1.setCurveSymbol(curveRef, qSymbol)
        self.window.qwtPlot1.setCurveTitle(curveRef, legend)
        qApp.unlock()
    
    def redraw(self):
        """Inform Qt graphics to draw the graph again""" 
        qApp.lock()
        self.window.qwtPlot1.replot()
        qApp.unlock()
        
if __name__ == '__main__':
    g = QwtPlot('test')
    g.display()
    
__id__="$Id: qwtplot.py,v 1.10 2005/09/01 14:47:20 jwliu Exp $"
