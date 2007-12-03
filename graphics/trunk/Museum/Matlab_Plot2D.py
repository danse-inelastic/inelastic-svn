'''displays an x-y plot with Matlab
data is retrieved from the stream,
and sent directly to Matlab through
sam (Simple API for Matlab).
Pyre adaption of mmckerns's Matlab_Plot2D.py cobra component.

Inventory:
    input_list --   list (default=None)
                    List containing lists of data to plot.

Notes
    Both Matlab and sam must be installed,
    and Matlab must be able to find a license.
    invokes sam.eval("plot(x,y,'k-','Linewidth',2)")
'''
__author__='Victoria Winters'


from pyre.applications.Application import Application
import sam

class MatlabPlot2D(Application):
    '''Pyre adaption of mmckerns Matlab_Plot2D.py cobra component'''

    class Inventory(Application.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory       # for pythia-0.6
        input_list = pyre.inventory.list('input_list', default=None)

    def config(self, **kwds):
        '''config modifies Inventory variables'''
        for key, value in kwds.items():
            if key == 'input_list':
                self.inventory.input_list = value

    ### BEGIN MAIN CODE BLOCK ###
    def run(self):
        '''main method: adapted from mmckerns Matlab_Plot2D2.py'''
        input_list = self.inventory.input_list

        #open a matlab session
        sam.eval("")
        
        #put the variables into the matlab workspace
        sam.put("x",input_list[0])
        sam.put("y",input_list[1])

        #check if put worked
        sam.tools.whos()

        #create an 2d plot
        sam.eval("plot(x,y,'k-','Linewidth',2)")
        sam.eval("title('X-Y Plot')")

        raw_input('Please press return to continue...\n')

        return 1
        ### END MAIN CODE BLOCK ###


    def __init__(self, name='MatlabPlot2D', **kwds):
        ''' Instantiate the application and pass any keywords to config. '''
        Application.__init__(self, name)
        self.config(**kwds)
        return

    def help(self):
        print __doc__
        return

if __name__ == '__main__':

    # Test
    x = [1, 2, 3, 4, 5, 6]
    y1 = [1, 4, 9, 16, 25, 36]
    y2 = [11, 12, 13, 14, 15, 16]
    l = [x, y1]
    mp2d = MatlabPlot2D(input_list=l)
    print "~~~~~~~~~~~~~~~~~~"
    print "MatlabPlot2D Test"
    mp2d.main()
