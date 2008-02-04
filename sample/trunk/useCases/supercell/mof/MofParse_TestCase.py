#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import unittest  
from sample.sampleCreation.supercell.Supercell import Supercell

import unittest

class MofParse_TestCase(unittest.TestCase):
#    def setUp(self):
#        """do MOF full cell"""
#        #first replace the deuterium with a hydrogen molecule: 0.741/6.8354 = 0.108406238
#        # so each H atom is located 0.054203119 above and below the deuterium center
#        self.cifParser=CifParser('MOF74_neutron_4K_a-2H.cif')

    def testDoubling(self):
        sc = Supercell(readFilePath=Nonecoords, cell)#, 1, 1, 1)#, coordType='cartesian')
        sc.i.m=1
        sc.i.n=1
        sc.i.l=2
        sc.create()
        sc.writeSupCellXYZFile('mof74cgDoubled.xyz')
#        sc = Supercell(coords, cell, 1, 1, 2)#, coordType='cartesian')
#        sc.writeSupCellXYZFile('MOF74_neutron_4K_a-1x1x2.xyz')
#        sc = Supercell(coords, cell, 2, 2, 2)#, coordType='cartesian')
#        sc.writeSupCellXYZFile('MOF74_neutron_4K_a-2x2x2.xyz')
        #assert coords==[[0.0, 0.0, 0.0], [0.0, 0.0, 0.5], 
#                        [0.33333000000000002, 0.66666999999999998, 0.0], 
#                        [0.66666999999999998, 0.33333999999999997, 0.5]]
    
def pysuite():
    suite1 = unittest.makeSuite(MofParse_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
#    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    #journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main() 
