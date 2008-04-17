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

    scheduler = server.scheduler
    if scheduler in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnf.clusterscheduler import scheduler as factory
    try: scheduler = factory( scheduler )
    except: raise NotImplementedError, 'scheduler %r' % scheduler

    scheduler = scheduler(
        lambda cmd: director.csaccessor.execute( cmd, job.id, server ),
        prefix = 'source ~/.vnf' )

    id1 = scheduler.submit( './run.sh' )

    job.id_incomputingserver = id1

    import time
    job.timestart = time.ctime()

    director.clerk.updateRecord( job )
    
    return


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
