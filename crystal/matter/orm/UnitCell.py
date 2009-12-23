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
from matter.UnitCell import UnitCell


# dsaw.model inventory
from Atom import Atom
class Inventory(InvBase):

    base = InvBase.d.array(name='base', shape=(3,3), elementtype='float')
    atoms = InvBase.d.referenceSet(name='atoms', targettype=Atom, owned=1)
    
    dbtablename = 'unitcells'
    
UnitCell.Inventory = Inventory
del Inventory


# version
__id__ = "$Id$"

# End of file 
