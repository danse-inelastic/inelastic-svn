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


class Builder:

    def render(self, instrument):
        self.appscript = []
        self.indent_level = 0
        self.dispatch( instrument )
        return self.appscript


    def dispatch(self, something):
        func = 'on%s' % something.__class__.__name__
        f = getattr( self, func )
        return f( something )


    def onInstrument(self, instrument):
        self._write( 'import mccomponents.pyre_support' )
        self._write( 'from mcni.pyre_support.Instrument import Instrument as base' )
        self._write( 'class Instrument(base):' )

        self._indent()
        self._write(
            'class Inventory(base.Inventory):'
            )

        self._indent()
        self._write( 'import pyre.inventory' )
        self._write( 'from mcni.pyre_support import facility, componentfactory as component')
        
        for component in instrument.components:
            self.dispatch( component )
            continue

        self._outdent()
        
        self._outdent()
        return


    def onMonochromaticSource(self, source):
        kwds = {
            'name': 'source',
            'category': 'sources',
            'type': 'MonochromaticSource',
            'supplier': 'mcni',
            }
        self.onNeutronComponent( **kwds )
        return


    def onSampleAssembly(self, sa):
        kwds = {
            'name': 'sample',
            'category': 'samples',
            'type': 'SampleAssemblyFromXML',
            'supplier': 'mcni',
            }
        self.onNeutronComponent( **kwds )
        return


    def onIQEMonitor(self, m):
        kwds = {
            'name': 'monitor',
            'category': 'monitors',
            'type': 'IQEMonitor',
            'supplier': 'mcstas',
            }
        self.onNeutronComponent( **kwds )
        return


    def onComponent(self, component):
        realcomponent = component.realcomponent
        return self.dispatch( realcomponent )
    

    def onNeutronComponent(self, **kwds):
        '''
        kwds: name, category, type, supplier
        '''
        self._write( 
            '%(name)s = facility(%(name)r, default = component(%(category)r, %(type)r, supplier = %(supplier)r )(%(name)r ) )' % kwds )
        return
                                    
            
    def _indent(self): self.indent_level += 1
    def _outdent(self): self.indent_level -= 1

    def _write(self, s):
        self.appscript.append( '%s%s' % (self.indent_level * '  ', s) )
        return


    pass # end of Builder


# version
__id__ = "$Id$"

# End of file 
