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
class Shape(Object):

    name = 'shapes'

    import pyre.db
    
    type = pyre.db.varchar( name = 'type', length = 10 )
    type.meta['tip'] = 'type of the shape'
    
    reference = pyre.db.varchar(name='reference', length = 100 )
    reference.meta['tip'] = 'reference id in the table of the given type'

    pass # end of Shape


# version
__id__ = "$Id$"

# End of file 
