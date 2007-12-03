print '''>>> from graphics.IDL import IDL
>>> ri = IDL()'''
from graphics.IDL import IDL
ri = IDL()

print '''>>> from Numeric import *
>>> x = pi*arange(21)/10
>>> y = ri.cos(x)
>>> ri.plot(x,y)'''
from Numeric import *
x = pi*arange(21)/10
y = ri.cos(x)
ri.plot(x,y)
raw_input("Press 'Return' to continue...")

print '''>>> ri.who()'''
print ri.who()
print '''>>> ri.x = x
>>> ri.y = ri.sin(ri.x)
>>> ri("plot, x, y")'''
ri.x = x
ri.y = ri.sin(ri.x)
ri("plot, x, y")
raw_input("Press 'Return' to continue...")

print '''>>> ri.who()'''
print ri.who()
print '''>>> ri.help('x')'''
ri.help('x')
print '''>>> ri._print(x)'''
ri._print(x)
