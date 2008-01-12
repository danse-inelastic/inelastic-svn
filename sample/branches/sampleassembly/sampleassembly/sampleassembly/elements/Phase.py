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


class Phase:

    '''a phase

    attributes:

      type: type of phase (crystal, amorphous, liquid, gas)
      chemical_formula: chemical formula
      crystal: if type is crystal, the crystal instance
    '''

    def __init__( self, type = 'crystal', chemical_formula = None ):
        """create a phase
"""
        self.type = type
        self.chemical_formula = chemical_formula
        return


    def identify( self, visitor):
        return visitor.onPhase( self )

    pass # end of PowderSample



# version
__id__ = "$Id$"

# End of file 
