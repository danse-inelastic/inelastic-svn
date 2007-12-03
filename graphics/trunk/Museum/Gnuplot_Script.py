'''Launches Gnuplot 'interactive' mode
uses standard gnuplot shell commands

Inventory:
    input_list      list (default=None)
                    List containing lists of data (or function) to plot.
    set_commands    string (default='')
                    Gnuplot command line commands to control plot properties.
    plot_style      string (default='Line') 
                    Gnuplot plottype string ('Line' or 'Grid')

Errors:
    Data in list form cannot be replotted interactively.
    (As far as I can tell.)

Notes:
    Data should be in the form [[0,1,2,3],[0,1,4,9],'y*sin(x)'],
    where if a function is included it will be the last list element.
    SetCommands should be in the form 'set data style lines; set hidden'.
    SetCommands, PlotType, and filename are optional, with PlotType set
    to "Line" as default.
'''
__author__='mmckerns'
__version__='1.0'

from pyre.applications.Script import Script
from Numeric import *
import Gnuplot, Gnuplot.funcutils

class GnuplotScript(Script):
    ''' Pyre adaption of mmckerns Gnuplot_Script.py code'''

    class Inventory(Script.Inventory):
        ''' Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_list = pyre.inventory.list('input_list', default=None)
        set_commands = pyre.inventory.str('set_commands', default='')
        plot_style = pyre.inventory.str('plot_style', default='Line')

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_list','set_commands','plot_style']:
                if value.__class__() == '':
                    exec 'self.inventory.'+key+' = "'+value+'"'
                else:
                    exec 'self.inventory.'+key+' = '+str(value)
        return

    ### BEGIN MAIN CODE BLOCK ###
    def main(self):
        ''' main method: adapted from mmckerns Gnuplot_Script.py'''
        # Pass inventory into non-global variables
        g_data = self.inventory.input_list
        g_commands = self.inventory.set_commands
        plot_style = self.inventory.plot_style

        # Feed to Gnuplot
        g = Gnuplot.Gnuplot(debug=1)
        g(g_commands)

        # If there is one list entry, plot it as a function
        if len(g_data) == 1:
            try:
                g('f(x) = '+g_data[0])
            except:
                print "Error: improper data format"
                return 0
        # If there are two list entries, plot as X-Y data
        elif len(g_data) == 2:
            x = g_data[0]
            y = g_data[1]
            try:
                d = Gnuplot.Data(x,y)
            except:
                try:
                    exec 'func = lambda x : '+y
                    d = Gnuplot.funcutils.compute_Data(x,func)
                except:
                    print "Error: improper data format"
                    return 0
            g('plot '+d.command())
        # If there are three list entries, plot as 3-D data
        elif len(g_data) == 3: 
            if plot_style == 'Grid':
                x = g_data[0]
                y = g_data[1]
                z = g_data[2]
                try:
                    exec 'func = lambda x,y : '+z
                    d = Gnuplot.funcutils.compute_GridData(x,y,func, binary=0)
                except:
                    print "Error: improper data format"
                    return 0
            else:
                    x = g_data[0]
                    y = g_data[1]
                    z = g_data[2]
                    try:
                        d = Gnuplot.Data(x,y,z)
                    except:
                        print "Error: improper data format"
                        return 0
            g('splot '+d.command())
        else:
            pass

        g.interact()
        g.reset()

        return 1
        ### END MAIN CODE BLOCK ###    


    def __init__(self, name='GnuplotScript', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        return
    
    def help(self):
        print __doc__
        return

if __name__ == '__main__':

    # Function Test
    # Input Format: ['function'] -or- 'function' also works
    f = 'sin(x)'
    l_f = [f]
    gs = GnuplotScript('test_gs', input_list=l_f)
    print "~~~~~~~~~~~~"
    print "Function Test"
    gs.run()
    
    # 2D Test
    # Input Format: [[x_data], [y_data]]
    x = range(20)
    y = x
    l = [x, y]
    gs1 = GnuplotScript('test_gs1', input_list=l)
    print "~~~~~~~~~~~~"
    print "2D Plot Test"
    gs1.run()

    # 3D Test
    # Input Format: [[x_data], [y_data], [z_data]]
    m = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,4,9,14,25],]
    gs2 = GnuplotScript('test_gs2', input_list=m, output_file='3D_output.ps')
    gs2.config(set_commands='set data style lines')
    print "~~~~~~~~~~~~"
    print "3D Test"
    gs2.run()

    # 3D Grid Test
    # Input Format: [[x_data], [y_data], 'function']
    m = [[0,1,2,3,4,5],[0,1,2,3,4,5],'y*sin(x)',]
    gs3 = GnuplotScript('test_gs3', input_list=m, plot_style='Grid')
    gs3.config(set_commands='set pm3d; set parametric; set data style lines')
    print "~~~~~~~~~~~~"
    print "3D Grid Test"
    gs3.run()
