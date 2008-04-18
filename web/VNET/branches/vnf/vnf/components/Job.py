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


from Actor import action_link, action, actionRequireAuthentication, AuthenticationError
from wording import plural, present_be


from FormActor import FormActor as base


class Job(base):

    class Inventory(base.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"


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
        jobs = clerk.getJobs( where = 'owner=%r' % director.sentry.username )
            
        p = document.paragraph()

        numJobs = len(jobs)

        #get the number of columns of info about a representative job
        numColumns=jobs[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numJobs,numColumns, {'width':'400','border':2,'bgcolor':'white'})
        for row in range(numJobs):
            job = jobs[row]
            for colNum, colName in enumerate(job.getColumnNames()):
                value = job.getColumnValue(colName)
                if colName == 'id':
                    link = action_link(
                        actionRequireAuthentication(
                        'job',
                        director.sentry,
                        label = value,
                        routine = 'show',
                        id = value,
                        ),  director.cgihome
                        )
                    value = link
                    pass # endif
                        
                t.setc(row,colNum,value)
                colNum+=1
        p.text = [t.return_html()]
        
        return page


    def edit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        job = self.processFormInputs( director )
        
        document = main.document( title = 'Job editor' )

        formcomponent = self.retrieveFormToShow( 'job' )
        formcomponent.inventory.id = job.id
        formcomponent.director = director

        form = document.form(
            name='job',
            legend = formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'job', sentry = director.sentry,
            label = '', routine = 'submit',
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        submit = form.control(name="submit", type="submit", value="Submit")
        
        return page


    def show(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        id = self.inventory.id
        record = director.clerk.getJob( id )
        assert record.owner == director.sentry.username

        main = page._body._content._main
        document = main.document( title = 'Job # %s: %s' % (
            record.id, record.status ) )

        status = check( record, director )
        lines = ['%s=%s' % (k,v) for k,v in status.iteritems()]
        for line in lines:
            p = document.paragraph()
            p.text = [line]
            continue
        return page


    def submit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        job = self.processFormInputs( director )

        server = job.server
        server_record = director.clerk.getServer( server )

        try:
            schedule(job, director)
        except RemoteAccessError, err:
            import traceback
            self._debug.log( traceback.format_exc() )
            document = main.document( title = 'Job not submitted' )
            p = document.paragraph()
            p.text = [
                'Failed to submit job %s to %s' % (
                job.id, server_record.server, ),
                ]
            return page

        job.status = 'submitted'
        director.clerk.updateRecord( job )
        
        document = main.document( title = 'Job submitted' )
        p = document.paragraph()
        p.text = [
            'Job #%s has been submitted to %s' % (
            job.id, server_record.server, ),
            ]
            
        p = document.paragraph()
        p.text = [
            'You can click "Jobs" link on the left menu to see all of your jobs',
            ]
            
        return page


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Job, self).__init__(name)
        return


from Scheduler import schedule, check, RemoteAccessError


def new_job( director ):
    id = new_jobid( director )
    from vnf.dom.Job import Job
    job = Job()
    job.id = id
    director.clerk.newJob( job )

    job.owner = director.sentry.username
    job.status = 'created'
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

    if not os.path.exists( jobdir ):
        os.makedirs( jobdir )

    return jobdir
basepath = 'content/jobs'


# version
__id__ = "$Id$"

# End of file 
