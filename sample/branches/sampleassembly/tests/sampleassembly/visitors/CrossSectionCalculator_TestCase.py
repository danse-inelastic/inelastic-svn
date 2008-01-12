#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from numpy import array
from pyre.units.length import m


import unittest


from unittestX import TestCase
class CrossSectionCalculator_TestCase(TestCase):


    def test0(self):
        """
        sampleassembly.visitors.CrossSectionCalculator
        """
        from sampleassembly.elements.phases import crystal
        from sampleassembly.elements import unitcell, atom
        Ni = atom('Ni')
        atoms = [Ni]
        cellvectors = [
            [1,0,0],
            [0,1,0],
            [0,0,1],
            ]
        
        positions = [ [0,0,0] ]

        uc = unitcell( cellvectors, atoms, positions )

        xtal = crystal( unitcell = uc )

        from sampleassembly.visitors.CrossSectionCalculator import CrossSectionCalculator
        calculator = CrossSectionCalculator()

        abs, inc, coh = calculator( xtal )

        import sampleassembly.units as units
        barn = units.area.barn
        angstrom = units.length.angstrom
        self.assertAlmostEqual( abs/barn * angstrom**3, 4.49 )
        print abs, inc, coh
        return

    pass # end of CrossSectionCalculator_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(CrossSectionCalculator_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    from instrument.elements import debug
    debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: CrossSectionCalculator_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
