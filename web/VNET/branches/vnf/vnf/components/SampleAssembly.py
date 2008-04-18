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


from Actor import action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class SampleAssembly(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the sample assembly"

        editee = pyre.inventory.str('editee', default = 'sampleassembly,#id#')
        editee.meta['tip'] = 'The sub element to edit for edit routine'



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='List of sample assemblies')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        sampleassemblies = clerk.indexSampleAssemblies()
        
        listsampleassemblies( sampleassemblies.values(), document, director )
        
        return page


    def edit(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, err:
            return err.page

        elementtype, elementid = self.inventory.editee.split(',')
        if elementtype == 'sampleassembly': elementid = self.inventory.id
        
        formcomponent = self.retrieveFormToShow( elementtype )
        formcomponent.inventory.id = elementid
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='sampleassembly',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'sampleassembly', sentry = director.sentry,
            label = '', routine = 'set',
            arguments = { 'id': self.inventory.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page    


    def set(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, error:
            return error.page

        self.processFormInputs( director )
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "sampleassembly"
        super(SampleAssembly, self).__init__(name)
        return


    def _head(self, director):
        page = director.retrieveSecurePage( 'sampleassembly' )
        
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

        treeview = create_treeview(
            director.clerk.getHierarchy(sampleassembly),
            director)
        document.contents.append(  treeview )
        return page, document


    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        form_received = self.form_received = self.inventory.form_received
        if form_received.name == 'sampleassembly':
            form_received.inventory.id = self.id
            pass
        return


    pass # end of SampleAssembly



from wording import plural, present_be

def listsampleassemblies( sampleassemblies, document, director ):
    p = document.paragraph()

    n = len(sampleassemblies)

    p.text = [ 'There %s %s sampleassembl%s: ' %
               (present_be(n), n, plural(n, 'y'))
                ]

    from inventorylist import list
    list( sampleassemblies, document, 'sampleassembly', director )
    return



def noscatterer( document, director ):
    p = document.paragraph()

    link = action_link(
        actionRequireAuthentication(
        'scatterer',
        director.sentry,
        label = 'add',
        routine = 'new',
        ),  director.cgihome
        )
    
    p.text = [
        "There is no scatterer in this sample assembly. ",
        'Please %s a scatter.' % (
        director.cgihome, link)
        ]
    return



    

def create_treeview( sampleassembly, director ):
    '''given the db hierarchy of sampleassembly, render a teeview
    '''
    from TreeViewCreator import create
    return create(sampleassembly, 'sampleassembly', director )
            

# version
__id__ = "$Id$"

# End of file 
