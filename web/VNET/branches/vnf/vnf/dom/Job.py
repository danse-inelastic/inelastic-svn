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


from Table import Table
class Job(Table):

    name = 'jobs'

    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    job = pyre.db.varchar(name='job', length = 32)
    job.meta['tip'] = 'computational job'

    server = pyre.db.varchar( name='server', length = 128)
    server.meta['tip'] = 'which server job is running on'

    timeCompletion = pyre.db.varchar(name='timeComletion', length = 128)
    timeCompletion.meta['tip'] = 'time left to completion'
    
    timeRun = pyre.db.varchar(name='timeRun', length = 128)
    timeRun.meta['tip'] = 'the amount of time the job has run'
    
    numProcessors = pyre.db.varchar(name='numProcessors', length = 128)
    numProcessors.meta['tip'] = 'the number of processors the jobs is using'
    
    reference = pyre.db.varchar(name='reference', length = 100 )
    reference.meta['tip'] = 'reference id in the table of the given type'


# version
__id__ = "$Id$"

# End of file 
