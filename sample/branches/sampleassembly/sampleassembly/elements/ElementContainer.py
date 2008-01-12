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


from elementTypes import typeFromName

from Element import Element, debug


class ElementContainer( Element ):

    allowed_item_types = ['Element']

    def __init__( self, name, shape = None, children = None,
                  **attributes):
        Element.__init__(self, name, shape, **attributes)

        from IdGenerator import IdGenerator
        self._idGenerator = IdGenerator()

        #containers
        self._elements = []
        self._id2element = {}
        self._name2element = {}
        self._name2id = {}

        #add children
        if children is None: children = []
        for child in children: self.addElement( child )
        return


    def identify( self, visitor):
        return visitor.onElementContainer( self)


    def replace(self, old, new):
        'replace an old subelement by a new one'
        if old not in self._elements:
            raise ValueError, "no such element: %s" % (old, )
        index = self._elements.index( old)
        #remove old element
        del self._elements[ index ]
        del self._id2element[ old.id() ]
        del self._name2element[ old.name ]
        del self._name2id[ old.name ]
        #add the new element
        self.addElement( new )
        #need to adjust the sequence
        del self._elements[-1]
        self._elements.insert( index, new )
        return
        

    def addElement( self, element):
        good = False
        for type in self.allowed_item_types:
            if isinstance(element, typeFromName(type) ): good = True
            continue
        if not good:
            raise TypeError , "%s(type=%s) is not allowed in this container"\
                  " %s(type=%s). Allowed elements are: %s" % (
                element.name, element.__class__.__name__,
                self.name, self.__class__.__name__,
                self.allowed_item_types)
        
        element._setParent( self )
        
        id = element.id()
        #assign id if necessary
        if id < 0:
            id = element.attributes.id = self._idGenerator.getUniqueID()
        else:
            self._idGenerator.usedId.append( element.id() )

        name = element.name
        if id not in self._id2element and name not in self._name2element:
            self._id2element[ id] = element
            self._name2element[ name ] = element
            self._elements.append( element )
            self._name2id[ name ] = id
        else:
            msg = "That element %r (id=%s) is already registered" % (
                name, id)
            raise ValueError, msg
        return


    def deleteElement(self, element):
        id = element.id()
        if id not in self._id2element: raise ValueError , "%s is not a sub element of %s" % (element.name, self.name)
        del self._id2element[ id ]
        del self._elements[ self._elements.index( element ) ]
        return


    def elements(self): return self._elements


    def elementFromName(self, name):
        'return child element given its name'
        return self._name2element[ name ]


    def elementFromId( self, id ):
        'return child element given its name'
        if id not in self._id2element:
            raise ValueError , "%s(%s): no such id: %s. current ids: %s" % (
                self.name, self.__class__.__name__,
                id, self._id2element.keys() )
        return self._id2element[ id ]
    

    def _getDescendent(self, identifier):
        if len(identifier) == 0: return self
        path = identifier.split( '/' )
        son = self.elementFromName( path[0] )
        if not (isElementContainer(son) or isCopy(son)):
            if len(path) > 1:
                msg = 'element container %r does not have a descendent %r.' %(
                    self.name, identifier )
                msg += 'The descendent %r is already an element that does not'\
                       ' have children' % (son.name, )
                raise RuntimeError , msg
            return son
        return son._getDescendent( '/'.join( path[1:] ) )
        

    def _getDescendentFromIndexTuple(self, indexTuple):
        if len(indexTuple) == 0: return self
        son = self.elementFromId( indexTuple[0] )
        if not (isElementContainer(son) or isCopy(son)):
            if len(indexTuple) > 1:
                msg = 'element container %r does not have a descendent %r.' %(
                    self.name, indexTuple )
                msg += 'The descendent %r is already an element that does not'\
                       ' have children' % (son.name, )
                raise RuntimeError , msg
            return son
        return son._getDescendentFromIndexTuple( indexTuple[1:] )


    def _indexTupleFromPath(self, path):
        '''return a tuple of indexes leading to an element given its path
        
  path: sth like "detectorSystem/detarr2/detpack3/dettube5"
  return: sth like (3,2,3,5)
  '''
        if len(path) == 0 or path == '/': return tuple()
        path = path.split('/')
        id = self._name2id[ path[0] ]
        element = self._name2element[ path[0] ]
        if len(path)==1: return id,
        ret = (id,) + element._indexTupleFromPath( '/'.join( path[1:] ) )
        return ret
    

    def __len__( self):
        return len( self._elements)


    def __iter__(self): return self._elements.__iter__()
    
    pass # end of ElementContainer
    


