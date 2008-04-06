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


from DbObject import DbObject as base
class PolyXtalScatterer(base):

    name = 'polyxtalscatterers'

    import pyre.db

    shape_id = pyre.db.varchar( name = 'shape_id', length = 100 )
    shape_id.meta['tip'] = 'reference id in the shape table. geometric shape of the scatterer'

    crystal_id = pyre.db.varchar( name = 'crystal_id', length = 100 )
    crystal_id.meta['tip'] = 'reference id in the crystal table. a single crystal of the scatterer'

    from ReferenceSet import ReferenceSet
    class Kernels( ReferenceSet ):
        name = 'kernelsforpolyxtalscatterer'
        pass

    pass # end of PolyXtalScatterer


# version
__id__ = "$Id$"

# End of file 
