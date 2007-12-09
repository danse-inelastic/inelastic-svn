# Copyright 2007 Brandon Keith  See LICENSE file for details. 
"""
EpydocTest.py Tests to see if a module is being imported by epydoc in
order to document it, rather than for actual use.

To use:

import EpydocTest

if (EpydocTest.documenting()):
    ... documentation behavior
else:
    ... actual run behavior

$Id: EpydocTest.py,v 1.2 2007/05/16 23:37:50 emessick Exp $
"""

__author__ = "EricM"

import sys

def documenting():
    if ('epydoc' in sys.modules):
        return True
    return False
