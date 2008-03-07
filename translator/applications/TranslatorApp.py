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
from translator.Trajectory import Trajectory


class TranslatorApp(Script):
    '''Driver for file conversion'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        translator = inv.facility('translator', default=Trajectory())
        #translator = inv.facility('translator', default='trajectory')
        translator.meta['tip'] = 'translate a file from one format to another'
        translator.meta['known_plugins'] = ['trajectory']

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
