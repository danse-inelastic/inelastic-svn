# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject
class GulpDynamicsKernel(OwnedObject):

    name = 'gulpscatteringkernels'
    
    import pyre.db

    inputFile = pyre.db.varcharArray( name = 'inputFile', length = 256 )
    inputFile.meta['tip'] = 'input file to run gulp'



# version
__id__ = "$Id$"

# End of file 
