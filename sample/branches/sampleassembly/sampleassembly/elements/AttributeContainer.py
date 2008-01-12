#!/usr/bin/env python
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

from AbstractAttributeContainer import AbstractAttributeContainer

from pyre.inventory.Inventory import Inventory
class AttributeContainer( Inventory, AbstractAttributeContainer ):

    from Attribute import str
    name = str( 'name' )
    

    def set(self, name, value):
        exec "self.%s = value" % name
        return


    def get(self, name):
        exec "value = self.%s" % name
        return value


    def __iter__(self):
        props = self.propertyNames()
        return props.__iter__()


    def copy(self):
        ret = self.__class__( self.name )
        for k in self: ret.set( k, self.get( k ) )
        return ret
    
    pass


def test():

    from AbstractAttributeContainer import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            class AC(AttributeContainer):
                from Attribute import str
                hello = str( 'hello' )
                pass

            self.attributeContainer = AC( 'test' )
            return

        pass

    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 

