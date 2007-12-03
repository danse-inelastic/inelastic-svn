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


class AbstractGlobalGeometer( object):
    
    """Maintain positions and orientations of elements in a hierarchial structure.
    each layer in the hierarchy will have a local geometer.
    
    measures displacements between elements."""


    def __init__(self, target):
        """ctor
        target system that this geometer will work on
        """
        self.target = target
        return


    def displacement( self, element1, element2):
        """displacement( el1, el2) -> vector from el2 to el1
        """
        self._abstract( "displacement" )


    def distance(self, element1, element2 ):
        """distance( el1, el2) -> distance between el2 and el1
        """
        self._abstract( "distance" )


    def orientation( self, element):
        """orientation( element) -> orientation of element rel. to absolute
        coordinate system.
        List of three angles.
        Use changeCoordinateSystem to change the coordinate system 
        Use getCoordinateSystemDescription to get description of the current coordinate
          system.
        """
        self._abstract( "orientation" )
        

    def position( self, element):
        """position( element) -> displacement of element's reference point
        from parent's reference point
        Use changeCoordinateSystem to change the coordinate system 
        Use getCoordinateSystemDescription to get description of the current coordinate
          system.
        """
        self._abstract( "position" )
          

    def getCoordinateSystemDescription( self):
        """getCoordinateSystemDescription() -> verbal description of current
        coordinate system"""
        self._abstract( "getCoordinateSystemDescription" )


    # throw an exception
    def _abstract(self, method):
        raise NotImplementedError(
            "class '%s' should override method '%s'" % (self.__class__.__name__, method))

    pass # end of AbstractGlobalGeometer


# version
__id__ = "$Id: Geometer.py 1156 2006-10-12 00:51:00Z linjiao $"

# End of file
