#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


msg = "%s must override %s"


class AbstractAttributeContainer( object):
    """attribute container interface"""


    def __init__(self, name):
        self.name = name
        return
    

    def get( self, name):
        """get( name) -> value"""
        raise NotImplementedError, msg%(self.__class__.__name__, 'get')


    def set( self, name, value):
        """set( name, value) -> None"""
        raise NotImplementedError, msg%(self.__class__.__name__, 'set')


    def __iter__(self):
        raise NotImplementedError, msg%(self.__class__.__name__, '__iter__')


    def copy(self):
        raise NotImplementedError, msg%(self.__class__.__name__, 'copy')

##     def next( self ):
##         raise NotImplementedError, msg%(self.__class__.__name__, 'next')


    pass # end of AbstractAttributeContainer



import unittest as ut

class TestCase(ut.TestCase):

    def setUp(self):
        # overload this to test a special subclass of AbstractAttributeContainer
        self.attributeContainer = None
        return


    def test_setget(self):
        "AttributeContainer: set and get"
        ac = self.attributeContainer
        ac.set( "hello", '1' )
        self.assertEqual( ac.get( "hello" ), '1' )
        return


    def test_iter(self):
        "AttributeContainer: iteration"
        ac = self.attributeContainer
        ac.set( "hello", 1 )
        for i in ac: print i
        return


    def test_copy(self):
        "Attributecontainer: copy"
        ac = self.attributeContainer
        acc = ac.copy()
        for i in ac: self.assertEqual( ac.get(i), acc.get(i) )
        return

    pass



# version
__id__ = "$Id$"

# End of file 
