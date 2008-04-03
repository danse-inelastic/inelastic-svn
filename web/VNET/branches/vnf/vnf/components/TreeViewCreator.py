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



def create( instrument, actor, director ):
    '''given the db hierarchy of instrument, render a teeview
    '''
    return TreeViewCreator( director, actor ).render( instrument )


import vnf.content as factory
class TreeViewCreator:


    def __init__(self, director, actor):
        self.director = director
        self.actor = actor
        return
    

    def render(self, rootnode):
        self._parent = None
        self._rootnode = rootnode
        return self(rootnode)


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onInstrument(self, instrument):
        node = self._node( instrument, factory.treeview )
        for component in instrument.components:
            self._parent = node
            self( component )
            continue
        return node


    def onComponent(self, component):
        realcomponent = component.realcomponent
        self(realcomponent)
        return


    def onMonochromaticSource(self, source):
        parent = self._parent
        node = self.leafNode( source )
        parent.addChild( node )
        return

    
    def onIQEMonitor(self, iqem):
        parent = self._parent
        node = self.leafNode( iqem )
        parent.addChild( node )
        return

    
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
    
        
    def branchNode(self, container):
        return self._node( container, factory.treeview.branch )
    
    
    def leafNode(self, record):
        return self._node( record, factory.treeview.leaf )
    
    
    def _node(self, record, nodefactory):
        director = self.director
        actor = self.actor
        
        type = record.__class__.__name__
        
        node = nodefactory(
            '%s (%s)' % (record.short_description, type),
            factory.actionRequireAuthentication(
            actor,
            director.sentry,
            routine='edit',
            dataobject = type.lower(),
            id = self._rootnode.id,
            arguments = { '%s.id' % type.lower(): record.id },
            )
            )
        return node
        
    pass # end of TreeViewCreator




# version
__id__ = "$Id$"

# End of file 
