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

        remote_username = pyre.inventory.str( 'remote_username', default = 'vnf' )

        remote_workdir = pyre.inventory.str( 'remote_workdir', default = 'jobs' )
        
        pass # end of Inventory
    

    def __init__(self, *args, **kwds):
        base.__init__(self, *args, **kwds)
        return
    

    def push( self, path, server ):
        'push a local directory to remote server'
        address = server.server
        directory = self.inventory.remote_workdir
        username = self.inventory.remote_username
        
        cmd = 'scp -r %s %s@%s:%s' % (
            path, username, address, directory )

        env = {
            'SSH_AUTH_SOCK': self.inventory.auth_sock,
            }
        failed, output, error = spawn( cmd, env = env )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    def execute( self, cmd, directory, server ):
        'execute command in the given directory of the given server'

        address = server.server
        workdir = self.inventory.remote_workdir
        username = self.inventory.remote_username

        path = os.path.join( workdir, directory )

        cmd = 'cd %s && %s' % (path, cmd)
        
        cmd = 'ssh %s@%s %s' % (username, address, cmd)

        env = {
            'SSH_AUTH_SOCK': self.inventory.auth_sock,
            }
        failed, output, error = spawn( cmd, env = env )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg

        return


    pass # end of SSHer


import os
from spawn import spawn


# version
__id__ = "$Id$"

# End of file 
