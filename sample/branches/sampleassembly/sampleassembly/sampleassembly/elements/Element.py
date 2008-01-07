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


from _journal import debug



class Element(object):
    
    """Instrument element base class"""

    from AttributeContainer import AttributeContainer
    class Attributes(AttributeContainer):

        from Attribute import int
        guid = int( 'guid', default = -1 )

        id = int('id', default = -1 )
        id.meta['tip'] = 'local id'

        pass # end of Attributes


    def parent(self): return self._parent


    def guid( self):
        """This element's Global Unique Identifier"""
        return self.attributes.guid


    def id(self):
        '''This element\'s local id'''
        return self.attributes.id


    def shape(self):
        '''shape() --> geometric shape of this element
        '''
        return self._shape


    def setShape(self, shape): self._shape = shape


    def identify( self, visitor):
        '''identify myself to visitor

        the interface requited by visitor pattern
        '''
        return visitor.onElement( self)


    def __init__( self, name, shape=None, **attributes):
        """Element( name, guid, shape, attributes) --> new element
        """
        self.name = name

        #for now, I don't know my parent. after I am added to a container
        #my _setParent will be called and I get to know my parent.
        self._setParent( None )

        #my geometric shape
        self._shape = shape

        # init my attribute container
        self.attributes = self.Attributes( name )
        
        # transfer inputs to my attribute container
        if attributes is None: attributes = {}
        attributes['name'] = name
        for k, v in attributes.iteritems():
            self.attributes.set( k,v )
            continue
        return


    def __getattribute__(self, name):
        # bypass all normal attributes
        if name.startswith('__'): 
            return object.__getattribute__(self,name)
        
        if name in dir(self):
            return object.__getattribute__(self,name)
        
        if name in dir(self.__class__):
            return object.__getattribute__(self,name)

        # physical attributes of this element inside the attribute container
        if name in self.attributes:
            # lambda expression allows us to have interface like this:
            #   detector.pressure()
            return lambda : self._getProperty( name )
        raise AttributeError, '%r' % name


    def __str__(self):
        klass = str(self.__class__.__name__)
        name = self.name

        attributes = []
        for key in self.attributes:
            value = self.attributes.get( key )
            attributes.append( '%s=%s' % (key, value) )
            continue

        return '%s(%s): %s' % (
            klass, name,
            ','.join( attributes ) )


    # get property, either physical or geometrical
    def _getProperty(self, name):
        try: return eval('self.attributes.%s' % name)
        except: return eval('self._shape.%s' % name)
        raise "should not reach here"
    

    # methods for friends
    def _setParent(self, p): self._parent = p

    def _getRoot(self): return _getRoot(self)

    def _setGuid(self, guid):
        self.attributes.guid = guid
        return


    pass # end of Element


def isElement(c): return isinstance(c, Element)

def _getRoot( element ):
    parent = element.parent()
    if parent is None:
        from Instrument import Instrument
        debug.log(element.__class__)
        assert element.__class__.__name__ =='Instrument'
        #assert isinstance( element, Instrument )
        return element
    return _getRoot( parent )

    
import unittest

from unittest import TestCase
class Element_TestCase(TestCase):

    def test(self):
        element = Element( 'element11' )
        self.assertEqual( element.shape(), None )
        self.assertEqual( element.name, 'element11' )

        element = Element( 'element11', guid = 11 )
        self.assertEqual( element.guid(), 11 )
        return


    def test2(self):
        class Moderator(Element):
            class Attributes(Element.Attributes):
                import Attribute
                type = Attribute.str( "type", default = "")
        m = Moderator( 'm', type = 'hi' )
        self.assertEqual( m._getProperty( 'type' ), 'hi' )
        self.assertEqual( m.type(), 'hi' )
        return
        

    pass # end of Element_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Element_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Element.py 1271 2007-10-26 23:48:04Z linjiao $"

# End of file
