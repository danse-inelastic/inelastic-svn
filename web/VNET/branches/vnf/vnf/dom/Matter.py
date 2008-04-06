# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DbObject import DbObject
class Matter(DbObject):

    name = 'matter'

    import pyre.db

    cartesianLattice = pyre.db.doubleArray( name = 'cartesianLattice')
    cartesianLattice.meta['tip'] = 'array of cartesian lattice vectors'
    
    fractionalCoordinates = pyre.db.doubleArray( name = 'fractional_coordinates')
    fractionalCoordinates.meta['tip'] = 'array positions as fractional values of unit cell'
    
    atomSymbols = pyre.db.varcharArray( name = 'atom_symbols', length = 2 )
    atomSymbols.meta['tip'] = 'atom symbols for each position in the unit cell'

    pass # end of PolyXtalScatterer


# version
__id__ = "$Id$"

# End of file 
