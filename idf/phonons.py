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


import os

def read(
    datapath, Omega2 = 'Omega2', Polarizations = 'Polarizations',
    Qgridinfo = 'Qgridinfo', DOS = 'DOS',
    reciprocal_unitcell = None):
    
    '''read phonons on a grid in idf format

    datapath: the root directory containing the data files
    Omega2, Polarizations, Qgridinfo, DOS: relative paths of individual idf data files
    '''

    Qgridinfo = os.path.join( datapath, Qgridinfo )
    Omega2 = os.path.join( datapath, Omega2 )
    Polarizations = os.path.join( datapath, Polarizations )
    DOS = os.path.join( datapath, DOS )

    # read DOS if it is available
    if os.path.exists(DOS):
        dos = _readDOS(DOS)
    else:
        dos = None

    from Qgridinfo import read
    reciprocalcell, ngridpnts = read( Qgridinfo )
    reciprocalcell = _checkReciprocalCell(reciprocalcell, reciprocal_unitcell, ngridpnts)

    from Omega2 import read as readOmega2
    omega2 = readOmega2( Omega2 )[1]
    # !!!
    # sometime omega2 has negative values. have to make sure all values are
    # positive
    omega2[ omega2<0 ] = 0
    
    import numpy as N
    energies = N.sqrt(omega2) * hertz2mev

    from Polarizations import read as readP
    polarizations = readP( Polarizations )[1]
    
    #N_q, N_b_times_D, N_b, D, temp = polarizations.shape
    #assert temp == 2
    N_q, N_b_times_D, N_b, D = polarizations.shape
    
    assert N_b_times_D == N_b*D
    assert D == len( ngridpnts )
    assert D == len( reciprocalcell )
    import operator
    assert N_q == reduce( operator.mul, ngridpnts )

    #polarizations.shape = ngridpnts + (N_b_times_D, N_b, D, 2)
    polarizations.shape = ngridpnts + (N_b_times_D, N_b, D)
    
    energies.shape = ngridpnts + (N_b_times_D, )

    nAtoms = N_b
    dimension = D
    #Qaxes = [
    #    (0, length(reciprocalcell[i]) / (ngridpnts[i] - 1), ngridpnts[i])
    #    for i in range( D )
    #    ]
    Qaxes = zip(reciprocalcell, ngridpnts)
    return nAtoms, dimension, Qaxes, polarizations, energies, dos


def _checkReciprocalCell(cell, unitcell, ngridpnts, epsilon = 0.1):
    '''check the cell against the unitcell (actually both are in the reciprocal space)

    The cell given by different computations (such as bvk, vasp, QE) are slightly
    different. We have to (by hacks) make them more-or-less consistent.

    cell: (v1, v2, v3) three vectors for the cell
    unitcell: (u1, u2, u3) three vectors for the unit cell

    cell should be very close to unitcell already
    '''
    # 
    n1, n2, n3 = ngridpnts
    
    from _crystal_utils import volume
    v = volume(cell)
    vuc = volume(unitcell)

    # if the volumes match, we assume we are good
    f1,f2,f3 = (
        (n1-1.)/n1, 
        (n2-1.)/n2, 
        (n3-1.)/n3,
        )
    diff = 1 - f1*f2*f3
    if abs((v/vuc)-1) < epsilon*diff:
        return _roundUpCell(cell, unitcell)

    raise NotImplementedError


def _roundUpCell(cell, unitcell):
    '''trying to round up the given cell according to the "unit" cell
    cell should be very close to unitcell already

    cell: (v1, v2, v3) three vectors for the cell
    unitcell: (u1, u2, u3) three vectors for the unit cell
    '''
    import numpy as np, numpy.linalg as nl
    inv = nl.inv(unitcell)
    r = []
    for v in cell:
        c = np.dot(v, inv)
        c = c.round()
        r.append(np.dot(c, unitcell))
        continue
    return r
    

def _readDOS(path):
    from DOS import read
    dummy, v, Z = read(path)
    # v is in terahertz, and it is not angular frequency
    from math import pi
    E = v * 2*pi * 1e12 * hertz2mev
    dos = E,Z
    return dos


def _hertz2meV():
    'calculate conversion constant'
    import _units as units
    SI = units.SI
    m = SI.meter; kg = SI.kilogram; s = SI.second
    hbar = 1.05457148e-34 * m**2 * kg /s
    hertz = 1 / s
    meV = units.energy.meV
    return hbar * hertz / meV
hertz2mev = _hertz2meV()



def test_checkReciprocalCell():
    import numpy.testing as nt, numpy as np
    
    unitcell = [
        [-1.555243888, 1.555243888, 1.555243888],
        [1.555243888, -1.555243888, 1.555243888],
        [1.555243888, 1.555243888, -1.555243888],
        ]
    cell = [
        [-1.55160454, -1.55160454, 1.55160454],
        [1.55160454, 1.55160454, 1.55160454],
        [-1.55160454, 1.55160454, -1.55160454],
        ]
    ngridpnts = 40,40,40
    cell1 = _checkReciprocalCell(cell, unitcell, ngridpnts)
    nt.assert_almost_equal(np.array(cell1), [
        [-1.555243888, -1.555243888, 1.555243888],
        [1.555243888, 1.555243888, 1.555243888],
        [-1.555243888, 1.555243888, -1.555243888],
        ])
    return
    

def test_roundUpCell():
    import numpy.testing as nt
    
    unitcell = [
        [1., 0, 0],
        [0, 1., 0],
        [0, 0, 1.],
        ]
    cell = [
        [1.001, 0, 0],
        [0, 0.999, 0.001],
        [0, 0, 0.9999],
        ]
    cell1 = _roundUpCell(cell, unitcell)
    nt.assert_equal(cell1, unitcell)

    unitcell = [
        [1., 1, 0],
        [1, 0., 1],
        [0, 0, 1.],
        ]
    cell = [
        [1.001, 0, 0],
        [0, 0.999, 0.001],
        [0, 0, 0.9999],
        ]
    cell1 = _roundUpCell(cell, unitcell)
    rcell = [
        [1.,0,0],
        [0,1,0],
        [0,0,1],
        ]
    nt.assert_equal(cell1, rcell)
    
    return


def main():
    test_roundUpCell()
    test_checkReciprocalCell()
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
