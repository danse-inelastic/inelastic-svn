#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Matlab.py
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
__doc__ = '''Instructions for Pyre Matlab scripting interface:
Import the Matlab class         >>> from graphics.applications import Matlab
Instantiate the Matlab class    >>> ml = Matlab()
Start the interface             >>> ml.run()
'''
from pyre.applications.Script import Script

class Matlab(Script):
    '''Pyre Matlab scripting interface (adapted from Matlab_mcomm.py)

Inventory:
  none
Methods:
  run() --> launch Matlab interface
Notes:
  Reproduces the Matlab command line in Python via a simple
  function that uses the Simple API for Matlab (sam).
  Both Matlab, sam, and array_kluge must be installed,
  and Matlab must be able to find a license.
'''

    def main(self):
        '''run() --> launch Matlab interface'''
        self.session.prompt()
        return

    def __init__(self, name='Matlab', **kwds):
        Script.__init__(self, name)
        from graphics.Matlab import Matlab
        self.session = Matlab()
        return

if __name__ == '__main__':
    mp = Matlab()
    mp.run()
