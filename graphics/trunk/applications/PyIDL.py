#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyIDL.py
#
# 3/19/2005 version 0.0.2a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__='Mike McKerns'
__doc__='''Instructions for Pyre IDL scripting interface:
Import the IDL class            >>> from graphics.applications import IDL
Instantiate the IDL class       >>> ri = IDL()
Start the interface             >>> ri.run()
'''

from pyre.applications.Script import Script

class rsiIDL(Script):
    '''Pyre IDL scripting interface (adapted from mmckerns' pyIDL)

Inventory:
  None
Methods:
  run() --> launch IDL interface
Notes:
  Reproduces the IDL command line in Python via a simple
  function that uses the Simple API for IDL (pyIDL).
  Both IDL and pyIDL must be installed,
  and IDL must be able to find a license.
'''

    def main(self):
        '''run() --> launch IDL interface'''
        self.session.prompt()
        return

    def __init__(self, name='rsiIDL', **kwds):
        Script.__init__(self, name)
        from graphics.IDL import IDL
        self.session = IDL()
        return

if __name__ == '__main__':
    ri = rsiIDL()
    ri.run()
