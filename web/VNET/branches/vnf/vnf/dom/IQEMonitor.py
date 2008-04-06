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
class IQEMonitor(DbObject):

    name = 'iqemonitors'

    import pyre.db

    Emin = pyre.db.real( name = 'Emin' )
    Emax = pyre.db.real( name = 'Emax' )
    nE = pyre.db.integer( name = 'nE' )

    Qmin = pyre.db.real( name = 'Qmin' )
    Qmax = pyre.db.real( name = 'Qmax' )
    nQ = pyre.db.integer( name = 'nQ' )

    max_angle_in_plane = pyre.db.real( name = 'max_angle_in_plane' )
    min_angle_in_plane = pyre.db.real( name = 'min_angle_in_plane' )
    max_angle_out_of_plane = pyre.db.real( name = 'max_angle_out_of_plane' )
    min_angle_out_of_plane = pyre.db.real( name = 'min_angle_out_of_plane' )
    
    pass # end of IQEMonitor


# version
__id__ = "$Id$"

# End of file 
