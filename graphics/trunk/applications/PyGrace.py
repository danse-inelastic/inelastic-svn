#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
__doc__ = '''Instructions for Pyre grace scripting interface:
Import the PyGrace class        >>> from graphics.applications import grace
Instantiate the PyGrace class   >>> gr = grace()
Start the interface             >>> gr.run()
'''
from pyre.applications.Script import Script

class PyGrace(Script):
    '''Pyre grace scripting interface

Inventory:
  none
Methods:
  run() --> launch grace interface
Notes:
  Reproduces the grace command line in Python
  grace must be installed
'''
    def main(self):
        '''run() --> launch grace interface'''
        self.session.prompt()
        return

    def __init__(self, name='grace', **kwds):
        Script.__init__(self, name)
        from graphics.grace import grace
        self.session = grace()
        return

if __name__ == '__main__':
    mp = PyGrace()
    mp.run()
