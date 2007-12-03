#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu
from samlab import __doc__ as samdoc
__doc__ = samdoc

def matlab():
    '''get usage: ml = matlab(); print ml.__doc__'''
    from samlab import matlab as matlabFactory
    return matlabFactory()

def copyright():
    return "pymatlab pyre module: Copyright (c) 2005 Michael McKerns";


# built with: Matlab 6.5.0.180913a Release 13, sam 1.0

# version
__id__ = "$Id: __init__.py 227 2007-09-25 16:33:11Z brandon $"

# End of file
