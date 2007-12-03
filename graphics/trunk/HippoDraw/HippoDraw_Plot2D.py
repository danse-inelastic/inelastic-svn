__doc__=''' Displays 2D data using HippoDraw.
HippoDraw must be installed and callable from python.

Inventory:
    input_file --   string (default=None)
                    Name of file containing data to plot.
                    Must be in HippoDraw '.tnt' format.
    input_list --   list (default=None)
                    List of 2 data lists: in_list = [x, y]
    plot_title --   string (default='X-Y Plot')
                    Title of plot.
    error_bars --   bool (default=False)
                    If True and if len(input_list) > 2,
                    y errorbars will be plotted.

Notes:
Will Seg Fault if more than one HippoPlot2D objects are created.
        
If both input_file and input_list are given, input_file data is plotted.

Application will not work if input_file is not in ASCII file format for NTuple.
The proper format for input_file is:
    * ends in '.tnt'
    * first line of file is the title
    * second line of file contains tab-separated labels for each data column
    * the remaining lines are n column data
'''
__author__='Victoria Winters'

from pyre.applications.Script import Script
from Numeric import *

class HippoPlot2D(Script):
    '''pyre application to create a x-y plot in HippoDraw'''
    
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


    # The method get_labels gets the data column labels from the
    # second line of the input file
    def get_labels(self, input_file=None):
        import string
        
        f = open(input_file, 'r')
        first_line = f.readline()
        second_line = f.readline()
        f.close()
        
        labels = string.split(second_line, '\t')

        # Remove '\n' from the last label:
        last_label = labels.pop()
        last_label = string.strip(last_label, '\n')
        labels.append(last_label)
        
        return labels    


    # Make sure input_file is in HippoDraw .tnt format and contains
    # enough data columns for the requested plot type.    
    def check_file_format(self, input_file=None, error_bars=None, labels=None):
        if input_file[-4:] != '.tnt':
            print "Input file name must end in '.tnt'."

        if len(labels) < 3 and error_bars:
            print "Three labeled columns of data are required", \
                  "for XY Plot with error bars."
            print "Only", len(labels), "label(s) in", input_file,\
                  ":", labels
            print "Note: labels must be on 2nd line, separated by tabs."

        elif len(labels) < 2:
            print "Two labeled columns of data are required", \
                  "for XY Plot without error bars."
            print "Only", len(labels), "label(s) in", input_file,\
                  ":", labels
            print "Note: labels must be on 2nd line, separated by tabs."
            
        else:
            print "Could not create a HippoDraw xy display object from", \
                  input_file
            
        return


    # Open HippoDraw and draw the xy display object on the canvas.
    def plot_xy(self, plot_title=None, xy=None):
        # Set the plot title.
        xy.setTitle(plot_title)

        # Get a HippoDraw Canvas
        from hippo import HDApp
        app = HDApp()
        canvas = app.canvas()

        # Display the xy plot.
        canvas.addDisplay(xy)

        return

    ### BEGIN MAIN CODE BLOCK ###
    def main(self):
        ''' main method: create an XY plot in HippoDraw '''
        # Pass inventory into non-global variables
        input_file = self.inventory.input_file
        input_list = self.inventory.input_list
        plot_title = self.inventory.plot_title       
        error_bars = self.inventory.error_bars 

        from hippo import Display

        # If a file name is given, make an xy display object from input_file
        if input_file != None:

            # Get a list of labels from the second line of input_file
            labels = self.get_labels(input_file)
        
            # Create an ntuple from the input file
            from hippo import NTupleController
            ntc = NTupleController.instance()
            input_nt = ntc.createNTuple(input_file)
            
            # Create the xy display object with or without error bars.
            if error_bars:
                try:
                    xy = Display('XY Plot', input_nt, (labels[0], labels[1], \
                                                   'nil', labels[2]) )
                    # Open HippoDraw and draw the xy display object
                    self.plot_xy(plot_title, xy)
                except:
                    self.check_file_format(input_file, error_bars, labels)
            else:
                try:
                    xy = Display('XY Plot', input_nt, (labels[0], labels[1]) )
                    # Open HippoDraw and draw the xy display object
                    self.plot_xy(plot_title, xy)
                except:
                    self.check_file_format(input_file, error_bars, labels)
    
        # If a list is given instead of a file, create an xy display
        # object from input_list
        elif input_list != None:

            self._convert()
            print self.data

            # Create the xy display object with error bars.
            if error_bars and len(self.data) > 2:
                xy = Display('XY Plot', [self.data[0], self.data[1],
                                         self.data[2]],
                             ['X', 'Y', 'nil', 'error'])
                # Open HippoDraw and draw the xy display object on the canvas.
                self.plot_xy(plot_title, xy)
                
                # Create the xy display object without error bars.
            elif len(self.data) > 1:
                xy = Display('XY Plot', [self.data[0], self.data[1]],
                             ['X', 'Y'])
                
                # Open HippoDraw and draw the xy display object on the canvas.
                self.plot_xy(plot_title, xy)

            else:
                print "input_list only contains", len(self.data),\
                      "list(s) of data."

        # If neither a file nor list is given, say so and exit program.
        else:
            print 'No file or list of data was given to plot.'
            return
            

            
        raw_input('Please press return to continue...\n')  

        return
        ### END MAIN CODE BLOCK ###
    

    def _convert(self):
        '''a list read from the commandline is parsed as ['[1','2','3','4]']
instead of [1,2,3,4,5]; if so, force conversion of list items to floats'''
        input_list = self.inventory.input_list
        z = []
        y = []
        if (input_list != []) and (input_list[0].__class__() == ''):
            for x in input_list:
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
            self.inventory.input_list = z
        self.data = self.inventory.input_list
        return self.data

    def __init__(self, name='Plot2D', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        self.data = []
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
    hp2D = HippoPlot2D('test_hp2D')
    print "Instance of HippoPlot2D class created"
    journal.debug('test_plt').activate()
    hp2D.run()
'''
    # plot with list given.
    x = range(10)
    y = x
    l = [x, y]
    e = [1, 1, 2, 1, 1, 2, 2, 1, 3, 1]
    
    hp2D2 = HippoPlot2D('test_hp2D2', input_list=l, \
                        plot_title="X Y Plot Title")
    print "Instance of Plot2D class created"
    journal.debug('test_hp2D2').activate()
    hp2D2.run()

    # plot list with error bars:
    m = [x, y, e]
    hp2D3 = HippoPlot2D('test_hp2D3', input_list=m,
                        plot_title="X Y Plot with Error Bars", error_bars=True)
    print "Test List with Error Bars"
    hp2D3.run()
    
    # plot list with error_bars=True, but none given
    hp2D4 = HippoPlot2D('test_hp2D4', input_list=l, error_bars=True)
    print "Test List with No Error List"
    hp2D4.run()
'''
