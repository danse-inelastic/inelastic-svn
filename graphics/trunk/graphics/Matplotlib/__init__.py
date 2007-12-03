__doc__='''Instructions for Pyre matplotlib interface (and math functions):
Import the matplotlib class     >>> from graphics.Matplotlib import *
Instantiate the matplot class   >>> pl = pylab()
Get help                        >>> pl.doc()
'''
from matplotlib.numerix import *

def pylab():
    from matplot import matplot as matplotFactory
    return matplotFactory()

