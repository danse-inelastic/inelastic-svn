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

def clerk():
    from Clerk import Clerk
    return Clerk( 'clerk', 'clerk' )


def scribe():
    from pyre.components.Component import Component
    return Component( 'scribe', 'scribe' )


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sat Mar 15 08:11:12 2008

# End of file 
