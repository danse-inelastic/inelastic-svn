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


class NeutronExperimentWizard(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the experiment"

        ncount = pyre.inventory.float( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        pass # end of Inventory


    def start(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment Wizard - start')
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
            'Please click one of link on the left side to start',
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
            title='Neutron Experiment Wizard - select neutron instrument')
        document.description = ''
        document.byline = 'byline?'

        return page


    def sample_preparation(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard - sample preparation')
        document.description = ''
        document.byline = 'byline?'

        return page


    def sample_environment(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard - sample environment')
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
            title='Neutron Experiment Wizard - specify experiment parameters')
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
            title='Neutron Experiment Wizard - pick computation server')
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
