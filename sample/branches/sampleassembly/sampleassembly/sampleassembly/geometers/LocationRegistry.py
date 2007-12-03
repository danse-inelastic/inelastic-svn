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


from _journal import debug


from CoordinateSystem import McStasCS
import CoordinateSystem


class LocationRegistry(object):

    '''Registry of position and orientation of geometrical
    objects.
    '''

    def __init__(self, target, coordinate_system = McStasCS):
        """
  - coordinate_system: the coordinate system. The position
    and orientation that are registered are expressed using
    this coordinate system.
    """
        self._coordinate_system = coordinate_system
        self._registry = {}
        self._target = target
        return


    def register( self, element, offset, orientation, relative=None):
        if self._registry.has_key(element):
            raise RuntimeError, "you have already registered %s before" % element
        
        self._registry[ element ] = relative, offset, orientation
        return


    def registered(self, element):
        return self._registry.get(element) is not None


    def location(self, element):
        ret = self._registry.get( element )
        if ret is None: 
            msg = "%s of %s: cannot find record for %s" % (
                self.__class__.__name__, self._target, element )
            raise ValueError, msg
        return ret

    def coordinate_system(self): return self._coordinate_system

    pass # end of Geometer


def main():
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file
