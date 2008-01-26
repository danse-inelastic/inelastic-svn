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

##### ISAW #####
from graphics.ISAW.ISAW_Plot import ISAW_Plot
ip = ISAW_Plot()
#ip.help()
ip.put('x',x)
ip.put('y',y)
ip.select('x','y')
print '''\nselect(x,y)\n'''
ip.run()
ip.put('z',x+y)
ip.select('y','z')
print '''\nselect(y,x+y)\n'''
ip.run()
