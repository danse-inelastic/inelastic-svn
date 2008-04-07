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


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError
from wording import plural, present_be


class Job(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"

        name = pyre.inventory.str( 'name', default = 'jobname' )

        server = pyre.inventory.str( 'server', default = 'serverid' )

        numprocessors = pyre.inventory.int( 'numprocessors', default = 1 )
        
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


    def edit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        id = self.inventory.id
        
        document = main.document( title = 'Job editor' )

        job = director.clerk.getJob( id )

        objtype = job.__class__
        objtypename = objtype.__name__
        
        form = document.form(
            name=objtypename,
            legend='Job #%s' % job.id,
            action=director.cgihome)

        actor = 'job'
        actor_field = form.hidden(name='actor', value=actor)
        routine_field = form.hidden(name='routine', value='submit')
        id_field = form.hidden(
            name = '%s.id' % actor, value = id)
        
        username_filed = form.hidden(
            name='sentry.username', value = director.sentry.username)
        ticket_filed = form.hidden(
            name='sentry.ticket', value = director.sentry.ticket)

        # properties of a job
        field = form.text(
            id = 'name',
            name = '%s.name' % actor,
            label = 'name',
            value = job.jobName )

        servers = director.clerk.getServers()
        entries = [ (server.id, server.server) for server in servers ]
        ids = [ id for id, server in entries ]

        selected_server = job.server
        if selected_server not in ids: selected_server = entries[0][0]
        
        import opal.content
        selector = opal.content.selector(
            name = '%s.server' % actor,
            entries = entries,
            label = 'server',
            selected = selected_server,
            )
        form.contents.append( selector )

        field = form.text(
            id = 'numprocessors',
            name = '%s.numprocessors' % actor,
            label = 'number of processors',
            value = job.numprocessors,
            )

        submit = form.control(name="submit", type="submit", value="Submit")
        
        return page


    def submit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        id = self.inventory.id
        name = self.inventory.name
        server = self.inventory.server
        numprocessors = self.inventory.numprocessors

        job = director.clerk.getJob( id )
        job.jobName = name
        job.server = server
        job.numprocessors = numprocessors

        director.clerk.updateRecord( job )
        
        schedule(job)

        document = main.document( title = 'Job submitted' )
        p = document.paragraph()

        server_record = director.clerk.getServer( server )
        
        p.text = [
            'Job #%s has been submitted to %s' % (
            job.id, server_record.server, ),
            ]
            
        return page


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Job, self).__init__(name)
        return


def schedule( job ):
    return


def new_job( director ):
    id = new_jobid( director )
    from vnf.dom.Job import Job
    job = Job()
    job.id = id
    director.clerk.newJob( job )

    job.owner = director.sentry.username
    import time
    job.timeStart = job.timeCompletion = time.ctime()

    servers = director.clerk.getServers()
    server = servers[0]
    job.server = server.id

    job.numprocessors = 1
    
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
