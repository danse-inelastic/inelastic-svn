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


from opal.components.Actor import Actor


from Action import Action
def action( *args, **kwds ): return Action( *args, **kwds )

from ActionRequireAuthentication import ActionRequireAuthentication
def actionRequireAuthentication(*args, **kwds): return ActionRequireAuthentication( *args, **kwds )


def action_link(action, cgihome):
    from ActionLinkRenderer import ActionLinkRenderer
    renderer = ActionLinkRenderer( cgihome )
    return renderer.render( action )


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Mar 14 22:18:28 2008

# End of file 
