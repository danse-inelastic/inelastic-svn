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


class IdGenerator:


    def __init__(self):
        self._idCounter = -1
        self.usedId = []
        return


    def getUniqueID( self):
        """getUniqueID() -> id
        get an identifier that is unique for this generator
        Input:
            None
        Output:
            id: integer
        Exceptions: None
        Notes: Right now, just using integers."""
        while 1:
            self._idCounter += 1
            ret = self._idCounter
            if ret not in self.usedId:
                return ret
            continue
        raise RuntimeError , "should not reach here"


# version
__id__ = "$Id$"

# End of file
