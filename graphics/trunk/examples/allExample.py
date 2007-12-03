#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 2/11/2005 version 0.0.1d
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

##### Gnuplot #####
from graphics.gnuplot.Gnuplot_Script import GnuplotScript
gs = GnuplotScript()
gs.config(set_commands='set data style lines')
gs.config(input_list=[x,y])
print '''EXAMPLE SCRIPT:
 gnuplot>>> plot sin(x)
 Ctrl-d
'''
gs.run()
from graphics.gnuplot.Gnuplot_Script import GnuplotScript
gp = GnuplotScript()
gp.config(set_commands='set pm3d')
gp.config(plot_style='Grid')
gp.config(input_list=[x,y,'sin(x)'])
gp.run()
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
raw_input('Please press return to continue...\n')

##### pgplot #####
from graphics.pgplot.pgplot2D import pgplot2D
pg = pgplot2D()
#pg.config(output_type='/XWINDOW')
pg.config(input_list=[x,y],plot_type='line')
print '''\nline plot\n'''
pg.run()
pg.config(input_list=[[-5,5],[-5,5],'cos(y)+sin(x)'],plot_type='contour')
print '''\ncontour plot\n'''
pg.run()
raw_input('Please press return to continue...\n')

##### HippoDraw #####
from graphics.HippoDraw.HippoDraw_Plot2D import HippoPlot2D
hp = HippoPlot2D()
hp.config(input_list=[x,y])
print '''EXAMPLE SESSION:
 * Left-click on 'X-Y Plot'
 * Select 'Functions' tab
 * Add function 'PowerLaw'
 * Select 'Axis' tab
 * Adjust Axis settings
'''
hp.run()
raw_input('Please press return to continue...\n')
