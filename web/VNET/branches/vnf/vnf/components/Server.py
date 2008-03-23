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


class Server(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

        pass # end of Inventory



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
        jobs = clerk.indexJobs()
        
        listservers( jobs.values(), document, director )
        
        return page  


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Server, self).__init__(name)
        return



def listservers( jobs, document, director ):
    
    p = document.paragraph()

    from PyHtmlTable import PyHtmlTable
    t=PyHtmlTable(2,2, {'width':'400','border':2,'bgcolor':'white'})
    t.setc(0,0,"T1 Cell 00");   t.setc(0,1,"T1 Cell 01")
    t.setc(1,0,"T1 Cell 01");   t.setc(1,1,"T1 Cell 11")
    
    p.text = [t.display()]

    from inventorylist import list
    list( jobs, document, 'scatterer', director )
    return


# version
__id__ = "$Id$"

# End of file 
