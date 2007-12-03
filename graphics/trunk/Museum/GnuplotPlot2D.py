''' Displays 2D data using Gnuplot.
Inventory:
    input_file --   string (default=None)
                    Name of file containing data to plot.
    input_list --   list (default=None)
                    List of 2 data lists: in_list = [x, y]
    plot_title --   string (default='X-Y Plot')
                    Title of plot.
    error_bars --   bool (default=False)
                    If True and if len(input_list) > 2,
                    y errorbars will be plotted.

Notes:
If both input_file and input_list are given, input_file data is plotted.
'''
__author__='Victoria Winters'

from pyre.applications.Script import Script
from Numeric import *
import Gnuplot, Gnuplot.funcutils

class Plot2D(Script):
    '''pyre adaption of Jonathan Lin s Plot2D.py code'''
    
    class Inventory(Script.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_file = pyre.inventory.str('input_file', default=None)
        input_list = pyre.inventory.list('input_list', default=None)
        plot_title = pyre.inventory.str('plot_title', default='X-Y Plot')
        error_bars = pyre.inventory.bool('error_bars', default=False)

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_file','input_list','plot_title', 'error_bars']:
                if value.__class__() == '':
                    exec 'self.inventory.'+key+' = "'+value+'"'
                else:
                    exec 'self.inventory.'+key+' = '+str(value)
        return

    def main(self):
        ''' main method: adapted from J. Lin s Plot2D.py '''
        # Pass inventory into non-global variables
        input_file = self.inventory.input_file
        input_list = self.inventory.input_list
        plot_title = self.inventory.plot_title       
        error_bars = self.inventory.error_bars 
        
        # Use Gnuplot to plot the data    
        g = Gnuplot.Gnuplot(debug=1)
        g.title(plot_title)

        # If a file name is given, plot data from input_file
        if input_file != None:
            # Plot y error bars if specified.
            if error_bars:
                g('set data style yerrorbars')
            d = 'plot \'' + input_file +'\''
            g(d)      
        # If a list is given, plot data from input_list
        elif input_list != None:
            input_list = self._convert(input_list)
            # Plot y error bars if specified.
            if error_bars and len(input_list) > 2:
                g('set data style yerrorbars')
                d = Gnuplot.Data(input_list[0], input_list[1], input_list[2])
            else:
                d = Gnuplot.Data(input_list[0], input_list[1])
            g.plot(d)
        # If neither a file nor list is given, say so
        else:
            print 'No file or list of data was given to plot.'

        raw_input('Please press return to continue...\n')  
        return 

    def _convert(self, data):
        '''a list read from the commandline is parsed as ['[1','2','3','4]']
instead of [1,2,3,4,5]; if so, force conversion of list items to floats'''
        if (data != []) and (data[0].__class__() == ''):
            z = []
            y = []
            for x in data:
                islist = True
                if x[0] == '[': y = []
                try:
                    y.append(float(x.lstrip('[').rstrip(']')))
                except:
                    w = x.lstrip('[').lstrip('"').lstrip("'")
                    w = w.rstrip(']').rstrip('"').rstrip("'")
                    z.append(w)
                    islist = False
                if (x[-1] == ']') and (islist): z.append(y)
            data = z
        return data

    def __init__(self, name='Plot2D', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        return

    def help(self):
        print __doc__
        return

# main
if __name__ == '__main__':
    '''begin journaling services to log input/output/errors,
    then run doTransformation'''

    import journal
    # plot with no data given.
    plt = Plot2D('test_plt')
    print "Instance of Plot2D class created"
    journal.debug('test_plt').activate()
    plt.run()

##     # plot with list given.
##     x = range(10)
##     y = x
##     l = [x, y]
##     e = [1, 1, 2, 1, 1, 2, 2, 1, 3, 1]
##     plt2 = Plot2D('test_plt2', input_list=l)
##     print "Instance of Plot2D class created"
##     journal.debug('test_plt2').activate()
##     plt2.run()
    
##     # plot list with error_bars=True, but none given
##     plt4 = Plot2D('test_plt4', input_list=l, error_bars=True)
##     print "Test List with No Error List"
##     plt4.run()

##     # plot list with error bars:
##     m = [x, y, e]
##     plt3 = Plot2D('test_plt3', input_list=m, error_bars=True)
##     print "Test List with Error Bars"
##     plt3.run()
    
