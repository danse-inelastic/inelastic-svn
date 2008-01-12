#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy as N
import crystal 

def read( filename ):
    lines = open(filename).readlines()
    # line 1: number of atoms
    n = int(lines[0])
    # line 2: cell vectors
    cellvectors = N.array([ float(i) for i in lines[1].split() ] )
    cellvectors.shape = 3,3
    # after that, we have atoms
    atomrecords = [ line2atomrecord( line ) for line in lines[2:] ]
    atoms = [r[0] for r in atomrecords]
    positions = [ r[1] for r in atomrecords ]
    uc = crystal.unitcell( cellvectors, atoms, positions )
    return uc


def line2atomrecord( line ):
    symbol, x,y,z = line.split()
    atom = crystal.atom( symbol)
    position = [ float(i) for i in x,y,z ]
    return atom, position

# version
__id__ = "$Id$"

# End of file 
