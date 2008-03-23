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
class Server(Table):

    name = 'servers'

    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    server = pyre.db.varchar(name='server', length = 128)
    server.meta['tip'] = 'name of server'

    location = pyre.db.varchar( name='location', length = 128)
    location.meta['tip'] = 'location of server'

    groupAccess = pyre.db.varchar(name='groupAccess', length = 128)
    groupAccess.meta['tip'] = 'which group of users has access to the server'
    
    reference = pyre.db.varchar(name='reference', length = 100 )
    reference.meta['tip'] = 'reference id in the table of the given type'


# version
__id__ = "$Id$"

# End of file 
