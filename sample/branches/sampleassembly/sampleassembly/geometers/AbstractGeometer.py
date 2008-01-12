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


class AbstractGeometer( object):
    
    """Maintain positions and orientations of elements in a container.
    Measures displacements between elements.
    """


    def __init__(self, target):
        """ctor
        target system that this geometer will work on
        """
        self.target = target
        return


    def orientation( self, element):
        """orientation( element) -> orientation of element rel. to the container
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
          

    def register( self, element, offset, orientation, relative=None):
        """register( element, offset, orientation, relative=None) -> None
        Register an element.
        Inputs:
            element: the element to register. It must be a signature like
              "monitor1" or "moderator" or "funnel1".
              relative could be None or signature of another element.
               
            offset: displacement from "relative"'s reference point to
                    element's reference point.
            orientation: orientation of element, relative to "relative"
        Output:
            None
        Exceptions: ValueError
        """
        self._abstract( "register" )


    def getCoordinateSystemDescription( self):
        """getCoordinateSystemDescription() -> verbal description of current
        coordinate system"""
        self._abstract( "getCoordinateSystemDescription" )


    # throw an exception
    def _abstract(self, method):
        raise NotImplementedError(
            "class '%s' should override method '%s'" % (self.__class__.__name__, method))

    pass # end of AbstractGeometer


# version
__id__ = "$Id: Geometer.py 1156 2006-10-12 00:51:00Z linjiao $"

# End of file
