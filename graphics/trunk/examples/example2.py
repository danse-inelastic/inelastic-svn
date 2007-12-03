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

##### grace #####
from graphics.grace import grace
pg = grace()
#pg.doc()
pg.plot(x,y)
print '''EXAMPLE SCRIPT:
 grace> z = [2,8,18,32,50]
 grace> histoPlot(z)
 grace> s0 fill color 3
 grace> redraw()
 grace> exit
'''
pg.prompt()
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
#raw_input('Please press return to continue...\n')
