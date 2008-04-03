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


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError


class SampleAssembly(Actor):


    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the sample assembly"


        import vnf.inventory
        dataobject = vnf.inventory.dataobject(
            'dataobject', default='sampleassembly' )
        dataobject.meta['tip'] = 'the data object to be edited'

        pass # end of Inventory



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
        page, document = self._head( director )
        
        scribe = director.scribe

        # the record
        obj = self._getDataObjectRecord( director )

        # properties of the data object
        properties = self.inventory.dataobject.propertyNames( director )
        
        # create form
        sampleassembly = self.sampleassembly_record
        scribe.objectEditForm(
            document, obj, properties,
            sampleassembly, 'sampleassembly',
            director)

        return page    


    def set(self, director):
        page, document = self._head( director )
        
        obj = self._getDataObjectRecord( director )

        dataobject = self.inventory.dataobject

        for prop in dataobject.propertyNames( director ):
            setattr(
                obj, prop,
                dataobject.inventory.getTraitValue( prop ) )
            continue

        director.clerk.updateRecord( obj )
        
        return page    


    def __init__(self, name=None):
        if name is None:
            name = "sampleassembly"
        super(SampleAssembly, self).__init__(name)
        return


    def _head(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page
        
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


    def _getDataObjectRecord(self, director):
        return self.inventory.dataobject.getRecord( director )
    

    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _configure(self):
        Actor._configure(self)
        self.id = self.inventory.id
        dataobject = self.dataobject = self.inventory.dataobject
        if dataobject.name == 'sampleassembly':
            dataobject.inventory.id = self.id
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
