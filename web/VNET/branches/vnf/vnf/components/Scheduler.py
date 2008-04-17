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

    id1 = director.csaccessor.execute(
        submit_cmd( "./run.sh" ),
        job.id, server )

    job.id_incomputingserver = id1

    import time
    job.timestart = time.ctime()

    director.clerk.updateRecord( job )
    
    return


def submit_cmd( cmd ):
    return r'source ~/.vnf ;  echo \"%s\" | qsub' % cmd


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
