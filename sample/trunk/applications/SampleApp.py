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
from molDynamics.GeneralSettings import GeneralSettings
#from sample.sampleCreation.cluster.Cluster import Cluster
#from sample.sampleCreation.cluster.Supercell import Supercell

class SampleApp(Script):
    '''Driver for the md engines in DANSE.'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        sampleCreation = inv.facility('sampleCreation', default='supercell')#Cluster())#'supercell')
        sampleCreation.meta['known_plugins'] = ['supercell','cluster']
        #mdEngine = inv.facility('Molecular Dynamics Engine', default=Gulp())
        #mdEngine = inv.facility('Molecular Dynamics Engine', default=Mmtk())
        sampleCreation.meta['tip'] = 'form a supercell or a cluster'
        generalSettings = inv.facility('General Settings', default = GeneralSettings())
        generalSettings.meta['tip'] = 'working directory, engine executable path, etc.'

    def __init__(self):
        Script.__init__(self, 'SampleApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        self.i.sampleCreation.create()

if __name__=='__main__':
    app=SampleApp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
