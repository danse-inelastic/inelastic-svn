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

    server = pyre.db.varchar(name='server', length = 32)
    server.meta['tip'] = 'server for computational work'

    location = pyre.db.varchar( name='location', length = 128)
    location.meta['tip'] = 'location of server'

    accessibility = pyre.db.varchar(name='accesibility', length = 128)
    accessibility.meta['tip'] = 'which group of users have access'
    
    reference = pyre.db.varchar(name='reference', length = 100 )
    reference.meta['tip'] = 'reference id in the table of the given type'


# version
__id__ = "$Id$"

# End of file 
