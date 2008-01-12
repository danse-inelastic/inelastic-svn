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


#this should be a simple subclass of SampleAssembly. For now let us only focus
#on providing a reasonable interface.


import units
mm = units.length.mm
cm = units.length.cm
degree = units.angle.degree


class VanadiumPlate:


    def __init__(self, name = 'vanadiumPlate', 
                 width = None, height = None, thickness = None, 
                 darkAngle = None):
        '''create a vanadium plate sample
        
        all inputs must have units attached
        '''
        self.name = name
        if width is None: width = 6*cm
        if height is None: height = 10*cm
        if thickness is None: thickness = 2*mm
        if darkAngle is None: darkAngle = 135 * degree
        
        self.width = width
        self.height = height
        self.thickness = thickness
        self.darkAngle = darkAngle
        return


    def dimensions(self): return self.width, self.height, self.thickness


    def setDarkAngle(self, darkAngle):
        #this is a temporary implementation.
        #later this class should be a subclass of SampleAssembly
        #and this method should be reimplemented
        self.darkAngle = darkAngle
        return
    


# version
__id__ = "$Id$"

# End of file 
