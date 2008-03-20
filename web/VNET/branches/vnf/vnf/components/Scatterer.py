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


from Actor import Actor


class Scatterer(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        pass # end of Inventory



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        page = director.retrieveSecurePage( 'scatterer' )
        if not page:
            return director.retrievePage("authentication-error")
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of scatterers')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatterers = clerk.indexScatterers()
        
        listscatterers( scatterers.values(), document, director )
        
        return page


    def edit(self, director):
        page = director.retrieveSecurePage( 'scatterer' )
        if not page:
            return director.retrievePage("authentication-error")
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        scatterer = self._getscatterer( id, director )

        # populate the main column
        document = main.document(title='Scatterer: %s' % scatterer.short_description )
        document.description = ''
        document.byline = 'byline?'

        type = scatterer.type
        editors[ type ]( scatterer, document, director )
    
        return page    


    def __init__(self, name=None):
        if name is None:
            name = "scatterer"
        super(Scatterer, self).__init__(name)
        return


    def _getscatterer(self, id, director):
        clerk = director.clerk
        return clerk.getScatterer( id )


    pass # end of Scatterer


from wording import plural, present_be

def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There %s %s scatterer%s: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( scatterers, document, 'scatterer', director )
    
    return



def noscatterer( document, director ):
    p = document.paragraph()

    link = action_link(
        actionRequireAuthentication(
        'scatterer', director.sentry,
        label = 'add', routine = 'new',
        ),  director.cgihome
        )
    
    p.text = [
        "There is no scatterer. ",
        'Please %s a scatter.' % (
        director.cgihome, link)
        ]
    return



def edit_polyxtalscatterer( scatterer, document, director ):
    p = document.paragraph()

    p.text = [
        scatterer.short_description,
        ]
    return


editors = {}
editors['PolyXtalScatterer'] = edit_polyxtalscatterer


# version
__id__ = "$Id$"

# End of file 
