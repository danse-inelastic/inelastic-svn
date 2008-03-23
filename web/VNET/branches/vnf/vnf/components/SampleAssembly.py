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
        id.meta['tip'] = "the unique identifier for a given search"
        
        objtype = pyre.inventory.str('objtype', default='SampleAssembly')
        objtype.meta['tip'] = 'the object type'

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
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        sampleassembly = self._getsampleassembly( id, director )

        treeview = create_treeview(
            director.clerk.getHierarchy(sampleassembly) )
        main.contents.append(  treeview )
        
        # populate the main column
        document = main.document(title='Sample Assembly: %s' % sampleassembly.short_description )
        document.description = (
            'Sample assembly is a collection of neutron scatterers. For example, '\
            'it can consist of a main sample, a sample container, and a furnace.\n'\
            )
        document.byline = 'byline?'

        scatterers = self._getscatterers( id, director )

        if len(scatterers) == 0:
            noscatterer( document, director )
        else:
            listscatterers( scatterers, document, director )
            pass
    
        return page    


    def __init__(self, name=None):
        if name is None:
            name = "sampleassembly"
        super(SampleAssembly, self).__init__(name)
        return


    def _getsampleassembly(self, id, director):
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _getscatterers(self, id, director):
        clerk = director.clerk
        return clerk.getScatterers( id )


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



    

def create_treeview( sampleassembly ):
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
            node = nodefactory(
                record.short_description,
                factory.action(
                'sampleassembly',
                routine='edit',
                objtype=record.__class__.__name__,
                id=record.id)
                )
            return node
        
        pass # end of _

    return _().render( sampleassembly )
    
            

# version
__id__ = "$Id$"

# End of file 
