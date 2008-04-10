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


class Greeter(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'greet' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Welcome')
        p = document.paragraph()
        p.text = [
            'Welcome to the Virtual Neutron Facility!',
            ]

        # my experiments
        document = main.document(title='Experiments')
        clerk = director.clerk
        username = director.sentry.username
        experiments = clerk.indexNeutronExperiments(
            where = 'creator=%r' % username )
        experiments = experiments.values()
        from NeutronExperiment import listexperiments
        listexperiments( experiments, document, director )

        # misc links
        document = main.document(title='Samples and Equipment')
        p = document.paragraph()
        p.text = [
            action_link(
            actionRequireAuthentication(
            'sampleassembly', director.sentry, 'Sample Assemblies'),
            director.cgihome) + "<br/>",
            
            action_link(
            actionRequireAuthentication(
            'samplePreparation', director.sentry, 'Sample Preparation'),
            director.cgihome) + "<br/>",
            
            action_link(
            actionRequireAuthentication(
            'instrument', director.sentry, 'Instruments'),
            director.cgihome) + "<br/>",
            
            action_link(
            actionRequireAuthentication(
            'sample', director.sentry, 'Samples'),
            director.cgihome) + "<br/>",
            
            '<a href="%s/InstrumentSimulation.html">Instrument Simulation</a><br/>' % director.home,
            
            action_link(
            actionRequireAuthentication(
            'job', director.sentry, 'Job Monitoring'),
            director.cgihome) + "<br/>",
            
            action_link(
            actionRequireAuthentication(
            'server', director.sentry, 'Manage Servers'),
            director.cgihome) + "<br/>",

            '<a href="MaterialSimulation.html">Supporting Calculations</a><br/>',
            ]

        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(Greeter, self).__init__(name)
        return


    pass # end of Greeter


# version
__id__ = "$Id$"

# End of file 
