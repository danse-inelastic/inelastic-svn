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
        
        listjobs( jobValues, document, director )
        
        return page  


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Job, self).__init__(name)
        return



def listjobs( jobs, document, director ):
    
    p = document.paragraph()
    numJobs = len(jobs)

    from PyHtmlTable import PyHtmlTable
    t=PyHtmlTable(numJobs,5)#, {'width':'400','border':2,'bgcolor':'white'})
#    for row in range(numJobs):
#        for col in range(5):
#            t.setc(row,col,"T1 Cell 00")
    p.text = [t.display()]

    #from inventorylist import list
    #list( jobs, document, 'scatterer', director )
    return


def listsampleassemblies( sampleassemblies, document, director ):
    p = document.paragraph()

    n = len(sampleassemblies)

    p.text = [ 'There %s %s sampleassembl%s: ' %
               (present_be(n), n, plural(n, 'y'))
                ]

    from inventorylist import list
    list( sampleassemblies, document, 'sampleassembly', director )
    return



def noscatterer( document, director ):
    p = document.paragraph()

    link = action_link(
        actionRequireAuthentication(
        'scatterer',
        director.sentry,
        label = 'add',
        routine = 'new',
        ),  director.cgihome
        )
    
    p.text = [
        "There is no scatterer in this sample assembly. ",
        'Please %s a scatter.' % (
        director.cgihome, link)
        ]
    return


# version
__id__ = "$Id$"

# End of file 
