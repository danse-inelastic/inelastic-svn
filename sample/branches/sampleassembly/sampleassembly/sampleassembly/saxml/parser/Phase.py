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

from pyre.xml.Node import Node


class Phase(Node):

    tag = 'Phase'

    def __init__(self, document, attributes):
        Node.__init__(self, document)

        # convert to dictionary
        attrs = {}
        for k,v in attributes.items(): attrs[str(k)] = v

        type = attrs['type']
        from sampleassembly.elements import phase
        self.element = phase( type )
        return


    def notify(self, parent):
        return self.element.identify( parent )


    def onChemicalFormula(self, formula ):
        self.element.chemical_formula = formula
        return


    def onXYZfile(self, xyzfile):
        from sampleassembly.crystal.ioutils import xyzfile2crystal
        self.element.crystal = xyzfile2crystal( xyzfile )
        return


    pass # end of Phase



# version
__id__ = "$Id$"

# End of file 
