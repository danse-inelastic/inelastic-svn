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


# the data object
from matter.Atom import Atom



# dsaw.model helpers
def __establishInventory__(self, inventory):
    inventory.element = self.symbol
    inventory.xyz = self.xyz
    inventory.label = self.label
    inventory.occupancy = self.occupancy
    return
Atom.__establishInventory__ = __establishInventory__

def __restoreFromInventory__(self, inventory):
    # create a new atom with new propties
    atom = self.__class__(
        atype=inventory.element,
        xyz=inventory.xyz,
        label=inventory.label,
        occupancy=inventory.occupancy)
    # and use the copy constructer to reinitilize myself
    self.__init__(atom)
    return
Atom.__restoreFromInventory__ = __restoreFromInventory__

#   inventory
class Inventory(InvBase):

    
    # atype
    element = InvBase.d.str(name='element', max_length=2, default='H') # validator choice?

    xyz = InvBase.d.array(name = 'xyz', elementtype='float', shape=3, default=[0.0, 0.0, 0.0])
    
    label = InvBase.d.str(name='label', max_length=16)
    
    occupancy = InvBase.d.float(name = 'occupancy', default=1.0)
#    _anisotropy = False
#    _U = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]#numpy.zeros((3,3), dtype=float)
#    _Uisoequiv = 0.0
#    _Usynced = True

    dbtablename = 'atoms'

Atom.Inventory = Inventory
del Inventory


# version
__id__ = "$Id$"

# End of file 
