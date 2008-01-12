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


import unittest


from unittestX import TestCase
class sampleassembly_TestCase(TestCase):


    def test0(self):
        """
        cross_sections
        """
        from sampleassembly.elements.phases import crystal
        from sampleassembly.elements import unitcell, atom
        Fe = atom('Fe')
        atoms = [Fe]
        cellvectors = [
            [1,0,0],
            [0,1,0],
            [0,0,1],
            ]
        
        positions = [ [0,0,0] ]

        uc = unitcell( cellvectors, atoms, positions )

        xtal = crystal( unitcell = uc )

        from sampleassembly import cross_sections
        abs, inc, coh = cross_sections( xtal )
        print abs, inc, coh
        return

    pass # end of sampleassembly_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(sampleassembly_TestCase)
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
__id__ = "$Id: sampleassembly_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
