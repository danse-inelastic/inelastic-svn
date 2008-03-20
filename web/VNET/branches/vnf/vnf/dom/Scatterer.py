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
class Scatterer(Table):

    name = 'scatterers'

    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    creater = pyre.db.varchar(name='creater', length = 32)
    creater.meta['tip'] = 'creater of scatterer'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    short_description = pyre.db.varchar(name='short_description', length = 128)
    short_description.meta['tip'] = 'short description of scatterer'

    type = pyre.db.varchar( name = 'type', length = 10 )
    type.meta['tip'] = 'type of the scatterer'
    
    reference = pyre.db.varchar(name='reference', length = 100 )
    reference.meta['tip'] = 'reference id in the table of the given type'

    pass # end of Scatterer


# version
__id__ = "$Id$"

# End of file 
