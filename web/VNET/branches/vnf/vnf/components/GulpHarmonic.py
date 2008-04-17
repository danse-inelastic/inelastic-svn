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


class GulpHarmonic(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'gulpHarmonic' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        
        document = main.document(title='Hamonic dynamics from Gulp' )
        document.byline = '<a href="http://danse.us">DANSE</a>'
        
        formcomponent = self.retrieveFormToShow( 'gulpHarmonic')
        formcomponent.director = director
        
        # build the SKChoice form
        SKChoice = document.form(name='scatteringKernelInput', action=director.cgihome)
        
        # specify action
        action = actionRequireAuthentication(          
            actor = 'gulpHarmonic', 
            sentry = director.sentry,
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
            
        from vnf.weaver import action_formfields
        action_formfields( action, SKChoice )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( SKChoice )
        
        submit = SKChoice.control(name='submit',type="submit", value="next")
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(GulpHarmonic, self).__init__(name)
        return



# version
__id__ = "$Id$"

# End of file 
