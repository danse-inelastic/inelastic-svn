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


from ElementContainer import ElementContainer
from debug import debug


class Scatterer( ElementContainer ):

    allowed_item_types = [
        'Scatterer',
        ]    

    class Attributes(Element.Attributes):

        import Attribute

        pass
        
    
    def __init__( self, name, shape = None, **attributes):
        """ Sample ctor
"""
        ElementContainer.__init__(
            self, name, shape = shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onScatterer( self)

    pass # end of Scatterer



# version
__id__ = "$Id: Scatterer.py 487 2005-06-22 22:52:09Z tim $"

# End of file
