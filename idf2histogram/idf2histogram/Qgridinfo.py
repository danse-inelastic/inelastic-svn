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


# To create histogram, qgrid must be regular.
# The Qgridinfo defines a regular Q grid
# The Q grid covers a box defined by b1, b2, b3
# At bi direction, the grid is [0*bi, 1./(ni-1)*bi, ..., 1*bi]
# 


def read(directory, qgridinfo_file, weightedq_file, nD=3):
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
    if not os.path.exists(f):
        # WeightedQ does not exist
        return qgridinfo
    
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
