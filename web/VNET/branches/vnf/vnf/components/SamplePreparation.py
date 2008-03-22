#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication


class SamplePreparation(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        page = director.retrievePage('samplePreparation')
        main = page._body._content._main
        return page 


    def __init__(self, name=None):
        if name is None:
            name = "samplePreparation"
        super(SamplePreparation, self).__init__(name)
        return


    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _getscatterers(self, id, director):
        clerk = director.clerk
        return clerk.getScatterers( id )







# version
__id__ = "$Id$"

# End of file 
