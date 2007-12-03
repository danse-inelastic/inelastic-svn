#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import threading

class PWorkThread(threading.Thread):
    """A simple class provide a single thread to update the graphic
       window"""
    def __init__ ( self, graph, fname, name = "Plot2DThread"):
        threading.Thread.__init__(self, name=name)
        self.graph = graph
        self.fname = fname
        self.running = True
        
    def run(self):
        if self.fname == '-':
            self.defaultTest()
        else:
            pass
    
    def defaultTest(self):
        # First insert the curve to the plot
        import math
        import demoplot.curve
        x = range(1,500,10)
        y = [ math.cos(a)*1000 for a in x] 
        curve = demoplot.curve.Curve('TestData')
        curve.changeStyle( self.graph.buildLineStyle())
        curve.setX(x)
        curve.setY(y)
        self.graph.addCurve(curve)
        
        y2 = [ a * 2 for a in y ]
        curve2 = demoplot.curve.Curve('Test2')
        curve2.changeStyle(self.graph.buildSymbolStyle())
        curve2.setX(x)
        curve2.setY(y2)
        self.graph.addCurve(curve2)
        
        # Now generate new data every second.
        for n in range(1,10,1):
            if not self.running:
              return
            import time
            time.sleep(1)
            x = range (1, 500*n, 10)
            y = [(math.sin(a*n))*1000 for a in x]
            style = self.graph.buildSymbolStyle() 
            style['legend'] = "CURVE-%d"%n 
            curve2.changeStyle(style)
            curve2.setX(x)
            curve2.setY(y)
            self.graph.changeCurveStyle(curve2)
            self.graph.updateCurveData(curve2)

def main():

    from pyre.applications.Script import Script
    from graphics.plot2D.MatplotlibPlot import MatPlot 
    from graphics.plot2D.GnuPlot import GnuPlot
    from graphics.plot2D.QwtPlot import QwtPlot


    class Plot2DApp(Script):


        class Inventory(Script.Inventory):

            import pyre.inventory as inv
            plot = inv.facility('plot',default=QwtPlot())#GnuPlot())#MatPlot())#'gnuplot')
            plot.meta['tip'] = 'Plotting facility'
            #plot.validator = inv.choice(['matplotlib','gnuplot','qwtplot'])
            filename = inv.str('filename', default='-')
            filename.meta['tip'] = 'File to be read from'

        def main(self, *args, **kwds):
            print 'Start'
            self.i=self.inventory
            self.plot = self.i.plot
            workThread = PWorkThread(self.plot,self.filename)
            self.plot.setLabels('This is a graph', 'This is x', 'This is y')
            workThread.start()
            self.plot.setSize(800,600)
            self.plot.display()
            workThread.running = False
            workThread.join()

        def __init__(self):
            Script.__init__(self, 'demoplot')
            return


        def _defaults(self):
            Script._defaults(self)
            return


        def _configure(self):
            Script._configure(self)
            #self.plot =self.inventory.plot
            self.filename = self.inventory.filename
            return


        def _init(self):
            Script._init(self)
            return


    app = Plot2DApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: simple.py,v 1.8 2006/01/24 16:07:35 jwliu Exp $"

# Generated automatically by PythonMill on Fri May 20 11:06:21 2005

# End of file 
