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


from Phase import Phase
class Crystal(Phase):

    def __init__(self, chemical_formula = None, unitcell = None):
        Phase.__init__(
            self, type = 'crystal',
            chemical_formula = chemical_formula)
        
        self.unitcell = unitcell
        return


    def identify(self, visitor): return visitor.onCrystal(self)

    pass # end of Crystal


# version
__id__ = "$Id$"

# End of file 
