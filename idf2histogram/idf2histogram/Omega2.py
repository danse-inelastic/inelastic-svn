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

# read omega2 data file in idf format
# nD is the dimension of the qgrid.
# it is assumed that the qgrid is regular, and is defined in qgridinfo_file
# The qgridinfo_file is a python file that defines vars bi, {i=1..nD} and ni, {i=1..nD}
def read(directory,
         omega2_idf_file='Omega2', qgridinfo_file='Qgridinfo', weightedq_file='WeightedQ',
         nD=3):
    
    import os
    
    from idf.Omega2 import read
    info, omega2 = read(os.path.join(directory,omega2_idf_file))

    qgridinfo = _retrieveQgridinfo(directory, qgridinfo_file, weightedq_file, nD=nD)

    #
    nQ, nbXnD = omega2.shape
    #
    import operator
    assert nQ == reduce(operator.__mul__, [qgridinfo['n'+str(i)] for i in range(1, nD+1)])

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


def _retrieveQgridinfo(directory, qgridinfo_file, weightedq_file, nD=3):
    import os
    f = os.path.join(directory, qgridinfo_file)
    qgridinfo = {}
    if not os.path.exists(f): raise RuntimeError, 'missing file: %s' % f
    content = open(f).read()
    exec content in qgridinfo
    # we should have {bi} and {ni} in d now
    qgridshape = [qgridinfo['n'+str(i)] for i in range(1, nD+1)]

    # try to match qgridinfo from weightedq
    f = os.path.join(directory, weightedq_file)
    if not os.path.exists(f): raise RuntimeError, 'missing file: %s' % f
    from idf.WeightedQ import read
    info, Qs, Ws = read(f)
    N_q, D = Qs.shape
    assert D == nD
    import operator
    assert N_q == reduce(operator.__mul__, [qgridinfo['n'+str(i)] for i in range(1, nD+1)])
    assert len(Ws) == N_q

    #
    Qs.shape = tuple(qgridshape) + (D,)
    for q in Qs[ (0,)*D ] : assert q==0.
    for i in range(D):
        indexes = [0] * D
        indexes[i] = qgridshape[i]-1
        indexes = tuple(indexes)
        bb = Qs[indexes]
        b = qgridinfo['b'+str(i+1)]
        assertVectorAlmostEqual(b, bb)
        continue
    
    return qgridinfo
        

def assertVectorAlmostEqual(a, b, eps=1.e-5):
    for ea, eb in zip(a,b):
        assertAlmostEqual(ea,eb, eps=eps)
        continue
    return


def assertAlmostEqual(a,b, eps = 1.e-5):
    if abs(a) < eps and abs(b) < eps: return
    assert abs( (a-b)/b ) < eps, '%s != %s' % (a,b)
    

# version
__id__ = "$Id$"

# End of file 
