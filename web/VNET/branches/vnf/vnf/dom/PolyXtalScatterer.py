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


from Table import Table
class PolyXtalScatterer(Table):

    name = 'polyxtalscatterers'

    import pyre.db

    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    creater = pyre.db.varchar(name='creater', length = 32)
    creater.meta['tip'] = 'creater of polycrystal scatterer'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    short_description = pyre.db.varchar(name='short_description', length = 128)
    short_description.meta['tip'] = 'short description of scatterer'

    shape_id = pyre.db.varchar( name = 'shape_id', length = 100 )
    shape_id.meta['tip'] = 'reference id in the shape table. geometric shape of the scatterer'

    crystal_id = pyre.db.varchar( name = 'crystal_id', length = 100 )
    crystal_id.meta['tip'] = 'reference id in the crystal table. a single crystal of the scatterer'

    pass # end of PolyXtalScatterer


# version
__id__ = "$Id$"

# End of file 
