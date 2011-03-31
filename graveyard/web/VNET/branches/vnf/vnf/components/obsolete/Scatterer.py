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


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


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
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page
        
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
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        scatterer = self._getscatterer( id, director )

        # populate the main column
        document = main.document(title='Scatterer: %s' % scatterer.short_description )
        document.description = ''
        document.byline = 'byline?'

        type = scatterer.type
        editors[ type ](
            director.clerk.getRealScatterer( id ),
            document, director )
    
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
    shape_id = scatterer.shape_id
    shape_ctrl = object_description_sentence( shape_id, 'Shape', director )
    p.text = ["Shape: %s" % shape_ctrl,]

    p = document.paragraph()
    crystal_id = scatterer.crystal_id
    crystal_ctrl = object_description_sentence( crystal_id, 'Crystal', director )
    p.text = ["Crystal: %s" % crystal_ctrl,]
    return


def object_description_sentence( objid, type, director):
    """given an object's id, return a sentence describing
    the object.
    
    In case the id is empty, return a sentence saying
    the object is not yet created, please create it.
    
    In case the id is valid, return a sentence describing
    the object, and a link to configure the object.
    """
    if objid == '':
        link = action_link(
            actionRequireAuthentication(
            type.lower(), director.sentry,
            label = 'create', routine = 'new',
            ), director.cgihome)
        obj_ctrl = "%s has not been defined. Please %s a %s" % (
            type, link, type.lower())
    else:
        link = action_link(
            actionRequireAuthentication(
            type.lower(), director.sentry,
            label = 'configure', routine = 'new',
            ), director.cgihome)
        method = 'get%s' % type
        method = getattr( director.clerk, method )
        obj_record = method( objid )
        obj_ctrl = "%s (%s)" % (
            obj_record.short_description, link)
        pass
    return obj_ctrl



editors = {}
editors['PolyXtalScatterer'] = edit_polyxtalscatterer


# version
__id__ = "$Id$"

# End of file 
