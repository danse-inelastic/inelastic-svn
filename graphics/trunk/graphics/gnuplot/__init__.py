__doc__ = '''Instructions for Pyre gnuplot component:
Import the PyGnuplot class        >>> from graphics.gnuplot import gnuplot
Instantiate the PyGnuplot class   >>> gr = gnuplot()
Get help                          >>> gr.help()
'''

def gnuplot():
    from PyGnuplot import PyGnuplot as PyGnuplotFactory
    return PyGnuplotFactory()

