# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def read(directory,
         omega2_idf_file='Omega2', qgridinfo_file='Qgridinfo', weightedq_file='WeightedQ',
         nD=3):
    ''' read omega2 data file in idf format
    nD is the dimension of the qgrid.
    it is assumed that the qgrid is regular, and is defined in qgridinfo_file
    The qgridinfo_file is a python file that defines vars bi, {i=1..nD} and ni, {i=1..nD}
    '''
    
    import os
    
    from idf.Omega2 import read
    info, omega2 = read(os.path.join(directory,omega2_idf_file))

    qgridinfo = _retrieveQgridinfo(directory, qgridinfo_file, weightedq_file, nD=nD)

    #
    nQ, nbXnD = omega2.shape
    #
    import operator
    nis = [qgridinfo['n'+str(i)] for i in range(1, nD+1)]
    assert nQ == reduce(operator.__mul__, nis),\
           "Q points mismatch: nQ=%s, {ni}=%s" % (nQ, nis)

    # number of basis
    nb = nbXnD / nD

    #
    import histogram as H
    # Q axes
    Qaxes = []
    for i in range(nD):
        ni = qgridinfo['n'+str(i+1)]
        bi = qgridinfo['b'+str(i+1)]
        Qiaxis = H.axis('Q'+str(i+1), H.arange(0, 1+1e-10, 1./(ni-1)), '1./angstrom',
                        attributes = {'b': bi} )
        Qaxes.append(Qiaxis)
        continue
    # basis
    basisaxis = H.axis('basisID', range(nb))
    # dimension
    Daxis = H.axis('dimensionID', range(nD))
    #
    axes = Qaxes+[basisaxis, Daxis]
    #
    omega2.shape = [axis.size() for axis in axes]
    h = H.histogram('Omega2', axes, data = omega2)

    return h


from Qgridinfo import read as _retrieveQgridinfo


# version
__id__ = "$Id$"

# End of file 
