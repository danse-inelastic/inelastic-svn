#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   BK
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ccp1gui.Supercell import Supercell
from os import sep,system
import unittest 
import danseGlob
from numpy import *

appName = "PotassiumGraphite3x2x1"
caseName = "fulltest"

import journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

class PotassiumGraphite3x2x1_TestCase(unittest.TestCase):
    
    def setUp(self):
        """
        do potassium graphite 3x2x1 supercell
        """
        self.graphiteKUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.4], 
                 ['C', -1.2279999999864621e-05, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 5.4]]
        self.graphiteKLattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 8.75]]
        
        self.graphiteKHUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.69], 
                 ['C', 0.0, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 5.69]]
        self.graphiteKH2Lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 9.04]]    
    
    def testHexToOrthorhombicSupWithKAndH(self):
        '''convert a hexagonal supercell to orthorhombic and add potassium to make
        C_24 K then make much bigger in preparation for simulation'''
        # first get 3x2x1 supercell of real coordinates from graphite
        supercell=Supercell(self.graphiteKUnitCell,self.graphiteKLattice,3,2,1,coordType='cartesian')
        realCoords=supercell.getSupercellRealCoordinates()
        lattice=supercell.getSupercellLatticeVectors()
        #print lattice
        #print realCoords
        orthorhombicSuperLattice=[[7.368, 0.0, 0.0], [0.0, 4.2539167833891627, 0.0], [0.0, 0.0, 8.75]]
        orthorhombicRealCoords=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.4000000000000004], 
         ['C', 0.0, 1.4179793509910266, 0.0], 
         ['C', 1.228, 0.70900031028747168, 5.4000000000000004], 
         ['C', 6.14, 2.1269583916945813, 0.0], ['C', 6.14, 2.1269583916945813, 5.4], 
         ['C', 6.14, 3.5449377426856081, 0.0], 
         ['C', 0.0, 2.8359587019820531, 5.4000000000000004], ['C', 2.456, 0.0, 0.0], 
         ['C', 2.456, 0.0, 5.4000000000000004], ['C', 2.45598772, 1.4179793509910266, 0.0], 
         ['C', 3.6840000000000002, 0.70900031028747168, 5.4], 
         ['C', 1.228, 2.1269583916945813, 0.0], ['C', 1.228, 2.1269583916945813, 5.4], 
         ['C', 1.22798772, 3.5449377426856081, 0.0], ['C', 2.456, 2.8359587019820531, 5.4], 
         ['C', 4.912, 0.0, 0.0], ['C', 4.912, 0.0, 5.4], 
         ['C', 4.9119877199999999, 1.4179793509910266, 0.0], 
         ['C', 6.1399999999999997, 0.70900031028747168, 5.4000000000000004], 
         ['C', 3.6840000000000002, 2.1269583916945813, 0.0], 
         ['C', 3.6840000000000002, 2.1269583916945813, 5.4000000000000004], 
         ['C', 3.6839877200000002, 3.5449377426856081, 0.0], 
         ['C', 4.9119999999999999, 2.8359587019820531, 5.4000000000000004]]
        # put the potassium in the middle of the first cell halfway between
        # the middle and lower layer
        fracPos=array([0.16666666666666667, 0.25, 0.308571429])
        lat=array(orthorhombicSuperLattice)
        realPos=dot(fracPos,lat).tolist()
        orthorhombicRealCoords.append(['K'] + realPos)
        # put the hydrogens in the second square over, back row, halfway between layers
        fracPos=array([0.45, 0.75, 0.308571429])
        lat=array(orthorhombicSuperLattice)
        realPos=dot(fracPos,lat).tolist()
        orthorhombicRealCoords.append(['H'] + realPos)
        fracPos=array([0.55, 0.75, 0.308571429])
        lat=array(orthorhombicSuperLattice)
        realPos=dot(fracPos,lat).tolist()
        orthorhombicRealCoords.append(['H'] + realPos)
        orthoSupercell=Supercell(orthorhombicRealCoords,orthorhombicSuperLattice,4,6,1,coordType='cartesian')
        supFile=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'orthoGraphKH212x12x1.xyz'
        orthoSupercell.writeSupCellXYZFile(supFile)
        system('vmd '+supFile)
        return  

def pysuite():
    suite1 = unittest.makeSuite(PotassiumGraphite3x2x1_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    #journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': 
    main() 
