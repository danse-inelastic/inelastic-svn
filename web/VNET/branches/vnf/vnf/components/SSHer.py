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


from CSAccessor import CSAccessor as base, RemoteAccessError

class SSHer(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        auth_sock = pyre.inventory.str( 'auth_sock', default = '' )

        pass # end of Inventory
    

    def __init__(self, *args, **kwds):
        base.__init__(self, *args, **kwds)
        return
    

    def push( self, path, server, remotepath ):
        'push a local directory to remote server'
        address = server.server
        username = server.username
        
        cmd = 'scp -r %s %s@%s:%s' % (
            path, username, address, remotepath )
        self._info.log( 'execute: %s' % cmd )

        env = {
            'SSH_AUTH_SOCK': self.inventory.auth_sock,
            }
        failed, output, error = spawn( cmd, env = env )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    def execute( self, cmd, server, remotepath ):
        'execute command in the given directory of the given server'

        address = server.server
        username = server.username

        cmd = 'cd %s && %s' % (remotepath, cmd)
        
        cmd = 'ssh %s@%s "%s"' % (username, address, cmd)

        self._info.log( 'execute: %s' % cmd )
        env = {
            'SSH_AUTH_SOCK': self.inventory.auth_sock,
            }
        failed, output, error = spawn( cmd, env = env )
        return failed, output, error


    pass # end of SSHer


import os
from spawn import spawn


# version
__id__ = "$Id$"

# End of file 
