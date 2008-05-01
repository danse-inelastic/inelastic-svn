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

    cartesianLattice = pyre.db.doubleArray(
        name = 'cartesianLattice', default = [])
    cartesianLattice.meta['tip'] = 'array of cartesian lattice vectors'
    
    fractionalCoordinates = pyre.db.doubleArray(
        name = 'fractional_coordinates', default = [])
    fractionalCoordinates.meta['tip'] = 'array positions as fractional values of unit cell'
    
    atomSymbols = pyre.db.varcharArray(
        name = 'atom_symbols', length = 2, default = [] )
    atomSymbols.meta['tip'] = 'atom symbols for each position in the unit cell'
    
    #shape_name = pyre.db.varchar( name = 'shape_name', length = 128 )
    #shape_name.meta['tip'] = 'the name of the shape: block, cylinder, etc.'
    
    #shape_parameters = pyre.db.varcharArray(
    #    name = 'shape_parameters', length = 128, default = [] )
    #shape_parameters.meta['tip'] = 'parameters of various sample shapes'




# version
__id__ = "$Id$"

# End of file 
