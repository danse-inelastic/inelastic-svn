#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication
from wording import plural, present_be


class Job(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'job' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of computational jobs')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        jobs = clerk.getJobs()
        jobValues=[]
        for job in jobs:
            jobValues.append(job.getValues())
        #get the number of columns of info about a representative job
        numColumns=jobs[0].getNumColumns() 
            
        p = document.paragraph()
        numJobs = len(jobs)
        numColumns=jobs[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numJobs,numColumns)#, {'width':'400','border':2,'bgcolor':'white'})
        for row in range(numJobs):
            colNum=0
            for name in jobs[row].getColumnNames():
                t.setc(row,colNum,jobs[row].getColumnValue(name))
                colNum+=1
        p.text = [t.return_html()]
        
        return page  


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Job, self).__init__(name)
        return



def new_job( director ):
    id = new_jobid( director )
    from vnf.dom.Job import Job
    job = Job()
    job.id = id
    job.owner = director.sentry.username
    director.clerk.newJob( job )
    return job


def new_jobid( director ):
    #new token
    token = director.idd.token()
    uniquename = '%s-%s-%s' % (token.locator, token.tid, token.date)
    return uniquename


def jobpath( jobid ):
    #make new run directory
    import os
    jobdir = os.path.join( basepath, jobid )
    os.makedirs( jobdir )

    return jobdir
basepath = 'content/jobs'


# version
__id__ = "$Id$"

# End of file 
