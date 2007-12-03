#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 3/15/2005 version 0.0.2a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__=''' Displays 2D data using pgplot.
Inventory:
    input_list --   list (default=None)
    plot_title --   string (default='X-Y Plot')
    plot_type --    string (default='data')
    output_type --  string (default='?')

Input_list is x,y data points, functions, or range
Plot_type is either 'data', 'line', or 'contour'
Output_type is '?', '/NULL', '/XWINDOW', '/GIF', '/PS', or '/CPS'

If 'plot_type' is 'data' or 'line':
  x is a list, y can be either a list or a function of x
If 'plot_type' is 'contour':
  x and y lists are to obtain xmin,xmax and ymin,ymax; z is a function of x & y
'''

from pyre.applications.Script import Script
from Numeric import *
from ppgplot import *

class pgplot2D(Script):
    '''simple pyre application for ppgplot'''
    class Inventory(Script.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_list = pyre.inventory.list('input_list', default=None)
        plot_title = pyre.inventory.str('plot_title', default='X-Y Plot')
        plot_type = pyre.inventory.str(
                    'plot_type', default='data',
                    validator=pyre.inventory.choice(['data','line','contour']))
        output_type = pyre.inventory.str(
                    'output_type', default='?',
                    validator=pyre.inventory.choice(['?','/NULL','/XWINDOW','/GIF','/PS','/CPS']))

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_list','plot_title','plot_type','output_type']:
                if value.__class__() == '':
                    exec 'self.inventory.'+key+' = "'+value+'"'
                else:
                    exec 'self.inventory.'+key+' = '+str(value)
        return

    def main(self, *args, **kwds):
        '''main method: use ppgplot to make a data or line graph'''
        # Pass inventory into non-global variables
        input_list = self.inventory.input_list
        plot_title = self.inventory.plot_title        
        plot_type = self.inventory.plot_type     
        output_type = self.inventory.output_type     
        
        # Set graphics type
        pgopen(output_type)

        # If a list is given, plot data from input_list
        if input_list != None:
            self.data = input_list
            self._NumericArray()
            self._getbounds()
            pgenv(self.min[0],self.max[0],self.min[1],self.max[1],0,1)
            pglab('(x)','(y)',plot_title)
            #set plot type
            if plot_type == 'data':
                pgpt(self.data[0], self.data[1], 9)
            elif plot_type == 'line':
                pgline(self.data[0], self.data[1])
            elif plot_type == 'contour':
                self._getsurf()
                pggray_s(self.surf)
                pgsci(2)
                pgcont_s(self.surf,10)
                pgsci(1)
                pgwedg_s(max(ravel(self.surf)),min(ravel(self.surf)), "RG")
            else:
                print 'Plot type %s not understood' % plot_type
                raise
        # If a list is not given, say so
        else:
            print 'No data was given to plot.'
            # raise
        pgend()
        return 

    def _NumericArray(self):
        '''convert list or function to Numeric array'''
        for i in range(len(self.data)):
            if self.data[i].__class__() == []:
                self.data[i] = array(self.data[i])
            elif self.data[i].__class__() == '':
                x = self.data[0]
                y = self.data[1]
                self.func.append(self.data[i])
                exec 'self.data[i] = array('+self.data[i]+')'
            else:
                print "Error: unknown data type"
                raise
        return

    def _getbounds(self):
        '''get x,y range'''
        for i in range(2):
            self.min[i] = min(self.data[i])
            self.max[i] = max(self.data[i])
        return

    def _getsurf(self):
        '''prepare contour surface'''
        xmin = int(self.min[0])
        xmax = int(self.max[0])
        ymin = int(self.min[1])
        ymax = int(self.max[1])
        self.surf = zeros([xmax-xmin,ymax-ymin],Float32)
        for x in range(xmin,xmax):
            for y in range(ymin,ymax):
                i = x-xmin
                j = y-ymin
                exec 'self.surf[i,j] = '+self.func[-1]
        return

    def __init__(self, name='pgplot2D', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        self.data = []
        self.min = [0,0]
        self.max = [10,10]
        self.func = []
        self.surf = []
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
    plt = pgplot2D('test_plt')
    print "Instance of pgplot2D class created"
    journal.debug('test_plt').activate()
    #Examples
#   vtkBackend.config(input_list=[[-5,5],[-5,5],'cos(y)+sin(x)'],plot_type='contour')
#   vtkBackend.run()
#   vtkBackend.config(input_list=[[1,2,3,4,5],'x*x'],plot_type='line')
#   vtkBackend.run()
#   vtkBackend.config(input_list=[[1,2,3,4,5],[1,4,9,16,25]],plot_type='data')
    vtkBackend.run()
