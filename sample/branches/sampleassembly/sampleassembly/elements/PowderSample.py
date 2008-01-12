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


from Element import Element
from _journal import debug


class PowderSample( Element ):

    allowed_item_types = [
        ]    

    class Attributes(Element.Attributes):

        import Attribute
        # need more attributes here
        pass
        

    def __init__( self, name, shape = None, **attributes):
        """create a powder sample
"""
        Element.__init__(
            self, name, shape = shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onPowderSample( self )

    pass # end of PowderSample



# version
__id__ = "$Id: PowderSample.py 487 2005-06-22 22:52:09Z linjiao $"

# End of file
