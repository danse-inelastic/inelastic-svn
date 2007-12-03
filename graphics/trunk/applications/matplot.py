#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# matplot.py
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
__doc__='''Instructions for Pyre matplotlib interface:
Import the matplotlib class     >>> from graphics.applications import pylab
Instantiate the matplot class   >>> pl = pylab()
Start the interface             >>> pl.run()
'''
from pyre.applications.Script import Script

class matplot(Script):
    '''Pyre matplotlib scripting interface

Inventory:
  None
Methods:
  run() --> start an interactive session
Notes:
  All 'pylab' attributes are available as matplot class attributes.
  All 'numerix' functions may be made global.  Matplotlib must be installed.
'''

    def main(self):
        '''run() --> interactive session'''
        self.session.prompt()
        return

    def __init__(self, name='matplot', **kwds):
        Script.__init__(self, name)
        from graphics.Matplotlib.mplcomm import matplot
        self.session = matplot()
        return

if __name__ == '__main__':
    mp = matplot()
    mp.run()
