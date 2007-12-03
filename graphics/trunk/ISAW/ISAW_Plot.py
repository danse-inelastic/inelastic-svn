'''displays an x-y pair column in ISAW
Inventory:
    input_file --   string (default=None)
Methods:
  put(name,value) --> swallow named data array
  select(x,y) --> select data to plot
Notes:
  makes a system call to run "pyIsaw.py" with the selected args. 
  creates temporary file ".ISAW_data"
  then invokes "python pyISAW/pyISAW.py -Ftxt .ISAW_data"
'''
__author__='Mike McKerns'

from pyre.applications.Script import Script
import os

class ISAW_Plot(Script):
    '''pyre adaption of ISAW_Plot.py code'''
    
    class Inventory(Script.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_file = pyre.inventory.str('input_file', default=None)

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_file']:
                exec 'self.inventory.'+key+' = "'+value+'"'
        return

    def put(self,name,values):
        '''put(name,value) --> swallow named data array'''
        if not isinstance(name, str):
            print "Warning: Unknown variable name %s" % str(name)
            raise 'NameError'
           #return
        if isinstance(values, list): self.inputs[name] = values
        return

    def select(self,x,y):
        '''select(x,y) --> select data to plot'''
        xname = 'defaultXXX'
        yname = 'defaultYYY'
        if isinstance(x, list): self.put(xname,x)
        elif isinstance(x, str): xname = x
        else: self.put(x,[]) #raise error
        if isinstance(y, list): self.put(yname,y)
        elif isinstance(y, str): yname = y
        else: self.put(y,[]) #raise error
        self.file = '.ISAW_data'
        f=open(self.file,"w")
        for i in range(len(self.inputs[xname])):
            f.write(str(self.inputs[xname][i])+" "+ \
                    str(self.inputs[yname][i])+"\n")
        f.close()
        return

    def _execute(self,input_file=None):
        '''execute(input_file) --> ship command to pyISAW.py'''
        if not input_file: input_file = self.file
#       cmd = 'os.system("python pyISAW/pyISAW.py -Ftxt %s")' % input_file
        cmd = 'os.system("python $EXPORT_ROOT/modules/graphics/ISAW/pyISAW/pyISAW.pyc -Ftxt %s")' % input_file
        exec(cmd)
        return

    def main(self, *args, **kwds):
        '''create the plot'''
        if self.file:
            self._execute(self.file)
        elif self.inventory.input_file:
            self._execute(self.inventory.input_file)
            self.file = None
        else:
            print 'No file or list of data was given to plot.'
            raise 'InputError'
           #return
        return 

    def __init__(self, name='ISAW_Plot', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        self.inputs = {}
        self.file = None
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
    plt = ISAW_Plot('test_plt')
    journal.debug('test_plt').activate()
    vtkBackend.run()
