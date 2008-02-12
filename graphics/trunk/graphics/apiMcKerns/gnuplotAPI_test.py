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

from GnuplotEngine import GnuplotEngine
x = [1,2,3,4,5]
y = [1,4,9,16,25]

# instantiate
gpi = GnuplotEngine()
print 'type =',gpi.sessiontype

# open blank canvas
gpi.blank()

# set title
gpi.title('test')

# change range
gpi.xrange(-1,1)
gpi.yrange(max=2)
gpi.plot('sin(x)')
raw_input("Press 'Return'")

# reset range
gpi.xrange()
gpi.yrange()
gpi.plot('sin(x)')
raw_input("Press 'Return'")

# set logscale
gpi.xrange(1,10)
gpi.xlogscale()
gpi.ylogscale()
gpi.plot('log(x)')
raw_input("Press 'Return'")
gpi.xlogscale(False)
gpi.ylogscale(False)

# set labels
gpi.xlabel('foo')
gpi.ylabel('bar')
gpi.plot('log(x)')
raw_input("Press 'Return'")

# set tics
gpi.xtics(2)
gpi.ytics(.5)
gpi.plot('log(x)')
raw_input("Press 'Return'")

# unset title & labels & tics
gpi.title()
gpi.xlabel()
gpi.ylabel()
gpi.xtics(None)
gpi.plot('log(x)')
raw_input("Press 'Return'")

# autoscale tics
gpi.xtics()
gpi.ytics()
gpi.plot('log(x)')
raw_input("Press 'Return'")

# autoscale range
gpi.xrange("*","*")
gpi.plot(gpi.Data(x,y))
raw_input("Press 'Return'")

# set plot item style & label
gpi.setLabel(0,'x**2')
#with = 'linespoints linetype 5 pointtype 4'
gpi.setStyle(0,style='solid',color='cyan',shape='square')
raw_input("Press 'Return'")

# get plot item (and style & label)
gpi.replot(gpi.Func('sin(x)', with='linespoints', title='sine'))
print 'plot item #0 =',gpi._getItem(0)
print 'with style:',gpi.getStyle(0)
print 'and label:',gpi.getLabel(0)
print ''
print 'plot item #1 =',gpi._getItem(1)
print 'with style:',gpi.getStyle(1)
print 'and label:',gpi.getLabel(1)
raw_input("Press 'Return'")

# remove plot item
gpi.remove(0)
raw_input("Press 'Return'")

# destroy
gpi.destroy()
