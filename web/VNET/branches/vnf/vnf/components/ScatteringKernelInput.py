#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class ScatteringKernelInput(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of a scattering kernel"
        

    def default(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, err:
            return err.page
    
        formcomponent = self.retrieveFormToShow( 'selectkernel')
        formcomponent.director = director
        
        # build the SKChoice form
        SKChoice = document.form(name='scatteringKernelInput', action=director.cgihome)
        
        # specify action
        action = actionRequireAuthentication(          
            actor = 'scatteringKernelInput', 
            sentry = director.sentry,
            routine = 'onselect',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
            
        from vnf.weaver import action_formfields
        action_formfields( action, SKChoice )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( SKChoice )
        
        submit = SKChoice.control(name='submit',type="submit", value="next")
    
        return page 
    
    
    def onselect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )


    def gulpHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'gulpHarmonic' )
        except AuthenticationError, err:
            return err.page
        
        formcomponent = self.retrieveFormToShow( 'selectkernel')
        formcomponent.director = director
        
        # build the SKChoice form
        SKChoice = document.form(name='scatteringKernelInput', action=director.cgihome)
        
        # specify action
        action = actionRequireAuthentication(          
            actor = 'scatteringKernelInput', 
            sentry = director.sentry,
            routine = 'onselect',
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
            name = "scatteringKernelInput"
        super(ScatteringKernelInput, self).__init__(name)
        return
    
    
    def _head(self, director):
        page = director.retrieveSecurePage( 'scatteringKernelInput' )
        
        main = page._body._content._main

        # the record we are working on
        id = None # eventually get the id from idd
        
        document = main.document(title='Energetics / Dynamics Selection' )
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document


# version
__id__ = "$Id$"

# End of file 