def isElementContainer(c): return isinstance(c, ElementContainer)
def isCopy(c):
    from Copy import Copy
    return isinstance(c, Copy)


import unittest

from unittest import TestCase
class Element_TestCase(TestCase):

    def setUp(self):
        class EC(ElementContainer):
            allowed_item_types = ['Element']
            pass
        self.EC = EC
        
        self.e1 = e1 = Element( "e1")
        e2 = Element( "e2" )
        self.ec1 = ec1 = EC( "ec1" )
        ec1.addElement( e1 )
        ec1.addElement( e2 )
        e3 = Element( "e3" )
        ec2 = EC( "ec2" )
        ec2.addElement( ec1 )
        ec2.addElement( e3 )
        self.ec2 = ec2
        return
    

    def test_len( self ):
        "ElementContainer: len()"""
        self.assertEqual( len(self.ec2), 2 )
        return


    def test_iter(self):
        "ElementContainer: __iter__"""
        for e in self.ec2: print e
        return


    def test_delete(self):
        "ElementContainer: __iter__"""
        ec = self.EC( 'ec' )
        e = Element( 'e'  )
        ec.addElement( e )
        ec.deleteElement( e )
        self.assertRaises( ValueError, ec.deleteElement, e )
        return        
    

    def test_elements( self ):
        "ElementContainer: elements"""
        elements = self.ec2.elements()
        return


    def test_addWrongElement(self):
        'ElementContainer: add element of wrong type'
        ec = ElementContainer('ec' )
        self.assertRaises( TypeError, ec.addElement, Element( 'e' )  )
        return


    def test_elementFromName(self):
        'ElementContainer: elementFromName'
        ec1 = self.ec1
        e1 = ec1.elementFromName( 'e1' )
        self.assertEqual( e1.name, 'e1' )
        self.assertEqual( e1.parent(), ec1 )
        return


    def test_elementFromId(self):
        'ElementContainer: elementFromId'
        ec1 = self.ec1
        e1 = ec1.elementFromId( 0 )
        self.assertEqual( e1.name, 'e1' )
        self.assertEqual( e1.parent(), ec1 )
        return


    def test_getDescendnet(self):
        'ElementContainer: getDescendent'
        ec2 = self.ec2
        t = ec2._getDescendent( 'ec1/e1' )
        self.assertEqual( t, self.e1 )
        return


    def test_getDescendnetFromId(self):
        'ElementContainer: getDescendent'
        ec2 = self.ec2
        t = ec2._getDescendentFromIndexTuple( (0,0) )
        self.assertEqual( t, self.e1 )
        return


    def test__indexTupleFromPath(self):
        'ElementContainer: _indexTupleFromPath'
        ec2 = self.ec2
        indexes = ec2._indexTupleFromPath( 'ec1/e1' )
        self.assertEqual( indexes[0], 0 )
        self.assertEqual( indexes[1], 0 )
        indexes = ec2._indexTupleFromPath( '' )
        self.assertEqual( indexes, tuple() )
        return


    def test_replace(self):
        'ElementContainer: replace'
        class EC(ElementContainer):
            allowed_item_types = ['Element']
            pass
        e1 = Element( "e1")
        e2 = Element( "e2" )
        
        ec1 = EC( "ec1" )
        ec1.addElement( e1 ) ; ec1.addElement(e2)

        e3 = Element( 'e3' )
        ec1.replace( e1, e3 )

        self.assertEqual( ec1.elements()[0], e3 )
        self.assertEqual( ec1.elements()[1], e2 )
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
__id__ = "$Id: ElementContainer.py 1271 2007-10-26 23:48:04Z linjiao $"

# End of file
