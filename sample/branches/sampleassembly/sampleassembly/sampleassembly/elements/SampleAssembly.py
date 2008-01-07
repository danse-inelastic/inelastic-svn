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
from _journal import debug


class SampleAssembly( ElementContainer ):

    allowed_item_types = [
        'PowderSample',
        ]    

    class Attributes(ElementContainer.Attributes):

        import Attribute
        
        pass
        

    def __init__( self, name, shape = None, **attributes):
        """ Sample ctor
"""
        ElementContainer.__init__(
            self, name, shape = shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onSampleAssembly( self)

    pass # end of SampleAssembly



# version
__id__ = "$Id: SampleAssembly.py 487 2005-06-22 22:52:09Z tim $"

# End of file
