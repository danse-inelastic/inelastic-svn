#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 11/24/2004 version 0.0.1b
# mmckerns@caltech.edu
# (C) 2004 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'

from pyre.applications.Application import Application
from pyIDL import idl

class PyreIDLsp(Application):
    '''pyre idl application
Inventory:
  input_list -- list (default=None)
Notes:
  input_list is [x,y,error] for 'plot' (error optional)
  input_list is composed of lists of StdVectors
'''
    class Inventory(Application.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory    #for pythia0.6
        input_list = pyre.inventory.list('input_list', default=None)
#       return

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_list']:
                self.inventory.input_list = value
        return

    def run(self):
        '''create idl scatter plot'''
        inputs = self.inventory.input_list
        ## Place input vectors into IDL
        if inputs[0].__class__.__name__ == 'list':
            self.idl.put('x_values',inputs[0])
        else:
            raise TypeError,'First input must be a list'
        if inputs[1].__class__.__name__ == 'list':
            self.idl.put('y_values',inputs[1])
        else:
            raise TypeError,'Second input must be a list'
        if len(inputs) == 3 and inputs[2].__class__.__name__ == 'list':
            self.idl.put('y_errs',inputs[2])
            haveErrs = True
        else:
            haveErrs = False
        print 'Moved data sets to IDL, haveErrs =',haveErrs
        if haveErrs:
            self.idl.eval('plot, x_values, y_values, psym = 2')
            self.idl.eval('errplot, x_values, y_values + y_errs, y_values - y_errs')
        else:
            self.idl.eval('plot, x_values, y_values')

        raw_input('Please press enter to continue')
        return

    def __init__(self, name='PyreIDLsp', **kwds):
        '''instantiate the application, and pass any keywords to config'''
        Application.__init__(self, name)
        self.config(**kwds)
        self.idl = idl()
        return

    def help(self):
        print self.__doc__
        return

# main
if __name__ == '__main__':
    '''begin journaling services, and then run the main code block'''
#   import journal
    mp = PyreIDLsp('test')  #instance of class PyreIDLsp (named 'test')
#   journal.debug('test').activate()  #activate journal for 'test'
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
#   err = [0.2, 0.2, 0.2, 0.2, 0.2]
    mp.config(input_list=[x,y])
    mp.main()  #launch the main code block ('PyreIDLsp.run')

# version
__id__ = "$Id: PyIDL_ScatterPlot.py 227 2007-09-25 16:33:11Z brandon $"

# End of file 

