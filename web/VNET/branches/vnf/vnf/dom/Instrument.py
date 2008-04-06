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


from DbObject import DbObject


class Instrument(DbObject):
    
    name = "instruments"
    
    import pyre.db
    
    from ReferenceSet import ReferenceSet
    class Components( ReferenceSet ):
        
        name = 'componentsininstrument'

        import pyre.db
        label = pyre.db.varchar( name = 'label', length = 128 )
        
        pass
    
    componentsequence = pyre.db.varcharArray(
        name = 'componentsequence', length = 128 )

    from PositionOrientationRegistry import PositionOrientationRegistry
    class Geometer( PositionOrientationRegistry ):

        name = 'instrumentgeometer'

        pass # end of Geometer
    
    pass # end of Instrument


# version
__id__ = "$Id$"

# End of file 
