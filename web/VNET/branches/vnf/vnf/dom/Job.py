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

    jobName = pyre.db.varchar(name='jobName', length = 128)
    jobName.meta['tip'] = 'computational job name'

    server = pyre.db.varchar( name='server', length = 128)
    server.meta['tip'] = 'which server job is running on'

    timeCompletion = pyre.db.timestamp(name='timeCompletion')
    timeCompletion.meta['tip'] = 'time left to completion'
    
    timeStart = pyre.db.timestamp(name='timeStart')
    timeStart.meta['tip'] = 'the time the job started'
    
    numProcessors = pyre.db.integer(name='numProcessors')
    numProcessors.meta['tip'] = 'the number of processors the jobs are using'
    
#    reference = pyre.db.varchar(name='reference', length = 100 )
#    reference.meta['tip'] = 'reference id in the table of the given type'


# version
__id__ = "$Id$"

# End of file 
