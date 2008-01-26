#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 2/11/2005 version 0.0.1a
# mmckerns@caltech.edu
# (C) 2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
__author__ = 'Mike McKerns'


x = [1,2,3,4,5]
y = [1,4,9,16,25]
print 'x: %s' % x
print 'y: %s' % y
raw_input('Please press return to continue...\n')

#### Matplotlib #####
from graphics.Matplotlib import pylab
pl = pylab()
pl.ion()
print '''EXAMPLE SCRIPT:
 >> from Numeric import *
 >> t = arange(0.0, 1.0, 0.01)
 >> s = sin(2*pi*t)
 >> c = cos(2*pi*t)
 >> subplot(121)
 >> plot(t,s)
 >> subplot(122)
 >> plot(t,c)
 >> exit
'''
pl.prompt()
