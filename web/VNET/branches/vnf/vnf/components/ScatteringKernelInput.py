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

class ScatteringKernelInput(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of a scattering kernel"

    def default(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, err:
            return err.page

        elementtype, elementid = self.inventory.editee.split(',')
        if elementtype == 'sampleassembly': elementid = self.inventory.id
        
        formcomponent = self.retrieveFormToShow( elementtype )
        formcomponent.inventory.id = elementid
        formcomponent.director = director
    
        # build the SKChoice form
        SKChoice = document.form(name='SKChoice', legend='Energetics / Dynamics', action=director.cgihome)
        
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleassembly', sentry = director.sentry,
            label = '', 
            arguments = { 'id': self.inventory.id, 'form-received': formcomponent.name } )
            
        from vnf.weaver import action_formfields
        action_formfields( action, SKChoice )
        
        gulpHarmonic = SKChoice.radio(id='radio1', name='gulpHarmonic', label='Gulp Harmonic Motion')
        #gulpHarmonic.help = 'Gulp Harmonic Motion'
        gulpNE = SKChoice.radio(id='radio2', name='gulpNE', label="Gulp Newton's Equations")
        mmtkNE = SKChoice.radio(id='radio3', name='mmtkNE', label="Mmtk Newton's Equations")
    
        vaspPhon = SKChoice.radio(id='radio4', name='vaspPhon', label='Vasp Energies, Phon Harmonic Motion')
        abinitPhon = SKChoice.radio(id='radio5', name='abinitPhon', label="AbInit Energies, Phon Harmonic Motion")
        
        
        submit = SKChoice.control(name='next',type="submit", value="next")
    

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
        id = self.inventory.id
        self.sampleassembly_record = sampleassembly = self._getsampleassembly( id, director )

        # populate the main column
  

        
        document = main.document(title='Sample Assembly: %s' % sampleassembly.short_description )
        document.description = (
            'Sample assembly is a collection of neutron scatterers. For example, '\
            'it can consist of a main sample, a sample container, and a furnace.\n'\
            )
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document








# version
__id__ = "$Id$"

# End of file 
