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


from DbObject import DbObject
class OwnedObject(DbObject):

    import pyre.db

    owner = pyre.db.varchar(name='owner', length = 32)
    owner.meta['tip'] = 'owner name'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    pass # end of Shape


# version
__id__ = "$Id$"

# End of file 
