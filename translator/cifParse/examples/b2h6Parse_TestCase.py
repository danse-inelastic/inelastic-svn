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
from pycifrw.CifParser import CifParser
from sample.sampleCreation.supercell.Supercell import Supercell

appName = "CifParser"
caseName = "fulltest"

import unittest
#debug = journal.debug( "%s-%s" % (appName, caseName) )

#from shutil import copyfile
#copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)

class b2h6Parse_TestCase(unittest.TestCase):

    def setUp(self):
        """do B2H6 full cell"""
        
        self.cifParser = CifParser('b2h6.cif')
        
    def testCoords(self):
        coords = self.cifParser.cifToAtomAndCoordinateList()

    def testAllCoords(self):
        coords=self.cifParser.generateAllCoordinates()
        cell=self.cifParser.getUnitCellAsVectors()
        #this is risky because of round off error problems
        print coords 
        print len(coords)
        print cell
        sc = Supercell(coords, cell, 1, 1, 1)#, coordType='cartesian')
        sc.writeSupCellXYZFile('b2h6.xyz')

    
def pysuite():
    suite1 = unittest.makeSuite(b2h6Parse_TestCase)
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
