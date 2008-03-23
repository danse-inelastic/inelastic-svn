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

        table = pyre.inventory.str(
            'table', default = 'SampleAssembly' )
        table.meta['tip'] = 'The table to be worked on'

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
        properties = _get_properties( obj )
        
        # create form
        sampleassembly = self.sampleassembly_record
        scribe.objectEditForm(
            document, obj, properties,
            sampleassembly, 'sampleassembly',
            director)

        #scatterers = self._getscatterers( id, director )
        #
        #if len(scatterers) == 0:
        #    noscatterer( document, director )
        #else:
        #    listscatterers( scatterers, document, director )
        #    pass
    
        return page    


    def set(self, director):
        page, document = self._head( director )
        
        obj = self._getDataObjectRecord( director )

        dataobject = self.inventory.dataobject

        for prop in _get_properties( obj ):
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
        # the data object component containg info of data object
        # to be edited
        dataobject = self.inventory.dataobject
        # the id in its db table
        objID = dataobject.inventory.id
        # table name
        table = self.inventory.table
        # retrieve record from db
        return director.clerk.getRecordByID( table, objID )


    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _getscatterers(self, id, director):
        clerk = director.clerk
        return clerk.getScatterers( id )


    def _configure(self):
        Actor._configure(self)
        self.id = self.inventory.id
        table = self.table = self.inventory.table
        dataobject = self.dataobject = self.inventory.dataobject
        if table == 'SampleAssembly':
            dataobject.inventory.id = self.id
            pass
        return


    pass # end of SampleAssembly



from wording import plural, present_be

def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There %s %s scatterer%s in this sample assembly: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( scatterers, document, 'scatterer', director )
    return


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
    import vnf.content as factory
    class _:

        def render(self, sampleassembly):
            self._parent = None
            return self.onSampleAssembly( sampleassembly )


        def __call__(self, node):
            klass = node.__class__
            method = getattr(self, 'on%s' % klass.__name__)
            return method(node)

        def onSampleAssembly(self, sampleassembly):
            node = self._node( sampleassembly, factory.treeview )
            for scatterer in sampleassembly.scatterers:
                self._parent = node
                self( scatterer )
                continue
            return node
        
        
        def onScatterer(self, scatterer):
            realscatterer = scatterer.realscatterer
            self(realscatterer)
            return


        def branchNode(self, container):
            return self._node( container, factory.treeview.branch )
        
        
        def leafNode(self, record):
            return self._node( record, factory.treeview.leaf )
        
        
        def onPolyXtalScatterer(self, scatterer):
            parent = self._parent
            node = self.branchNode( scatterer )
            parent.addChild(node)
            
            self._parent = node; self(scatterer.crystal)
            self._parent = node; self(scatterer.shape)
            return
        
        def onCrystal(self, crystal):
            parent = self._parent
            node = self.leafNode( crystal )
            parent.addChild( node )
            return
        
        def onShape(self, shape):
            realshape = shape.realshape
            self(realshape)
            return
        
        
        def onBlock(self, block):
            parent = self._parent
            node = self.leafNode( block )
            parent.addChild( node )
            return
        
        
        def _node(self, record, nodefactory):
            type = record.__class__.__name__
            node = nodefactory(
                '%s (%s)' % (record.short_description, type),
                factory.actionRequireAuthentication(
                'sampleassembly',
                director.sentry,
                routine='edit',
                table = type,
                dataobject = type.lower(),
                id = sampleassembly.id,
                arguments = { '%s.id' % type.lower(): record.id },
                )
                )
            return node
        
        pass # end of _

    return _().render( sampleassembly )



def _get_properties( record ):
    # properties of the data object (columns in the table)
    properties = record.getColumnNames()
    # remove id from list. we don't want users to edit that.
    del properties[ properties.index('id') ]
    # remove any thing ends with 'id'
    properties = filter( lambda a: not a.endswith( 'id' ), properties )
    return properties
            

# version
__id__ = "$Id$"

# End of file 
