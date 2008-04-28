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


from Actor import actionRequireAuthentication, action_link, AuthenticationError
from FormActor import FormActor as base, InputProcessingError


class NeutronExperimentWizard(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default='')
        id.meta['tip'] = "the unique identifier of the experiment"

        ncount = pyre.inventory.float( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        pass # end of Inventory


    def start(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        if self.inventory.id == '':
            #create a new experiment
            from vnf.dom.NeutronExperiment import NeutronExperiment
            experiment = director.clerk.new_ownedobject( NeutronExperiment )
            #need to reload the page so that id is correctly
            self.inventory.id = experiment.id
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
            pass
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment Wizard: start')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        p.text = [
            'To run a virtual neutron experiment, you will need to select',
            'a neutron instrument, prepare your sample, put your',
            'sample in a sample holder, select instrument parameters',
            'for this experiment, and finally pick a computation server',
            'to run your virtual neutron experiment.',
            ]

        p = document.paragraph()
        p.text = [
            'Please click one of link on the left side to start.',
            ]

        return page


    def select_instrument(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: select neutron instrument')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow( 'selectneutroninstrument' )
        formcomponent.inventory.experiment_id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectneutroninstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'configure_instrument',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="OK")
            
        return page


    def configure_instrument(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        self.processFormInputs( director )

        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )
        instrument_id = experiment.instrument_id

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: instrument configuration')
        document.description = ''
        document.byline = 'byline?'

        instrument = director.clerk.getInstrument( instrument_id )
        formname = 'configure_%s_instrument' % (
            instrument.short_description
            .lower().replace(' ','_').replace( '-', '_' ), )

        #raise RuntimeError, formname
        formcomponent = self.retrieveFormToShow(formname)
        if formcomponent is None:
            formcomponent = self.retrieveFormToShow('configureneutroninstrument')
            pass # end if

        formcomponent.inventory.instrument_id = instrument.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='configureinstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'sample_preparation',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )
        
        # run button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page
    
    
    def sample_preparation(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample preparation')
        document.description = ''
        document.byline = 'byline?'
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            return self.configure_instrument( director, errors = errors )
        
        return page


    def sample_environment(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample environment')
        document.description = ''
        document.byline = 'byline?'

        return page


    def experiment_parameters(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: specify experiment parameters')
        document.description = ''
        document.byline = 'byline?'

        return page


    def pick_computation_server(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: pick computation server')
        document.description = ''
        document.byline = 'byline?'

        return page


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperimentwizard"
        super(NeutronExperimentWizard, self).__init__(name)
        return


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        return


    pass # end of NeutronExperimentWizard



from misc import new_id


# version
__id__ = "$Id$"

# End of file 
