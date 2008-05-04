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
            'In this virtual neutron facility, you can set up',
            'a new experiment by using %s.' % wizard_link,
            'Or you can select from one of the %s you have run' % list_link,
            'and rerun it with new settings.',
            ]
            
        return page


    def delete(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, error:
            return error.page

        record = director.clerk.getNeutronExperiment( self.inventory.id )
        director.clerk.deleteRecord( record )
        return self.listall(director)
        

    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Experiments')
        document.description = ''
        document.byline = 'byline?'

        #
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'this wizard',
            actor = 'neutronexperimentwizard',
            routine = 'start',
            sentry = director.sentry,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You can perform various kinds of neutron experiments in',
            'this virtual neutron facility.',
            'To start, you can plan a new experiment by following %s.' % link,
            ]

        # retrieve id:record dictionary from db
        clerk = director.clerk
        experiments = clerk.indexNeutronExperiments()
        # make a list of all experiments
        listexperiments( experiments.values(), document, director )
        return page


    def view(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page

        # the record we are working on
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        #see if the experiment is constructed or not. if not
        #ask the wizard to do the editing.
        if experiment.status not in ['constructed', 'running', 'finished']:
            director.routine = 'submit_experiment'
            actor = director.retrieveActor( 'neutronexperimentwizard')
            director.configureComponent( actor )
            actor.inventory.id = self.inventory.id
            return actor.submit_experiment( director )

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Experiment %r' % experiment.short_description )
        document.description = ( '')
        document.byline = 'byline?'

        status = experiment.status
        method = '_view_%s' % status
        method = getattr(self, method)
        method( experiment, document, director )
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


    def _view_constructed(self, experiment, document, director):
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'start running',
            actor = 'neutronexperimentwizard',
            routine = 'submit_experiment',
            sentry = director.sentry,
            id = self.inventory.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'Experiment %r has been constructed.' % experiment.short_description,
            'You can get it %s.' % link,
            ]

        p = document.paragraph()
        p.text = [
            'Details of configuration of this experiment can be',
            'found out in the following tree view.',
            ]
        experiment = director.clerk.getHierarchy( experiment )
        from TreeViewCreator import create
        view = create( experiment )
        document.contents.append( view )
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

    p.text = [ 'Here is a list of experiments you have planned or run:' ]


    formatstr = '%(index)s: %(viewlink)s (%(status)s) is a measurement of %(sample)r in %(instrument)r (%(deletelink)s)'
    actor = 'neutronexperiment'
    container = experiments

    for i, element in enumerate( container ):
        
        p = document.paragraph()
        name = element.short_description
        if name in ['', None, 'None'] : name = 'undefined'
        action = actionRequireAuthentication(
            actor, director.sentry,
            routine = 'view',
            label = name,
            id = element.id,
            )
        viewlink = action_link( action,  director.cgihome )

        action = actionRequireAuthentication(
            actor, director.sentry,
            routine = 'delete',
            label = 'delete',
            id = element.id,
            )
        deletelink = action_link( action,  director.cgihome )

        element = director.clerk.getHierarchy( element )
        if element.instrument is None \
               or element.instrument.instrument is None:
            action = actionRequireAuthentication(
                'neutronexperimentwizard', sentry = director.sentry,
                label = 'select instrument',
                routine = 'select_instrument',
                id = element.id,
                )
            link = action_link( action, director.cgihome )
            instrument = link
        else:
            instrument = element.instrument.instrument
            instrument = instrument.short_description
            pass # end if
        
        subs = {'index': i+1,
                'viewlink': viewlink,
                'deletelink': deletelink,
                'status': element.status,
                'instrument': instrument,
                'sample': 'sample',
                }

        p.text += [
            formatstr % subs,
            ]
        continue
    return


def view_instrument(instrument, form):
    p = form.paragraph()
    p.text = [
        'This experiment is to be performed in instrument %s' % instrument.short_description,
        ]
    
    from TreeViewCreator import create
    view = create( instrument )
    form.contents.append( view )
    return


def view_sampleassembly(sampleassembly, form):
    p = form.paragraph()
    p.text = [
        'The sample to study: %s' % sampleassembly.short_description,
        ]

    from TreeViewCreator import create
    view = create( sampleassembly )
    form.contents.append( view )
    return


def view_instrument_plain(instrument, form):
    p = form.paragraph()
    p.text = [
        'This experiment is to be performed in instrument %s' % instrument.short_description,
        ]
    
    p = form.paragraph()
    geometer = instrument.geometer
    components = instrument.componentsequence
    p.text = [
        'Instrument %r has %s components: %s' % (
        instrument.short_description, len(components),
        ', '.join( [ comp for comp in components ] ) ),
        ]
    
    excluded_cols = [
        'id', 'creator', 'date', 'short_description',
        ]
    p = form.paragraph()
    p.text = [ '<UL>' ]
    for component in components:
        if component != 'sample': 
            component_record = getattr( instrument, component ).realcomponent
            component_type = component_record.__class__.__name__
        else:
            component_type = ''
            pass # endif
        p.text.append( '<li>%s: %s' % (component, component_type) )
        p.text.append( '<UL>' )
        record = geometer[ component ]
        p.text.append( '<li>Position: %s' % (record.position,) )
        p.text.append( '<li>Orientation: %s' % (record.orientation,) )
        
        if component == 'sample':
            p.text.append( '</UL>' )
            continue
        
        columns = component_record.getColumnNames()
        for col in columns:
            if col in excluded_cols: continue
            value = getattr( component_record, col )
            p.text.append('<li>%s: %s' % (col, value) )
            continue
        
        p.text.append( '</UL>' )
        continue
    p.text.append( '</UL>' )
    return


from misc import empty_id

# version
__id__ = "$Id$"

# End of file 
