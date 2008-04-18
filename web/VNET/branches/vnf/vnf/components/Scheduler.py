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

    # copy local job directory to server
    director.csaccessor.push( path, server, server.workdir )
    server_jobpath = remote_jobpath( server, job )

    scheduler = schedulerfactory( server )
    scheduler = scheduler(
        lambda cmd: director.csaccessor.execute( cmd, server, server_jobpath ),
        prefix = 'source ~/.vnf' )
    
    id1 = scheduler.submit( 'sh %s/run.sh' % server_jobpath )

    job.id_incomputingserver = id1

    import time
    job.timestart = time.ctime()

    director.clerk.updateRecord( job )
    
    return


def check( job, director ):
    "check status of a job"

    server_id = job.server
    server = director.clerk.getServer( server_id )
    scheduler = schedulerfactory( server )

    server_jobpath = remote_jobpath( server, job )
    
    launch = lambda cmd: director.csaccessor.execute( cmd, server, server_jobpath )

    scheduler = scheduler(
        launch,
        prefix = 'source ~/.vnf' )

    return scheduler.status( job.id_incomputingserver )



def remote_jobpath( server, job ):
    import os
    return os.path.join(server.workdir, job.id )    


def schedulerfactory( server ):
    'obtain scheduler factory'
    scheduler = server.scheduler
    if scheduler in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnf.clusterscheduler import scheduler as factory
    try: scheduler = factory( scheduler )
    except: raise NotImplementedError, 'scheduler %r' % scheduler
    return scheduler


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
