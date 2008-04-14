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


# A "form" component is responsible to gather user inputs and
# transfor them to db.


from pyre.components.Component import Component as base


class Form( base ):

    class Inventory( base.Inventory ):
        import pyre.inventory
        pass # end of Inventory


    def __init__(self, name = 'form', facility = 'form'):
        base.__init__(self, name, facility)
        return


    def processUserInputs(self):
        'process user inputs and save them to db'
        return

    pass # end of Form


# version
__id__ = "$Id$"

# End of file 
