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

class LiBH4OrthoParse_TestCase(unittest.TestCase):

    def setUp(self):
        """do LiBH4 full cell"""
        
        self.cifParser=CifParser(os.getcwd()+os.sep+'orthorhombic.cif')
        
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
        sc.writeSupCellXYZFile(os.getcwd()+os.sep+'orthorhombic.xyz')

class LiBH4HexParse_TestCase(unittest.TestCase):

    def setUp(self):
        """do LiBH4 full cell"""
        #self.cifParser=CifParser(home+'/liBH4/hexagonal.cif')
        self.cifParser=CifParser(os.getcwd()+os.sep+'hexagonal.cif')
        
    def testCoords(self):
        coords = self.cifParser.cifToAtomAndCoordinateList()
        #print coords
        #print len(coords)

    def testAllCoords(self):
        coords = self.cifParser.generateAllCoordinates()
        cell = self.cifParser.getUnitCellAsVectors()
        print 'hexagonal'
        pprintCoords(coords)
        print len(coords)
        print cell
        sc = Supercell(coords, cell, 1, 1, 1)
        sc.writeSupCellXYZFile(os.getcwd()+os.sep+'hexagonal.xyz')
        
class Li2B12H12Parse_TestCase(unittest.TestCase):

    def setUp(self):
        """do Li2B12H12 full cell"""
        self.cifParser=CifParser(os.getcwd()+os.sep+'li2b12h12.cif')
        
    def testCoords(self):
        coords = self.cifParser.cifToAtomAndCoordinateList()
        #print coords
        #print len(coords)

    def testAllCoords(self):
        coords = self.cifParser.generateAllCoordinates()
        cell = self.cifParser.getUnitCellAsVectors()
        print 'li2b12h12' 
        pprintCoords(coords)
        print len(coords)
        print cell
        sc = Supercell(coords, cell, 1, 1, 1)
        sc.writeSupCellXYZFile(os.getcwd()+os.sep+'li2b12h12.xyz')
        #sc = Supercell(coords, cell, 2, 2, 2)
        #sc.writeSupCellXYZFile('li2b12h12-2x2x2.xyz')

    
def pysuite():
    suite1 = unittest.makeSuite(LiBH4OrthoParse_TestCase)
    suite2 = unittest.makeSuite(LiBH4HexParse_TestCase)
    suite3 = unittest.makeSuite(Li2B12H12Parse_TestCase)
    return unittest.TestSuite((suite1, suite2, suite3))

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
