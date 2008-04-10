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



import journal
info = journal.info( 'scheduler' )


def schedule( job, director ):
    from Job import jobpath
    path = jobpath( job.id )

    server_id = job.server
    server = director.clerk.getServer( server_id )
    
    director.csaccessor.push( path, server )
    #director.csaccessor.execute( 'nohup ./run.sh', path, server )
    
    return


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
