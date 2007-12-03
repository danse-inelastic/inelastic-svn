#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# matplot.py
#
# 3/15/2005 version 0.0.2b
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__='''Instructions for Pyre matplotlib component:
Import the matplotlib class     >>> from matplot import matplot
Instantiate the matplot class   >>> mp = matplot()
Get help                        >>> mp.doc()
'''
from pyre.components.Component import Component
comp = Component('dummy','dummy')

class matplot(Component):
    '''Pyre matplotlib component

Inventory:
  None
Methods:
  prompt() --> start an interactive session
  eval(command) --> execute a pylab command
  put(name,val) --> put variable into pylab session
  get(name) --> get variable from pylab session
  who([name]) --> return the existing pylab variables
  delete(name) --> destroy selected pylab variables
Notes:
  All native 'pylab' methods are also available as class methods.
  All 'numerix' functions may be made global.  Matplotlib must be installed.
'''
#NOTES:
#Section 2.14 in matplotlib user's guide is "Event Handling" via the mouse.
#Is there some way to put/get variables into the interactive session?

    def __init__(self, name='matplot', **kwds):
        Component.__init__(self, name, facility='matplotlib')
        import mplcomm
        self.session = mplcomm.matplot()
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

if __name__ == '__main__':
    mp = matplot()
    mp.ion()
    mp.prompt()
