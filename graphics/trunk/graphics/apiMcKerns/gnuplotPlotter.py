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

from plotter import Plotter2D

class GnuplotPlotter2D(Plotter2D):
    ''' ... '''

    def __init__(self):
        ''' ... '''
        from graphics.gnuplot import gnuplot
        self.session = gnuplot()
        return

    def blank(self):
        ''' ... '''
        self.session.clear()
        return

if __name__ is '__main__':
    gpp = GnuplotPlotter2D('test')
    gpp.blank()
    raw_input("Press 'Return' to end")


