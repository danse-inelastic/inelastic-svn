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


class NeutronExperiment(Actor):


    class Inventory(Actor.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the experiment"

        ncount = pyre.inventory.float( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        pass # end of Inventory


    def default(self, director):
        return self.listall( director )


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
        page, document = self._head( director )

        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        
        instrument_id = experiment.instrument_id
        instrument = director.clerk.getInstrument( instrument_id )
        
        p = document.paragraph()
        p.text = [
            'Instrument: %s' % instrument.short_description,
            ]

        sampleassembly_id = experiment.sampleassembly_id
        sampleassembly = director.clerk.getSampleAssembly( sampleassembly_id )
        
        p = document.paragraph()
        p.text = [
            'Sample assembly: %s' % sampleassembly.short_description,
            ]

        actor = self.name
        form = document.form(
            name=actor,
            legend='Experiment parameters',
            action=director.cgihome)

        actor_field = form.hidden(name='actor', value=actor)
        routine_field = form.hidden(name='routine', value='run')
        id_field = form.hidden(
            name = '%s.id' % actor, value = experiment.id)
        
        username_filed = form.hidden(
            name='sentry.username', value = director.sentry.username)
        ticket_filed = form.hidden(
            name='sentry.ticket', value = director.sentry.ticket)

        properties = self.parameters()
        table = experiment.__class__
        
        for property in properties:
            
            value = getattr( experiment, property )
            field = form.text(
                id = property,
                name='%s.%s' % (actor, property),
                label=property,
                value = value)
            
            descriptor = getattr(table, property)
            tip = descriptor.meta.get('tip')
            if tip: field.help = tip

            continue
            
        submit = form.control(name="submit", type="submit", value="Run")
            
        p = form.paragraph()
        p.text = [
            ]        

        return page    


    def run(self, director):
        page, document = self._head( director )
        
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        parameters = self.parameters()
        for parameter in parameters:
            setattr(
                experiment, parameter,
                self.inventory.getTraitValue( parameter ) )
            continue
        
        director.clerk.updateRecord( experiment )

        experiment = director.clerk.getHierarchy( experiment )

        appscript = build_run( experiment )

        apppath = 'InstrSim.py'
        open( apppath, 'w' ).write( '\n'.join( appscript ) )
        
        return page


    def parameters(self):
        return ['ncount']


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperiment"
        super(NeutronExperiment, self).__init__(name)
        return


    def _head(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, error:
            return error.page
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        self.experiment_record = experiment = \
                                 director.clerk.getNeutronExperiment( id )

        # populate the main column
        document = main.document(title='Neutron Experiment: %s' % experiment.short_description )
        document.description = ( '')
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document


    def _configure(self):
        Actor._configure(self)
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


def instrument_selector( document, instruments ):
    label = "Instrument selector: "
    entries = [ (instrument.id, instrument.short_description)
                for instrument in instruments]
    name = 'instrument'
    from opal.content import selector
    widget = selector( name=name, entries=entries, label=label )
    document.contents.append( widget )
    return



def build_run( experiment ):
    from NeutronExperimentSimulationRunBuilder import Builder
    return Builder().render(experiment)


# version
__id__ = "$Id$"

# End of file 
