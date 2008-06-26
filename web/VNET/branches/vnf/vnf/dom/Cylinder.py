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
class Cylinder(DbObject):

    name = 'cylinders'

    import pyre.db

    height = pyre.db.real( name = 'height', default = 0.1 )
    innerRadius = pyre.db.real( name = 'innerRadius', default = 0.0 )
    outerRadius = pyre.db.real( name = 'outerRadius', default = 0.002 )


# version
__id__ = "$Id$"

# End of file 
