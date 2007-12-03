from pylab import *

p,=plot([1,2,3])
ax=gca()
setp(gca(),'title','ha ha')

print getp(ax,'title')

setp(ax,'xlabel','my x')

print getp(ax,'xlabel')

setp(ax,'ylabel','my y')

print getp(ax,'ylabel')

show()