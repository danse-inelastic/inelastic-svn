__doc__=''' Displays data using HippoDraw.
HippoDraw must be installed and callable from python.

Inventory:
    input_file --   string (default=None)
                    Name of file containing data to plot.
                    Must be in HippoDraw '.tnt' format.
    input_list --   list (default=None)
                    List of data lists. Example: in_list = [[1,2,3], [2,3,4]]
    plot_title --   string (default=None)
                    Title of plot. If none, plot_type will be used.
    plot_type  --   string (default=None)
                    Type of HippoDraw Plot
    cols_to_plot -- list (default=[])
                    Column index (with input_list) or label (input_file) of
                    column to be plotted. Useful if not all data in input
                    is necessary for reqested plot. By default the first
                    1,2, or 3 columns are used, depending on how many are
                    necessary.

Notes:
Will Seg Fault if more than one HippoPlot objects are created.
        
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

class HippoPlot(Script):
    '''pyre application to create a x-y plot in HippoDraw'''
    
    class Inventory(Script.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_file = pyre.inventory.str('input_file', default=None)
        input_list = pyre.inventory.list('input_list', default=None)
        plot_title = pyre.inventory.str('plot_title', default=None)
        plot_type = pyre.inventory.str('plot_type', default=None)
        cols_to_plot = pyre.inventory.list('cols_to_plot', default=[])

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
    def check_file_format(self, input_file, labels, num_cols, plot_type):
        if input_file[-4:] != '.tnt':
            print "Input file name must end in '.tnt'."
        else:
            print "Could not create a HippoDraw", plot_type, \
                  "display object from", input_file          
        return


    # Open HippoDraw and draw the display object on the canvas.
    def plot(self, plot_title, display_obj):

        # Set the plot title.
        display_obj.setTitle(plot_title)

        # Get a HippoDraw Canvas
        from hippo import HDApp
        app = HDApp()
        canvas = app.canvas()

        # Draw the display object.
        canvas.addDisplay(display_obj)

        return

    # If the requested plot_type is valid, return the number of data
    # columns it takes. Otherwise return 0.
    def num_columns(self, plot_type):

        # Make a dictionary of valid plot types and the number of
        # data columns they take
        num_cols = {'Histogram': 1, 'Color Plot': 2, 'Contour Plot': 2,
                    'Profile': 2, 'Profile 2D': 3, 'Profile Contour': 3,
                    'Scatter Plot': 2, 'Strip Chart': 2, 'XY Plot': 2,
                    'XYZ Plot': 3, 'Y Plot': 1, 'Z Plot':1}

        if plot_type in num_cols.keys():
            return num_cols[plot_type]

        else:
            print "plot_type", plot_type, "is not valid"
            print "Valid plot types are:"
            print num_cols.keys()
            return 0

    # make_label_tuple makes a tuple of labels corresponding to the
    # columns to plot when the input is in file form.
    def make_label_tuple(self, labels, num_cols, cols_to_plot):
        ctp_valid = False
        if num_cols == len(cols_to_plot):
            cols_valid = True
            a = []
            for col in cols_to_plot:
                if col in labels:
                    a.append(col)
                else:
                    cols_valid = False
            if not cols_valid:
                print "The colums to plot", cols_to_plot
                print "are not in the file labels:", labels
            if cols_valid:
                return tuple(a)
             
        # If the wrong labels or number of columns were specified, use
        # columns in the order they are listed in the file.
        if not cols_valid:
            if len(cols_to_print) != num_cols:
                print num_cols, "columns are required.", len(cols_to_plot),\
                      "columns were given:", cols_to_plot
            a = []
            for i in range(num_cols):
                a.append(labels[i])
            return tuple(a)

    # make_label_list makes a list of column numbers to plot when the
    # input is in list form.
    # def make_label_list(self, num_cols, cols_to_plot):


    ### BEGIN MAIN CODE BLOCK ###
    def main(self):
        ''' main method: create a plot in HippoDraw '''
        # Pass inventory into non-global variables
        input_file = self.inventory.input_file
        input_list = self.inventory.input_list
        plot_title = self.inventory.plot_title       
        plot_type = self.inventory.plot_type

        num_cols = self.num_columns(plot_type)

        # If no title is give, use plot_type
        if not plot_title:
            plot_title = plot_type

        from hippo import Display

        # If a file name is given, make a display object from input_file
        if input_file != None:

            # Get a list of labels from the second line of input_file
            labels = self.get_labels(input_file)
            
            # End the program if there are not enough columns to make
            # the requested plot.
            if len(labels) < num_cols:
                print num_cols, "labeled columns of data are required", \
                      "for", plot_type
                print "Only", len(labels), "label(s) in", input_file,\
                      ":", labels
                print "Note: labels must be on 2nd line, separated by tabs."
                return
        
            # Create an ntuple from the input file
            from hippo import NTupleController
            ntc = NTupleController.instance()
            input_nt = ntc.createNTuple(input_file)

            label_tuple = self.make_label_tuple(labels, num_cols, cols_to_plot)
            try:
                display_obj = Display(plot_type, input_nt, label_tuple)
                # Open HippoDraw and draw the display object
                self.plot(plot_title, display_obj)
            except:
                self.check_file_format(input_file, labels, num_cols, plot_type)

        # If a list is given instead of a file, create a display
        # object from input_list
        elif input_list != None:

            self._convert()
            print self.data

            if num_cols == 0:
                return
            
            elif len(self.data) >= num_cols:
                data_list = []
                axis_labels = []
                for i in range(num_cols):
                    data_list.append(self.data[i])
                    if i == 0:
                        axis_labels.append('X')
                    if i == 1:
                        axis_labels.append('Y')
                    if i == 2:
                        axis_labels.append('Z')

                display_obj = Display(plot_type, data_list, axis_labels)
                
                # Open HippoDraw and draw the display object on the canvas.
                self.plot(plot_title, display_obj)

            else:
                print "input_list only contains", len(self.data),\
                      "list(s) of data."
                print num_cols, "lists of data are required", \
                      "for the plot type", plot_type

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

    def _defaults(self):
        Script._defaults(self)
        return

    def _configure(self):
        Script._configure(self)
        return

    def _init(self):
        Script._init(self)
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
    hp = HippoPlot('test_hp')
    print "Instance of HippoPlot class created"
    journal.debug('test_hp').activate()
    hp.run()

'''
    # plot with list given.
    x = range(10)
    y = x
    l = [x, y]
    e = [1, 1, 2, 1, 1, 2, 2, 1, 3, 1]
  
    hp2D2 = HippoPlot('test_hp2D2', input_list=l, plot_type='XY Plot', \
                       plot_title="X Y Plot Title")
    print "Instance of Plot2D class created"
    journal.debug('test_hp2D2').activate()
    hp2D2.run()

    # plot list with error bars:
    m = [x, y, e]
    hp2D3 = HippoPlot('test_hp2D3', input_list=m, plot_type='XY Plot', \
                       plot_title="X Y Plot with Error Bars", error_bars=True)
    print "Test List with Error Bars"
    hp2D3.run()
    
    # plot list with error_bars=True, but none given
    hp2D4 = HippoPlot('test_hp2D4', input_list=l, error_bars=True)
    print "Test List with No Error List"
    hp2D4.run()
'''
