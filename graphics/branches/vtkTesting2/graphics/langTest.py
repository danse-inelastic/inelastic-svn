from graphics.vtk_ import *
from graphics.utils import *
from graphics.movie import movie
from graphics.common import *
from Numeric import array, sin, cos, sqrt, pi, ones, zeros, Float, exp
from scipy import linspace
import time

plt = VtkBackend() # Create backend instance
use(plt, globals()) # Export public namespace of plt to globals()

def test_plot():
    line,=plot([1,2,3])
    ax=gca()
    ax.set(xlim=[0,5])
    raw_input('press enter')
    print line._prop
    print ax._prop
    print gcf()._prop
    
#    x = seq(-2,2,.1)
#    colors = 'r b g c m y k w'.split()
#    for i,c in zip(range(1,5),colors):
#        subplot(2,2,i)
#        plot(x,x**i,'%s' % c,title='subplot(2,2,%d)' % i)
#        raw_input('press enter')
#    raw_input('press enter')
#    subplot(2,2,1)
#    plot(x,x**5,'k',title='subplot(2,2,1)')
#    raw_input('press enter')
#    clf()
#    hold('on')
#    i = 1
#    axis([-2,2,0,10])
#    for color in plt._colors:
#        plot(x,x*0+i,color,box='on',title='colors')
#        i += 1
#    raw_input('press enter')
#    clf()
#    t = seq(0,2*pi,2*pi/100)
#    plot(cos(t),sin(t),title='circle',axis='equal')
#    raw_input('press enter')
#    t = seq(0,2*pi,pi/20)
#    plot(sin(t),2*cos(t),grid='on',axis='equal')
#    raw_input('press enter')
    
if __name__=='__main__': 
    test_plot()