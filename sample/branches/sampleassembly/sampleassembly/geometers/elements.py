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


# This module contains example classes Element and ElementContainer.
# They are used to demonstrate the capability of geometers, but
# not for real use.

class Element(object): 
    def __init__(self, name, *args): 
        self.name = name
        return
    def __str__(self): return "%s" % self.name
    __repr__ = __str__

class ElementContainer(Element):
    def __init__(self, name, *args):
        Element.__init__(self, name)
        self._elements = []
        self._name2element = {}
        return
    def addElement(self, element): 
        element.id = len(self._elements)
        self._elements.append(element)
        self._name2element[element.name] = element
        return
    def elements(self): return self._elements
    def elementFromId(self,id): return self._elements[ id ]
    def elementFromName(self, name): return self._name2element[ name ]
    def _getDescendent(self, identifier):
        """return the descendent of this container given a '/' delimited
    string.
    Example: _getDescendent( 'pack1/tube3/pixel10' ) 
    """
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
        """return the descendent of this container given a tuple of indexes
    string.
    Example: _getDescendent( (1,3,10) ) 
    """
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

def isElementContainer(candidate): return isinstance(candidate, ElementContainer)


class Copy(object):
    def __init__(self, name, reference):
        self.name = name
        self.reference = reference
    def __getattribute__(self, name):
        try: return object.__getattribute__( self, name )
        except AttributeError :
            return self.reference.__getattribute__(name)
        raise RuntimeError , "should not reach here"
def isCopy(candidate): return isinstance( candidate, Copy )
    

instrument = detectorSystem = detectorPack = detector = ElementContainer
sample = moderator = monitor = Element


# version
__id__ = "$Id$"

# End of file 
