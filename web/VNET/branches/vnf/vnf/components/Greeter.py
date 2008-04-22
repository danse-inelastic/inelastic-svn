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
