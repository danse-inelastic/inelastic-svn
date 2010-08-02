"""
Facade around Numpy/Numeric
"""
use_numpy = True
if use_numpy:
    from numpy import array,dot,reshape,identity,zeros
    from numpy import dot as matrixmultiply
    import numpy as NumWrap
else:
    from Numeric import array,dot,matrixmultiply,reshape,identity,zeros
    import Numeric as NumWrap
