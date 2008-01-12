#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractNode import AbstractNode, debug


class PowderSample(AbstractNode):


    tag = "PowderSample"

    from sampleassembly.elements.PowderSample import PowderSample as ElementFactory

    def onCrystal(self, crystalphase):
        assert crystalphase.type == 'crystal'
        self.element.phase = crystalphase
        return

    pass # end of PowderSample


# version
__id__ = "$Id$"

# End of file 
