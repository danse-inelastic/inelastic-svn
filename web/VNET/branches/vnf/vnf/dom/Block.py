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
class Block(Object):

    name = 'blocks'

    import pyre.db

    x = pyre.db.real( name = 'x' )
    y = pyre.db.real( name = 'y' )
    z = pyre.db.real( name = 'z' )
    
    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
