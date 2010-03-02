#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def _hertz2meV():
    'calculate conversion constant'
    import _units as units
    SI = units.SI
    m = SI.meter; kg = SI.kilogram; s = SI.second
    hbar = 1.05457148e-34 * m**2 * kg /s
    hertz = 1 / s
    meV = units.energy.meV
    return hbar * hertz / meV

# constant to convert angular frequency to meV
hertz2meV = _hertz2meV()

    
from math import pi


# version
__id__ = "$Id$"

# End of file 
