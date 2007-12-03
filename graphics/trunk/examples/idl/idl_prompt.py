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
z = 0
print 'x: %s' % x
print 'y: %s' % y
raw_input('Please press return to continue...\n')

##### IDL #####
from graphics.IDL import IDL
ri = IDL()
ri.x = x
ri.y = y
ri.z = z
print '''EXAMPLE SCRIPT:
 IDL> plot, x,y
 IDL> z= x+y
 IDL> print, z
 IDL> oplot, x,z
 IDL> exit
'''
ri.prompt()
ri.who()
z = ri.z
print 'z: %s' % z
