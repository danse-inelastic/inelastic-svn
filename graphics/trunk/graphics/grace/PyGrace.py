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
__author__ = 'Mike McKerns'
__doc__ = '''Instructions for Pyre grace component:
Import the PyGrace class        >>> from PyGrace import PyGrace
Instantiate the PyGrace class   >>> pg = PyGrace()
Get help                        >>> pg.doc()
'''
from pyre.components.Component import Component
comp = Component('dummy','dummy')

class PyGrace(Component):
    '''pyre pygrace component

Inventory:
  none
Methods:
  prompt() --> start interactive session
  eval(command) --> execute a grace command
  put(name,val) --> put variable into interactive session
  get(name) --> get variable from interactive session
  who([name]) --> return the existing grace variables
  delete(name) --> destroy selected pylab variables
  restart() --> restart a grace window
Notes:
  grace must be installed, grace relies on (open)motif and Numeric
'''
    def restart(self):
        '''restart() --> restart a grace window'''
        vars = self.session.who()
        self.session.restart()
        self.session.whos = vars
        return

    def __init__(self, name='PyGrace', **kwds):
        Component.__init__(self, name, facility='pygrace')
        from pygrace import grace
        self.session = grace()
        return

    def __getattr__(self, name):
        try:
            exec 'attr = self.session.'+name
        except:
            exec 'attr = self.session.get("'+name+'")'
        return attr

    def __setattr__(self,name,value):
        attrlist = comp.__dict__.keys()
        attrlist.append('session')
        if name in attrlist:
            self.__dict__[name] = value
            return
        self.session.put(name,value)
        return

    def __call__(self,*args):
        for arg in args:
            self.session.eval(arg)
        return

    def doc(self):
        print self.__doc__
        return

# main
if __name__ == '__main__':
    x = [1,4,9,16,25,36,49,64,81]
    mp = PyGrace('test')
    mp.put('x',x)
    print mp.who()
    mp.exit()

# version
__id__ = "$Id: PyGrace.py 227 2007-09-25 16:33:11Z brandon $"

# End of file 

