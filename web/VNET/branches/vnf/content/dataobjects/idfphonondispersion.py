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



from vnf.components.DataObject import DataObject as base


class IDFPhononDispersion(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def __init__(self, name = None):
        if name is None:
            name = 'idfphonondispersion'

        base.__init__(self, name)

        return



def dataobject(): return IDFPhononDispersion()

# version
__id__ = "$Id$"

# End of file 
