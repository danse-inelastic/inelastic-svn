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
class Block(Table):

    name = 'blocks'


    import pyre.db

    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    creater = pyre.db.varchar(name='creater', length = 32)
    creater.meta['tip'] = 'creater of this block'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    x = pyre.db.real( name = 'x' )
    y = pyre.db.real( name = 'y' )
    z = pyre.db.real( name = 'z' )
    
    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
