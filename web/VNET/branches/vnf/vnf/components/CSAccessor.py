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


from pyre.components.Component import Component

class CSAccessor(Component):

    class Inventory(Component.Inventory):

        pass # end of Inventory
    

    def push( self, path, server ):
        'push a local directory to remote server'
        raise NotImplementedError 


class RemoteAccessError(Exception): pass


# version
__id__ = "$Id$"

# End of file 
