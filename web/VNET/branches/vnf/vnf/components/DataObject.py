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


class DataObject(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        id = pyre.inventory.str( 'id', default = '' )

        creater = pyre.inventory.str(name='creater', default = '')

        date = pyre.inventory.str( name='date', default = '' )

        short_description = pyre.inventory.str(name='short_description')
        pass # end of Inventory


    def __init__(self, name):
        Component.__init__(self, name, facility='dataobject')
        return


# version
__id__ = "$Id$"

# End of file 
