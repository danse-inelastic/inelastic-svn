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
class PolyXtalCoherentPhononScatteringKernel(Object):

    name = 'polyxtalcoherentphononscatteringkernels'
    
    import pyre.db

    dispersion_id = pyre.db.varchar( name = 'dispersion_id', length = 100 )
    dispersion_id.meta['tip'] = 'reference id in the dispersion table'
    
    max_energy_transfer = pyre.db.varchar( name = 'max_energy_transfer', length = 10 )

    max_momentum_transfer = pyre.db.varchar( name = 'max_momentum_transfer', length = 10 )

    pass # end of PolyXtalCoherentPhononScatteringKernel


# version
__id__ = "$Id$"

# End of file 
