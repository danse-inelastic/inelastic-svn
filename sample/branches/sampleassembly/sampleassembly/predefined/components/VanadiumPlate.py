#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component
import units


class VanadiumPlate(Component):

    """Vanadium plate factory component

    Vanadium plate is a typical calibration sample. Please specify
    the width, height, and the thickness of the vanadium plate.
    """

    class Inventory(Component.Inventory):

        import pyre.inventory 
        
        width = pyre.inventory.dimensional(
            'width', default = units.length.cm * 5)
        width.meta['tip'] = "Width of vanadium plate"
        width.meta['importance'] = 1000
        
        height = pyre.inventory.dimensional(
            'height', default = units.length.cm * 10)
        height.meta['tip'] = "Height of vanadium plate"
        height.meta['importance'] = 1000
        
        thickness = pyre.inventory.dimensional(
            'thickness', default = units.length.cm*1 )
        thickness.meta['tip'] = "thickness of vanadium plate"
        thickness.meta['importance'] = 800
        
        darkAngle = pyre.inventory.str(
            'darkAngle', default = "135*degree" )
        darkAngle.meta['tip'] = "darkAngle of vanadium plate"
        darkAngle.meta['importance'] = 1000

        pass # end of Inventory


    def __init__(self, name = 'VanadiumPlate', facility='SampleFactory'):
        Component.__init__(self, name, facility)
        return


    def product(self): return self._sample


    def _configure(self):
        Component._configure(self)
        
        self.thickness = self.inventory.thickness
        self.width = self.inventory.width
        self.height = self.inventory.height
        from pyre.units import parser, angle
        self.darkAngle = parser().parse( self.inventory.darkAngle )
        try:
            self.darkAngle + angle.degree
        except:
            raise ValueError , "%s is not an angle" % self.inventory.darkAngle
        return


    def _init(self):
        Component._init(self)

        thickness = self.thickness
        width = self.width
        height = self.height
        darkAngle = self.darkAngle

        from sampleassembly.predefined.VanadiumPlate import VanadiumPlate
        
        self._sample = VanadiumPlate(  self.name, width, height, thickness, darkAngle )
        
        return


    pass # end of VanadiumPlate


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jul 10 10:30:20 2007

# End of file 
