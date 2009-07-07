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
from translator.pycifrw.CifParser import CifParser
from sample.sampleCreation.supercell.Supercell import Supercell

import unittest
import os

def pprintCoords(coords):
    for c in coords:
        print c[0], c[1], c[2], c[3]

class NaAlH4_TestCase(unittest.TestCase):

    def setUp(self):
        """do NaAlH4 full cell"""
        
        self.cifParser=CifParser(os.getcwd()+os.sep+'naalh4.cif')
        
    def testCoords(self):
        coords = self.cifParser.cifToAtomAndCoordinateList()
        print "cif coords:"
        pprintCoords(coords)

    def testAllCoords(self):
        coords=self.cifParser.generateAllCoordinates()
        cell=self.cifParser.getUnitCellAsVectors()
        #this is risky because of round off error problems
        print "all coords:"
        pprintCoords(coords)
        print len(coords)
        print cell
        sc = Supercell(coords, cell, 1, 1, 1)#, coordType='cartesian')
        sc.writeSupCellXYZFile(os.getcwd()+os.sep+'naalh4.xyz')

    
def pysuite():
    suite1 = unittest.makeSuite(NaAlH4_TestCase)
    return unittest.TestSuite((suite1))

def main():
#    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    #journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite((pytests,))
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return     


if __name__ == '__main__': main() 
