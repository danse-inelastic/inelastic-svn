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
class IDFPhononDispersion(DbObject):

    name = 'idfphonondispersions'

    import pyre.db

    origin = pyre.db.varchar( name = 'origin', length = 1024 )

    pass # end of IDFPhononDispersion


# version
__id__ = "$Id$"

# End of file 
