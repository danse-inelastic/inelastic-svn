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


from VirtualObject import VirtualObject
class Scatterer(VirtualObject):

    name = 'scatterers'

    import pyre.db
    status = pyre.db.varchar( name = 'status', default = 'new', length = 16 )
    
    pass # end of Scatterer


# version
__id__ = "$Id$"

# End of file 
