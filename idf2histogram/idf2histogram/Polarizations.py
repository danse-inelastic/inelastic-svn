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
         pols_idf_file='Polarizations', qgridinfo_file='Qgridinfo', weightedq_file='WeightedQ',
         nD=3):
    ''' read omega2 data file in idf format
    nD is the dimension of the qgrid.
    it is assumed that the qgrid is regular, and is defined in qgridinfo_file
    The qgridinfo_file is a python file that defines vars bi, {i=1..nD} and ni, {i=1..nD}
    The grid is a regularly spaced grid. See Qgridinfo.py for more details.
    '''
    
    import os
    
    from idf.Polarizations import read
    info, pols = read(os.path.join(directory,pols_idf_file))

    qgridinfo = _retrieveQgridinfo(directory, qgridinfo_file, weightedq_file, nD=nD)

    #
    nQ, nbXnD, nb, D = pols.shape
    assert D == nD
    assert nbXnD == nb*nD
    
    #
    import operator
    nis = [qgridinfo['n'+str(i)] for i in range(1, nD+1)]
    assert nQ == reduce(operator.__mul__, nis),\
           "Q points mismatch: nQ=%s, {ni}=%s" % (nQ, nis)

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

    # branch
    branchaxis = H.axis('branchID', range(nbXnD))
    
    # basis
    basisaxis = H.axis('basisID', range(nb))
    
    # dimension
    Daxis = H.axis('dimensionID', range(nD))

    # real or imaginary
    riaxis = H.axis('realimagID', range(2))

    #
    axes = Qaxes+[branchaxis, basisaxis, Daxis, riaxis]

    #
    shape = [axis.size() for axis in axes]

    #
    import numpy
    pols1 = numpy.zeros(shape, dtype='float')
    pols.shape = shape[:-1]
    print pols.shape
    print pols1.shape
    pols1[:,:,:,:,:,:, 0] = numpy.real(pols)
    pols1[:,:,:,:,:,:, 1] = numpy.imag(pols)
    
    #
    h = H.histogram('Pols', axes, data = pols1)

    return h


from Qgridinfo import read as _retrieveQgridinfo


# version
__id__ = "$Id$"

# End of file 
