print "build python list"
print '''>>> from Numeric import *
>>> from Numeric import NewAxis
>>> x = pi*arange(21)/10.
>>> y = cos(x)'''
from Numeric import *
from Numeric import NewAxis
x = pi*arange(21)/10.
y = cos(x)

print "build a Numeric matrix"
print '''>>> xm = x[:,NewAxis]
>>> ym = y[NewAxis,:]
>>> m = (sin(xm) + 0.1*xm) - ym**2'''
xm = x[:,NewAxis]
ym = y[NewAxis,:]
m = (sin(xm) + 0.1*xm) - ym**2

print "instantiate the Matplotlib class"
print '''>>> from graphics.Matplotlib import pylab
>>> pl = pylab()'''
from graphics.Matplotlib import pylab
pl = pylab()

#print "get help"
#print '''>>> pl.doc()'''
#pl.doc()

print "create a colormap directly from python"
print '''>>> pl.pcolor(m)
>>> pl.show()'''
pl.pcolor(m)
pl.show()

#print "create a surface plot from within Matplotlib"
#MATPLOTLIB (0.83) CANNOT CREATE SURFACE PLOT

print "delete a variable within Matplotlib"
print '''>>> pl.m = m
>>> pl.delete('m')'''
pl.m = m
pl.delete('m')

print "create a lineplot directly from python"
print '''>>> pl.plot(x,sin(x))'''
pl.plot(x,sin(x))
pl.show()
raw_input("Press 'Return' to continue...")

print "create a formatted lineplot from within Matplotlib"
print '''>>> pl.x = x
>>> pl.y = cos(x)
>>> pl("plot(x,y,'go-')")'''
pl.x = x
pl.y = cos(x)
pl("plot(x,y,'go-')")
pl.show()
raw_input("Press 'Return' to continue...")

print "create a histogram using the Matplotlib session interface"
print '''#   TYPE THE FOLLOWING IN THE PROMPT:
#   >> clf()
#   >> title('foobar')
#   >> hist(y)
#   >> exit'''
print '''>>> pl.prompt()'''
pl.prompt()

print "inspect variables within Matplotlib"
print '''>>> pl.who().keys()'''
print pl.who().keys()
print '''>>> pl.who('x')'''
print pl.who('x')

print "get variables from Matplotlib into python"
print '''>>> pl.y'''
print pl.y
print '''>>> pl.y[0]'''
print pl.y[0]
