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
