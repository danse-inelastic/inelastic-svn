
basepath = 'content/runs'


def new_rundir( director ):
    #new token
    token = director.idd.token()
    uniquename = '%s-%s-%s' % (token.locator, token.tid, token.date)

    #make new run directory
    import os
    rundir = os.path.join( basepath, uniquename )
    os.makedirs( rundir )

    return rundir
