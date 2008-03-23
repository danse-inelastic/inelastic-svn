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
class PolyXtalScatterer(Object):

    name = 'polyxtalscatterers'

    import pyre.db

    shape_id = pyre.db.varchar( name = 'shape_id', length = 100 )
    shape_id.meta['tip'] = 'reference id in the shape table. geometric shape of the scatterer'

    crystal_id = pyre.db.varchar( name = 'crystal_id', length = 100 )
    crystal_id.meta['tip'] = 'reference id in the crystal table. a single crystal of the scatterer'

    pass # end of PolyXtalScatterer


# version
__id__ = "$Id$"

# End of file 
