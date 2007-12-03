#!/usr/bin/env python
##
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 4/17/2006 version 0.1a
# mmckerns@caltech.edu
# (C) 2006 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'
__doc__ = '''...
'''

from pyre.components.Component import Component

class Plotter2D(Component):
    ''' ... '''

    def __init__(self,name):
        ''' ... '''
        if name is None: name='Plotter2D'
        Component.__init__(self,name,facility='graphics')

    def blank(self):
        ''' ... '''
        raise NotImplementedError("class %s must override function 'blank'"
                                  % self.__class__.__name__)


