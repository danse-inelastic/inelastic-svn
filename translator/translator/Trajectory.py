#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                              Brandon Keith
#                      California Institute of Technology
#              (C) 2007 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.components.Component import Component
from pyregui.inventory.extensions.OutputDir import OutputDir
from pyregui.inventory.extensions.InputFile import InputFile

class Trajectory(Component):
    '''given input parameters and coordinates of a trajectory, returns the coherent
    scattering function'''
    
    class Inventory(Component.Inventory):   
        import pyre.inventory as inv 
        speciesNumbers = inv.str( "List of (specie, specie count)", default = "")
        speciesNumbers.meta['tip'] = "list of tuples such as ('H',40)"
        speciesNumbers.meta['importance'] = 10
        historyFile = InputFile( ".his Filename", default = "")
        historyFile.meta['tip'] = "the trajectory file of the MD run (NetCDF format)"
        historyFile.meta['importance'] = 9

    def __init__(self, name = 'trajectory'):
        Component.__init__(self, name, 'translator')
        self.i=self.inventory
        
    def translate(self):
        from hisToNc import hisToNc
        hisToNc(eval(self.i.speciesNumbers), self.i.historyFile, blockSize=1)
        
        
    
    
    

    