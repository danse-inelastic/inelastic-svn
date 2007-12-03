'''Displays data with Gnuplot.
Creates 2D data plot, 3D data plot, or 3D grid plot.
Adapted from mmckerns's Cobra component Gnuplot_Plot.py.

Inventory:
    input_list   -- list (default=None)
                    List containing lists of data to plot.
    set_commands -- string (default='')
                    Gnuplot command line commands to control plot properties.
    plot_style   -- string (default='Line')
                    Gnuplot plottype string ('Line' or 'Grid')
    output_file  -- string (default=None)
                    Output file name. If it ends in '.ps' the Gnuplot graph
                    will be written to that file. Otherwise nothing will be
                    written.

Notes:
    Data should be in the form [[0,1,2,3],[0,1,4,9],'y*sin(x)'],
    (for this input_list, plot_style='Grid' needs to be set)
    where if a function is included it will be the last list element.
    SetCommands should be in the form 'set data style lines; set hidden'.
    SetCommands, PlotType, and filename are optional, with PlotType set
    to "Line" as default.
'''
__author__='Victoria Winters'

from pyre.applications.Script import Script
from Numeric import *
import Gnuplot, Gnuplot.funcutils

class GnuplotPlot(Script):
    ''' Pyre adaption of mmckerns Gnuplot_Plot.py code'''

    class Inventory(Script.Inventory):
        ''' Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_list = pyre.inventory.list('input_list', default=None)
        set_commands = pyre.inventory.str('set_commands', default='')
        plot_style = pyre.inventory.str('plot_style', default='Line')
        output_file = pyre.inventory.str('output_file', default=None)

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_list','set_commands','plot_style','output_file']:
                if value.__class__() == '':
                    exec 'self.inventory.'+key+' = "'+value+'"'
                else:
                    exec 'self.inventory.'+key+' = '+str(value)
        return
        
    # Method to plot a function f(x).
    def Gnuplot_Func(self, input_list=None): 
        fx = input_list[0]
        Gnuplot_data = Gnuplot.Func(fx)
        return Gnuplot_data

    # Method to plot 2D data: x,y -or- x,f(x).
    def Gnuplot_2D(self, input_list=None): 
        x = input_list[0]
        fx = input_list[1]
        try:
            Gnuplot_data = Gnuplot.Data(x,fx)
        except:
            exec 'func = lambda x : '+fx
            Gnuplot_data = Gnuplot.funcutils.compute_Data(x,func)
        return Gnuplot_data

    # Method to plot 3D data: x, y, f(x)
    def Gnuplot_3DGrid(self, input_list=None): 
    #   try:
    #       Gnuplot_data = Gnuplot.GridData(input_list,binary=1)
    #   except:
        x = input_list[0]
        y = input_list[1]
        fxy = input_list[2]
        exec 'func = lambda x,y : '+fxy
        Gnuplot_data = Gnuplot.funcutils.compute_GridData(x,y,func,binary=1)
        return Gnuplot_data

    # Method to plot 3D data: x, y, z
    def Gnuplot_3DData(self, input_list=None):
        x = input_list[0]
        y = input_list[1]
        z = input_list[2]
        Gnuplot_data = Gnuplot.Data(x,y,z)
        return Gnuplot_data


    ### BEGIN MAIN CODE BLOCK ###
    def main(self):
        ''' main method: adapted from mmckerns Gnuplot_Plot.py'''
        # Pass inventory into non-global variables
        input_list = self.inventory.input_list
        set_commands = self.inventory.set_commands
        plot_style = self.inventory.plot_style
        output_file = self.inventory.output_file
                
        # Feed to Gnuplot
        g = Gnuplot.Gnuplot(debug=1)

        # Give user-defined commands to Gnuplot 
        g(set_commands)

        # If there is one list entry, plot it as a function
        if len(input_list) == 1:
            g.title('Func Plot')
            try:
                d = self.Gnuplot_Func(input_list)
            except:
                print "Error: improper data format"
                return 0
            if plot_style == 'Grid':
                g.splot(d)
            else:
                g.plot(d)
        # If there are two list entries, plot as X-Y data
        elif len(input_list) == 2:
            g.title('2D Plot')
            try:
                d = self.Gnuplot_2D(input_list)
            except:
                print "Error: improper data format"
                return 0
            g.plot(d)
        # If there are three list entries, plot as 3-D data
        elif len(input_list) == 3: 
            g.title('3D Plot')
            if plot_style == 'Grid':
                try:
                    d = self.Gnuplot_3DGrid(input_list)
                except:
                    print "Error: improper data format"
                    return 0
            else:
                try:
                    d = self.Gnuplot_3DData(input_list)
                except:
                    print "Error: improper data format"
                    return 0
            g.splot(d)

        # Wait for the user to view the plot.
        raw_input('Please press return to continue...\n')

        # If an output file was specified, write the graph to output_file.
        if output_file:
            if output_file[-3:] == '.ps':
                g.hardcopy(output_file,enhanced=1,color=1)
            elif output_file[-4:] == '.txt':
                pass
            #       elif output_file == 'interact':
            #           g.interact()

        g.reset()
        return 1
    ### END MAIN CODE BLOCK ###


    def __init__(self, name='GnuplotPlot', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        return
    
    def help(self):
        print __doc__
        return

if __name__ == '__main__':
    ''' Test the GnuplotPlot class. '''
    import math

    # Function Test
    # Input Format: ['function'] -or- 'function' also works
    f = 'sin(x)'
    l_f = [f]
    gp = GnuplotPlot('test_gp', input_list=l_f)
    print "~~~~~~~~~~~~"
    print "Function Test"
    gp.run()

    # 2D Test
    # Input Format: [[x_data], [y_data]]
    x = range(20)
    y = x
    l = [x, y]
    gp1 = GnuplotPlot('test_gp1', input_list=l)
    print "~~~~~~~~~~~~"
    print "2D Plot Test"
    gp1.run()

    # 3D Test
    # Input Format: [[x_data], [y_data], [z_data]]
    m = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,4,9,14,25],]
    gp2 = GnuplotPlot('test_gp2', input_list=m, output_file='3D_output.ps')
    gp2.config(set_commands='set data style lines')
    print "~~~~~~~~~~~~"
    print "3D Test"
    gp2.run()

    # 3D Grid Test
    # Input Format: [[x_data], [y_data], 'function']
    m = [[0,1,2,3,4,5],[0,1,2,3,4,5],'y*sin(x)',]
    gp3 = GnuplotPlot('test_gp3', input_list=m, plot_style='Grid')
    gp3.config(set_commands='set pm3d; set parametric; set data style lines')
    print "~~~~~~~~~~~~"
    print "3D Grid Test"
    gp3.run()
