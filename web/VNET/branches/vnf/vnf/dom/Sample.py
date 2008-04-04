# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Object import Object
class Sample(Object):

    name = 'samples'

    import pyre.db

    sampleName = pyre.db.varchar( name = 'sampleName', length = 128 )
    sampleName.meta['tip'] = 'name of sample'

    cartesianLattice = pyre.db.doubleArray( name = 'cartesianLattice')
    cartesianLattice.meta['tip'] = 'array of cartesian lattice vectors'
    
    fractionalCoordinates = pyre.db.doubleArray( name = 'fractional_coordinates')
    fractionalCoordinates.meta['tip'] = 'array positions as fractional values of unit cell'
    
    atomNames = pyre.db.varcharArray( name = 'fracti')
    fractionalCoordinates.meta['tip'] = 'array positions as fractional values of unit cell'

    pass # end of PolyXtalScatterer


# version
__id__ = "$Id$"

# End of file 
