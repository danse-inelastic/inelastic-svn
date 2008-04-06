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
class Block(DbObject):

    name = 'blocks'

    import pyre.db

    width = pyre.db.real( name = 'width' )
    height = pyre.db.real( name = 'height' )
    thickness = pyre.db.real( name = 'thickness' )
    
    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
