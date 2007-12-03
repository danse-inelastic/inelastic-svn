#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyIDL.py
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
__doc__='''Instructions for Pyre IDL component:
Import the IDL class            >>> from PyIDL import rsiIDL
Instantiate the IDL class       >>> ri = rsiIDL()
Get help                        >>> ri.doc()
'''

from pyre.components.Component import Component
comp = Component('dummy','dummy')

class rsiIDL(Component):
    '''Pyre component for python bindings to IDL

Inventory:
  None
Methods:
  eval(command) --> execute an IDL command
  get(name,[array,allowNone]) --> rsiidl into python
  put(name,value,[array,type,allowNone]) --> python into rsiidl
  who([name,local,stdout]) --> print/return the IDL/local variables
  help([name]) --> print the IDL help message (for a variable)
  delete(name) --> destroy selected IDL variables
  map([name]) --> get the IDL data type mapping
  prompt() --> start an interactive session
  _print(value) --> print using the IDL print command
Notes:
  Reproduces IDL in Python via the Simple API for IDL (pyIDL).
  Both IDL and pyIDL must be installed,
  and IDL must be able to find a license.
'''
    def __init__(self, name='rsiIDL', **kwds):
        Component.__init__(self, name, facility='pyIDL')
        import pyIDL
        self.session = pyIDL.idl()
        return

    def __getattr__(self, name):
        try:
            exec 'attr = self.session.'+name
        except:
#           attr = None
#       if attr: return attr
#       try:
            exec 'attr = self.session.get("'+name+'")'
#       except:
#           exec 'attr = self.session.pros.'+name
        return attr

    def __setattr__(self,name,value):
        if name in ['evalbuff']:
            self.session.__dict__[name] = value
            return
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
    ri = rsiIDL()
    ri.put('x',[1,2,3,4,5])
    print ri.who(local=True)
