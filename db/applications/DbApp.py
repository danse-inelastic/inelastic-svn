#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.applications.Script import Script
from interactions.TwoAtomInteraction import TwoAtomInteraction

class DbApp(Script):
    '''Driver for the db retrieval classes in DANSE.'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        twoAtomInteraction = inv.facility('Two Atom Interaction Db', default=TwoAtomInteraction())
        twoAtomInteraction.meta['tip'] = 'db of twoAtomsInteracting'
        dbRetrieval = inv.facility('Two Atom Interaction Db', default=TwoAtomInteraction())
        dbRetrieval.meta['tip'] = 'db of twoAtomsInteracting'
#        mdEngine.meta['known_plugins'] = ['gulp','mmtk']

    def __init__(self):
        Script.__init__(self, 'DbApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        self.i.mdEngine.execute()


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
