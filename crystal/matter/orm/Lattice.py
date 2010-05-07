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


from dsaw.model.Inventory import Inventory as InvBase


# data object
from matter.Lattice import Lattice


# dsaw.model inventory
class Inventory(InvBase):

    a = InvBase.d.float(name = 'a', default=1.0, validator=InvBase.v.positive)
    b = InvBase.d.float(name = 'b', default=1.0, validator=InvBase.v.positive)
    c = InvBase.d.float(name = 'c', default=1.0, validator=InvBase.v.positive)
    alpha = InvBase.d.float(name = 'alpha', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))
    beta = InvBase.d.float(name = 'beta', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))
    gamma = InvBase.d.float(name = 'gamma', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))

    base = InvBase.d.array(name='base', shape=(3,3), elementtype='float')
    
    dbtablename = 'lattices'
    
Lattice.Inventory = Inventory
del Inventory

#import numpy.linalg as la
import numpy as np

def aprEq(a,b):
    if abs(a-b)<10**-7: return True
    else: return False

def isUnitBase(testbase):
    ub=np.array([[1.0,0,0],[0,1,0],[0,0,1]])
    diff = ub-np.array(testbase)
    if aprEq(diff.all(),0.0): return True
    else: return False

def __restoreFromInventory__(self, inventory):
    #restore from base preferably because has setting information...
    #assume the unit base is like no base
    
    if not inventory.base or isUnitBase(inventory.base):
        self.__init__(a=inventory.a,
                      b=inventory.b,
                      c=inventory.c,
                      alpha=inventory.alpha,
                      beta=inventory.beta,
                      gamma=inventory.gamma,
                      )
    else:
        self.__init__(base=inventory.base)
    return
Lattice.__restoreFromInventory__ = __restoreFromInventory__

# version
__id__ = "$Id$"

# End of file 
