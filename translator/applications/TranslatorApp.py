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
        mdPostprocessing = inv.facility('translator', default='Trajectory')
        mdPostprocessing.meta['tip'] = 'translate a file from one format to another'
        mdPostprocessing.meta['known_plugins'] = ['CoherentScatteringFunction','IncoherentScatteringFunction',
                                                  'ElasticIncoherentStructureFactor','MeanSquareDisplacement',
                                                  'DensityOfStates']

    def __init__(self):
        Script.__init__(self, 'ChemSpecApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        # first compute the scattering function using nmoldyn engine
        self.i.mdPostprocessing.compute()

if __name__=='__main__':
    app=ChemSpecApp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
