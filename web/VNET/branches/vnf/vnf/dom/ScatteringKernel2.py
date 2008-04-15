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
class ScatteringKernel2(DbObject):
    
    name = 'scatteringkernel'

    import pyre.db
    
    texture = pyre.db.varchar(name="texture", length=100)
    texture.meta['tip'] = "either polycrystal, single crystal, or disordered"



# version
__id__ = "$Id$"

# End of file 
