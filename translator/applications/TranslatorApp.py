#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.applications.Script import Script


class TranslatorApp(Script):
    '''Driver for chemical spectroscopy calculations'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        #mdPostprocessing = inv.facility('Postprocessing Type', default=CoherentScatteringFunction())
        translator = inv.facility('translator', default='Trajectory')
        translator.meta['tip'] = 'translate a file from one format to another'
        translator.meta['known_plugins'] = ['Trajectory']

    def __init__(self):
        Script.__init__(self, 'TranslatorApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        # first compute the scattering function using nmoldyn engine
        self.i.translator.translate()

if __name__=='__main__':
    app=TranslatorApp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
