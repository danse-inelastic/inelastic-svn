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


class SampleAssembly(DbObject):

    name = "sampleassemblies"
    
    import pyre.db

    status = pyre.db.varchar( name = 'status', default = 'new', length = 16 )
    
    from ReferenceSet import ReferenceSet
    class Scatterers( ReferenceSet ):
        name = 'scatterersinsampleassembly'
        pass

    pass # end of SampleAssembly


# version
__id__ = "$Id$"

# End of file 
