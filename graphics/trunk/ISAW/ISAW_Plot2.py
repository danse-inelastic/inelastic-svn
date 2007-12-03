'''displays two x-y pair columns simultaneously in ISAW
Inventory:
    input_file --  string (default=None)
    input_file2 --  string (default=None)
Methods:
  put(name,value) --> swallow named data array
  select(x1,y1,x2,y2) --> select data to plot
Notes:
  makes a system call to run "pyIsaw.py" with the selected args. 
  creates two temporary files ".ISAW_data" & ".ISAW_data2"
  then invokes "python pyISAW/pyISAW.py
                -Ftxt .ISAW_data -Ftxt .ISAW_data2 -c -v SELECTED_GRAPHS"
'''
__author__='Mike McKerns'

from pyre.applications.Script import Script
import os

class ISAW_Plot2(Script):
    '''pyre adaption of ISAW_Plot2.py code'''
    class Inventory(Script.Inventory):
        '''Inventory declares and stores user modifiable variables'''
        import pyre.inventory
        input_file = pyre.inventory.str('input_file', default=None)
        input_file2 = pyre.inventory.str('input_file2', default=None)

    def config(self, **kwds):
        '''configure the inventory'''
        for key,value in kwds.items():
            if key in ['input_file','input_file2']:
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

    def select(self,x,y,x2,y2):
        '''select(x1,y1,x2,y2) --> select data to plot'''
        xname = 'defaultXX1'
        yname = 'defaultYY1'
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
        x2name = 'defaultXX2'
        y2name = 'defaultYY2'
        if isinstance(x2, list): self.put(x2name,x2)
        elif isinstance(x2, str): x2name = x2
        else: self.put(x2,[]) #raise error
        if isinstance(y2, list): self.put(y2name,y2)
        elif isinstance(y2, str): y2name = y2
        else: self.put(y2,[]) #raise error
        self.file2 = '.ISAW_data2'
        f=open(self.file2,"w")
        for i in range(len(self.inputs[x2name])):
            f.write(str(self.inputs[x2name][i])+" "+ \
                    str(self.inputs[y2name][i])+"\n")
        f.close()
        return

    def _execute(self,input_file=None,input_file2=None):
        '''execute(input_file,input_file2) --> ship command to pyISAW.py'''
        if not input_file: input_file = self.file
        if not input_file2: input_file2 = self.file2
#       cmd = 'os.system("python pyISAW/pyISAW.py -Ftxt %s' % input_file
        cmd = 'os.system("python $EXPORT_ROOT/modules/graphics/ISAW/pyISAW/pyISAW.py -Ftxt %s' % input_file
        cmd += ' -Ftxt %s -c -v SELECTED_GRAPHS")' % input_file2
        exec(cmd)
        return

    def main(self, *args, **kwds):
        '''create the plot'''
        if self.file and self.file2:
            self._execute(self.file,self.file2)
        elif self.inventory.input_file and self.file2:
            self._execute(self.inventory.input_file,self.file2)
            self.file = None
        elif self.file and self.inventory.input_file2:
            self._execute(self.file,self.inventory.input_file2)
            self.file2 = None
        elif self.inventory.input_file and self.inventory.input_file2:
            self._execute(self.inventory.input_file,self.inventory.input_file2)
            self.file = None
            self.file2 = None
        else:
            print 'No file or list of data was given to plot.'
            raise 'InputError'
           #return
        return 

    def __init__(self, name='ISAW_Plot2', **kwds):
        Script.__init__(self, name)
        self.config(**kwds)
        self.inputs = {}
        self.file = None
        self.file2 = None
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
    plt = ISAW_Plot2('test_plt')
    journal.debug('test_plt').activate()
    vtkBackend.run()
