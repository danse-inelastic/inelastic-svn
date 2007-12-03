'''launches Gnuplot 'fit' mode
performs nonlinear least-squares Marquardt-Levenberg algorithm
on a function of one or two independant variables

Inventory:
    data_lists  --  list (default=[])
                    List containing lists of x, y, and possibly z data to fit.
    error_list  --  list (default=[])
                    List of standard deviations for the corresponding y value.
                    If the error_list is not the same length as data_lists[0],
                    an error list of 1's will be used for fitting.
    fit_func    --  str (default=None)
                    Function string to be fit.
    fit_param   --  list (default=[])  
                    List of strings defining initial fit parameter values.
                    Example: ['a = 10', 'b = 5.5']
    result_file --  str (default='fit.new')
                    File name where final fit parameter values will be written.
                    The file <result_file>.log (created from 'fit.log') will
                    also be written.

Notes:
    Function can take one or two independant variables (i.e. f(x) or g(x,y))
    paramData should be in the form ['a = 10', 'b = 5.5'].
    The weights for the datum are calculated from the standard deviation
    of the corresponding y value as 1/stddev**2.
    zdata and stddev are optional, with stddev set to "1" as default.
'''
__author__='Victoria Winters'

from pyre.applications.Script import Script
import os
from Numeric import *
import Gnuplot, Gnuplot.funcutils


class GnuplotFit(Script):
    ''' Pyre adaption of mmckerns Gnuplot_Fit.py code'''

    class Inventory(Script.Inventory):
        ''' Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        data_lists = pyre.inventory.list('data_lists', default=[])
        error_list = pyre.inventory.list('error_list', default=[])
        fit_func = pyre.inventory.str('fit_func', default=None)
        fit_param = pyre.inventory.list('fit_param', default=[])
        result_file = pyre.inventory.str('result_file', default='fit.new')

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['data_lists','error_list','fit_func', \
                       'fit_param','result_file']:
                if value.__class__() == '':
                    exec 'self.inventory.'+key+' = "'+value+'"'
                else:
                    exec 'self.inventory.'+key+' = '+str(value)
        return

    def fitMe(self):
        # Pass inventory into non-global variables.
        data_lists = self.inventory.data_lists
        xdata = data_lists[0]
        ydata = data_lists[1]
        zdata = []
        if len(data_lists) >= 3:
            zdata = data_lists[2]
        edata = self.inventory.error_list
        func = self.inventory.fit_func
        g_param = self.inventory.fit_param
        result_file = self.inventory.result_file

        # Feed to Gnuplot
        g = Gnuplot.Gnuplot(debug=1)

        # If the length of error list is not the same as the length of
        # the data, use a list of all 1's for error_list
        if len(xdata) != len(edata):
            edata = []
            for i in range(len(xdata)):
                edata.append(1)

        # Make data file
        datfile = 'data.in'    #FIXME
        f = open(datfile,'w')
        for p in range(len(xdata)):
            if zdata:
                print >>f, xdata[p], ydata[p], zdata[p], edata[p]
            else:
                print >>f, xdata[p], ydata[p], edata[p]
        f.close()

        # Make param file
        parfile = 'fit.par'    #FIXME
        f = open(parfile,'w')
        for p in g_param:
            print >>f, p
        f.close()

        #fit in gnuplot
        if zdata:
            g("fit " + func + " '" + datfile + "' using 1:2:3:4 via '" + \
              parfile + "'")
        else:
            g("fit " + func + " '" + datfile + "' using 1:2:3 via '" + \
              parfile + "'")

        g("update '" + parfile + "' '" + result_file + "'")

        raw_input('Please press return to continue...\n')
        #erase input files
        os.remove(datfile)     #FIXME
        os.remove(parfile)     #FIXME

        return 1

    ### BEGIN MAIN CODE BLOCK ###
    def main(self):
        # Pass inventory into non-global variables.
        data_lists = self.inventory.data_lists
        xdata = data_lists[0]
        ydata = data_lists[1]
        zdata = []
        if len(data_lists) >= 3:
            zdata = data_lists[2]
        edata = self.inventory.error_list
        func = self.inventory.fit_func
        g_param = self.inventory.fit_param
        result_file = self.inventory.result_file
        result_log = result_file + '.log'

        self.fitMe()

#        os.remove(result_file)  #FIXME
        os.rename('fit.log', result_log)   #FIXME

        return 1
    ### END MAIN CODE BLOCK ###

    def __init__(self, name='GnuplotFit', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        return

    def help(self):
        print __doc__
        return

if __name__ == '__main__':
    ''' Test the GnuplotFit class '''

    x = [0,1.1,2.04,3.1,3.99,5]
    y = [0,1,2,3,4,5]
    z = [0,1,2,3,4,5]
    e = [1,1,1,1,1,1]
    f = '(a*x)+(y*b)'
    params = ['a=0','b=0']
    data = [x, y, z]
    
    gf = GnuplotFit('test_gf', data_lists=data, error_list=e, fit_func=f, \
                    fit_param=params, result_file='fit1')
    print "~~~~~~~~~~~~~~"
    print "Function Fit 1"
    gf.run()

    gf2 = GnuplotFit('test_gf2', data_lists=data, fit_func=f, \
                    fit_param=params, result_file='fit2')
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Function Fit 2 (no error_list)"
    gf2.run()

    data3 = [x, y]
    gf3 = GnuplotFit('test_gf3', data_lists=data3, fit_func=f, \
                    fit_param=params, result_file='fit3')
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Function Fit 3 (no error_list)"
    gf3.run()



