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
from FormActor import FormActor as base


class NeutronExperiment(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the experiment"

        ncount = pyre.inventory.float( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'this wizard', routine = 'start',
            )
        wizard_link = action_link( action, director.cgihome )        

        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = 'experiments', routine = 'listall',
            )
        list_link = action_link( action, director.cgihome )        

        p.text = [
            'In this virtual neutron facility, you can setup',
            'a new experiment by using %s.' % wizard_link,
            'Or you can select from one of the %s you have run' % list_link,
            'and rerun it.',
            ]
            
        return page


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='List of experiments')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        experiments = clerk.indexNeutronExperiments()
        
        listexperiments( experiments.values(), document, director )
        
        return page


    def edit(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, error:
            return error.page

        self.processFormInputs( director )

        #see if the experiment is constructed or not. if not
        #ask the wizard to do the editing.
        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        if experiment.status != 'constructed':
            director.routine = 'start'
            actor = director.retrieveActor( 'neutronexperimentwizard')
            director.configureComponent( actor )
            actor.inventory.id = self.inventory.id
            return actor.start( director )

        formcomponent = self.retrieveFormToShow( 'run_neutron_experiment' )
        formcomponent.inventory.id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='neutronexperiment',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'job', sentry = director.sentry,
            label = '', routine = 'edit',
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="Run")
            
        return page


    def selectinstrument(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, error:
            return error.page

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        
        # create form to set scatterer type
        formcomponent = self.retrieveFormToShow( 'selectneutroninstrument' )
        formcomponent.inventory.experiment_id = experiment.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectneutroninstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = '', routine = 'edit',
            arguments = { 'id': experiment.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperiment"
        super(NeutronExperiment, self).__init__(name)
        return


    def _head(self, director):
        page = director.retrieveSecurePage( 'neutronexperiment' )
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        # populate the main column
        document = main.document(
            title='Neutron Experiment: %s' % experiment.short_description )
        document.description = ( '')
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        return


    pass # end of NeutronExperiment



from wording import plural, present_be

def listexperiments( experiments, document, director ):
    p = document.paragraph()

    n = len(experiments)

    p.text = [ 'There %s %s experiment%s: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( experiments, document, 'neutronexperiment', director )
    return



# version
__id__ = "$Id$"

# End of file 
