#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.components.Component import Component


class Sample(Component):
    '''This is a container class which holds atoms, external conditions, 
unit cells, or anything else pertaining to the sample.  Such items should
be placed in the inventory.'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        atomicStructure = inv.facility('atomicStructure', default='unitCellBuilder')
        atomicStructure.meta['known_plugins'] = ['unitCellBuilder','xyzFile']
        atomicStructure.meta['tip'] = 'Input the atomic structure (simulation cell, coordinates, etc.)'
#        partialCharges = inv.str('Partial Charges', default=None)
#        partialCharges.meta['tip'] = '''a dictionary of atomic species and their 
#partial charges, i.e. {'H':-1.0, 'O':-2.0}'''
#        initialTemp = inv.str('Initial Temperature (K)', default=None)
#        initialTemp.meta['tip'] = 'the initial temperature of the system'
        temperature = inv.str('Temperature or Initial Energy (K)', default=None)
        temperature.meta['tip'] = 'the target temperature of the system'
        pressure = inv.str('Pressure (GPa)', default=None)
        pressure.meta['tip'] = 'the target pressure of the system'

    def __init__(self):
        Component.__init__(self, 'Sample', facility='facility')
        self.i = self.inventory
        
    def _defaults(self):
        Component._defaults(self)

    def _configure(self):
        Component._configure(self)

    def _init(self):
        Component._init(self)
    
    