#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import AuthenticationError, actionRequireAuthentication
from FormActor import FormActor

class SampleInput(FormActor):

    class Inventory(FormActor.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.create_sample_by_hand(director)
        
    def create_sample_by_hand(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleInput' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Sample input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'create_sample_by_hand')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'greeter', 
            sentry = director.sentry,
            routine = 'default',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="submit")
        #self.processFormInputs(director)
        return page  
        
#    def default(self, director):
#        page = director.retrievePage('sampleInput')
#        main = page._body._content._main
#        
#            # populate the main column
#        document = main.document(title='Sample input')
#    
#        # build the sample input form
#        form = document.form(name='form', action=director.cgihome)
#        
#        p = document.paragraph()
##        p.text = ['''Upload xyz file''']
#        
#        name = form.text(id='name', name='name', label='Sample Name')
#        name.help = 'An identifying name for this sample.'
#        
##        atomFile = form.file(id='atomFile', name='atomFile', label='Xyz file containing form')
##        atomFile.help = 'Lattice vectors a,b,c should be on comment line in form a_x a_y a_z b_x b_y b_z c_x c_y c_z'
#            
#        p = document.paragraph()
#        p.text = ['''Download material from <a href="/java/cod.jnlp">Crystallography Open Database</a>''']
#        
#        p = document.paragraph()
#        p.text = ['Input sample shape<br>',
#                  'Height, width, depth<label><input name="textfield" type="text" id="textfield" value="1.0 1.0 1.0" /></label>']
#        
#        submit = form.control(name="submit", type="submit", value="submit")
#        
#        return page 


    def __init__(self, name=None):
        if name is None:
            name = "sampleInput"
        super(SampleInput, self).__init__(name)
        return








# version
__id__ = "$Id$"

# End of file 
