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
    #status = pyre.db.varchar( name = 'status', default = 'new', length = 16 )
    template = pyre.db.boolean( name = 'template', default = False)
    basic = pyre.db.boolean( name = 'basic', default = False)
    basic.meta['tip'] = (
        'Is this scatterer basic? basic scatterers are presented to novice users'
        )
    pass # end of Scatterer


# version
__id__ = "$Id$"

# End of file 
