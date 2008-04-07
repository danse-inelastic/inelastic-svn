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
        fail, output, error = spawn( cmd, env = env )
        if fail:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return 


    pass # end of SSHer


from spawn import spawn


# version
__id__ = "$Id$"

# End of file 
