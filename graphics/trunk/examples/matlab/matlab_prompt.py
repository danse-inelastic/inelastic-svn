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

##### Matlab #####
from graphics.Matlab import Matlab
ml = Matlab()
ml.put('x',x)
ml.put('y',y)
ml.put('z',x+y)
print '''EXAMPLE SCRIPT:
 >> plot(x,y)
 >> z(3) = 100
 >> exit
'''
ml.prompt()
ml.who()
z = ml.get('z')
print 'z: %s' % z
