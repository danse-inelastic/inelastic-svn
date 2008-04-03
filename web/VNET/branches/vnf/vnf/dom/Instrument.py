# -*- Python -*-
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


from Object import Object


class Instrument(Object):

    name = "instruments"
    
    import pyre.db
    
    from ReferenceSet import ReferenceSet
    class Components( ReferenceSet ):
        name = 'componentsininstrument'
        pass

    pass # end of Instrument


# version
__id__ = "$Id$"

# End of file 
