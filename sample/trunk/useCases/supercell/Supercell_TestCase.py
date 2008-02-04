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
from os import sep
import unittest 
import danseGlob
from numpy import *
#from unittest import *

appName = "Supercell"
caseName = "fulltest"

import journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

class Supercell_TestCase(unittest.TestCase):
    
    def setUp(self):
        """
        do graphite 2x1x1 supercell from fractional xyz coordinates
        """
        self.lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 6.696]]
        self.fracUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 0.5], 
                        ['C', 0.33333000000000002, 0.66666999999999998, 0.0], 
                        ['C', 0.66666999999999998, 0.33333999999999997, 0.5]]
        self.supercellFromFrac=Supercell(self.fracUnitCell,self.lattice,2,1,1)
        """
        do graphite 2x1x1 supercell from real xyz coordinates
        """
        self.realUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 3.3479999999999999], 
                 ['C', -1.2279999999864621e-05, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 3.3479999999999999]]
        self.supercellFromReal=Supercell(self.realUnitCell, self.lattice,2,1,1,coordType='cartesian')
        """
        do graphite supercell from real xyz coordinates
        """
        self.graphiteKUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.4], 
                 ['C', -1.2279999999864621e-05, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 5.4]]
        self.graphiteKLattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 8.75]]
        
        self.graphiteKH2Lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 9.04]]

    def testFractionalSupercell(self):
        coords=self.supercellFromFrac.getSupercellFractionalCoordinates()
        assert len(coords)==8
        #print self.supercellFromFrac.getSupercellLatticeVectors()
        assert self.supercellFromFrac.getSupercellLatticeVectors()==\
        [[4.9119999999999999, 0.0, 0.0], [-1.228, 2.1269583916945813, 0.0], [0.0, 0.0, 6.6959999999999997]]
        return   
      
    def testRealSupercell(self):
        coords=self.supercellFromFrac.getSupercellFractionalCoordinates()
        assert len(coords)==8
        #print self.supercellFromFrac.getSupercellLatticeVectors()
        assert self.supercellFromFrac.getSupercellLatticeVectors()==\
        [[4.9119999999999999, 0.0, 0.0], [-1.228, 2.1269583916945813, 0.0], [0.0, 0.0, 6.6959999999999997]]
        return  
    
    def testProduceRealSupercell(self):
        coords=self.supercellFromFrac.getSupercellRealCoordinates()
        #print fracUnitCell
        #assert norm(array(fracUnitCell)-array(fracUnitCell))
        return  
    
    def testXYZFile(self):
        #print danseGlob.installDir + sep + 'ccp1gui' +sep + 'tests' + sep        
        self.supercellFromFrac.writeSupCellXYZFile(danseGlob.installDir+sep+'ccp1gui' 
            +sep+'tests'+sep+'graphite.xyz')
        return    
    
    def testHexToOrthorhombicSupercell(self):
        # first get 2x2x1 supercell of real coordinates from graphite
        supercellFromFrac=Supercell(self.fracUnitCell,self.lattice,2,2,1)
        realCoords=supercellFromFrac.getSupercellRealCoordinates()
        lattice=supercellFromFrac.getSupercellLatticeVectors()
        #print lattice
        #lattice=[[4.9119999999999999, 0.0, 0.0], [-2.456, 4.2539167833891627, 0.0], [0.0, 0.0, 6.6959999999999997]]
        #print realCoords
        orthorhombicSuperLattice=[[4.912, 0.0, 0.0], [0.0, 4.2539167833891627, 0.0], [0.0, 0.0, 6.696]]
        orthorhombicRealCoords=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 3.3479999999999999], 
           ['C', 0, 1.4179793509910266, 0.0], 
           ['C', 1.228, 0.70900031028747168, 3.3479999999999999], 
           ['C', 3.684, 2.1269583916945813, 0.0], 
           ['C', 3.684, 2.1269583916945813, 3.3479999999999999], 
           ['C', 3.684, 3.5449377426856077, 0.0], 
           ['C', 0.0, 2.8359587019820531, 3.3479999999999999], 
           ['C', 2.456, 0.0, 0.0], ['C', 2.456, 0.0, 3.3479999999999999], 
           ['C', 2.4559877200000004, 1.4179793509910266, 0.0], 
           ['C', 3.6840000000000002, 0.70900031028747168, 3.3479999999999999], 
           ['C', 1.228, 2.1269583916945813, 0.0], 
           ['C', 1.228, 2.1269583916945813, 3.3479999999999999], 
           ['C', 1.2279877200000002, 3.5449377426856077, 0.0], 
           ['C', 2.4560000000000004, 2.8359587019820531, 3.3479999999999999]]
        orthoSupercell=Supercell(orthorhombicRealCoords,orthorhombicSuperLattice,1,1,1,coordType='cartesian')
        orthoSupercell.writeSupCellXYZFile(danseGlob.installDir+sep+'ccp1gui' 
            +sep+'tests'+sep+'orthoGraphite2x2x1.xyz')
        return    
    
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
        orthoSupercell=Supercell(orthorhombicRealCoords,orthorhombicSuperLattice,1,1,1,coordType='cartesian')
        orthoSupercell.writeSupCellXYZFile(danseGlob.installDir+sep+'ccp1gui' 
            +sep+'tests'+sep+'orthoGraphKH23x2x1.xyz')
        return 
    
    def testC28KToOrthorhombicSupWithKAndH(self):
        '''convert a C28 hexagonal supercell to orthorhombic and add potassium to make
        C_24 K then make much bigger in preparation for simulation'''
        # first get 3x2x1 supercell of real coordinates from graphite
        supercell=Supercell(self.graphiteKUnitCell,self.graphiteKLattice,4,6,1,coordType='cartesian')
        fracCoords=supercell.getSupercellFractionalCoordinates()
        lattice=supercell.getSupercellLatticeVectors()
        #print lattice   0.629424779
        #print fracCoords
        
        # this is for intercalated graphite without hydrogens
        orthorhombicFracGraphK=[['C', 0.0, 0.0, 0.0], ['C', 1.0, 1.0, 0.0], 
                                ['C', 3.3333300000000001, 3.6666700000000003, 0.0], 
         ['C', 0.33333000000000013, 1.6666700000000001, 0.0], 
         ['C', 3.3333300000000001, 5.6666699999999999, 0.0],
         ['C', 3.3333300000000006, 4.6666700000000008, 0.0],
         ['C', 0.33333000000000007, 0.66666999999999998, 0.0],
         ['C', 1.0, 2.0, 0.0], ['C', 2.3333300000000001, 3.6666700000000003, 0.0],
         ['C', 1.0, 3.0000000000000004, 0.0],['C', 1.0, 4.0, 0.0], 
         ['C', 1.3333300000000001, 0.66666999999999998, 0.0], ['C', 2.0, 1.0, 0.0], 
         ['C', 1.3333300000000001, 1.6666700000000001, 0.0], ['C', 2.0, 2.0, 0.0],
         ['C', 1.3333299999999999, 2.6666699999999999, 0.0], ['C', 2.0, 3.0000000000000004, 0.0],
         ['C', 1.3333300000000001, 3.6666700000000003, 0.0], ['C', 2.0, 4.0, 0.0],
         ['C', 1.3333300000000003, 4.6666700000000008, 0.0], ['C', 2.0, 5.0, 0.0],
         ['C', 2.3333300000000001, 1.6666700000000001, 0.0], ['C', 3.0000000000000004, 2.0, 0.0],
         ['C', 2.3333300000000001, 2.6666699999999999, 0.0], ['C', 3.0000000000000004, 3.0, 0.0],
         ['C', 3.0, 4.0, 0.0], ['C', 2.3333300000000006, 4.6666700000000008, 0.0], 
         ['C', 3.0, 5.0, 0.0], ['C', 0.0, 0.0, 0.61714285714285722], 
         ['C', 3.6666699999999999, 5.3333399999999997, 0.61714285714285722],
         ['C', 1.0, 2.0, 0.61714285714285722], 
         ['C', 0.66666999999999998, 1.33334, 0.61714285714285722],
         ['C', 0.6666700000000001, 2.3333400000000002, 0.61714285714285722],
         ['C', 1.0, 3.0000000000000004, 0.61714285714285722], ['C', 1.0, 4.0, 0.61714285714285722], 
         ['C', 0.66666999999999998, 0.33333999999999997, 0.61714285714285722],
         ['C', 2.0, 1.0, 0.61714285714285722], ['C', 1.6666700000000003, 1.33334, 0.61714285714285722],
         ['C', 2.0, 2.0, 0.61714285714285722],
         ['C', 1.6666700000000003, 2.3333400000000002, 0.61714285714285722],
         ['C', 2.0, 3.0000000000000004, 0.61714285714285722],
         ['C', 1.6666700000000001, 3.3333400000000002, 0.61714285714285722],
         ['C', 1.0, 1.0, 0.61714285714285722], ['C', 2.0, 4.0, 0.61714285714285722],
         ['C', 1.6666699999999999, 4.3333399999999997, 0.61714285714285722],
         ['C', 0.66666999999999987, 3.3333400000000002, 0.61714285714285722],
         ['C', 2.0, 5.0, 0.61714285714285722],
         ['C', 3.0000000000000004, 2.0, 0.61714285714285722],
         ['C', 2.6666699999999999, 2.3333400000000002, 0.61714285714285722],
         ['C', 3.0000000000000004, 3.0000000000000004, 0.61714285714285722],
         ['C', 2.6666699999999999, 3.3333400000000002, 0.61714285714285722],
         ['C', 3.0, 4.0, 0.61714285714285722],
         ['C', 2.6666699999999999, 4.3333399999999997, 0.61714285714285722],
         ['C', 3.0000000000000004, 5.0, 0.61714285714285722],
         ['C', 2.6666699999999999, 5.3333399999999997, 0.61714285714285722],
         ['C', 2.6666699999999999, 1.33334, 0.61714285714285722]]
        #print len(orthorhombicFracCoords)

        # add two potassiums at 1/2, 1/3 and 3 1/2, 4 1/3 and halfway between 
        # the middle and lower layer
        #fracPos=[0.16666666666666667, 0.25, 0.308571429])
        #lat=array(orthorhombicSuperLattice)
#        realPos=dot(fracPos,lat).tolist()
        orthorhombicFracGraphK.append(['K', 0.6666666666666667, 0.33333333333333, 0.308571429])
        orthorhombicFracGraphK.append(['K', 2.6666666666666667, 3.33333333333333, 0.308571429])
        
        # this is for intercalated graphite with hydrogens
        orthorhombicFracGraphKH2=[['C', 0.0, 0.0, 0.0], ['C', 1.0, 1.0, 0.0], 
         ['C', 3.3333300000000001, 3.6666700000000003, 0.0], 
         ['C', 0.33333000000000013, 1.6666700000000001, 0.0], 
         ['C', 3.3333300000000001, 5.6666699999999999, 0.0],
         ['C', 3.3333300000000006, 4.6666700000000008, 0.0],
         ['C', 0.33333000000000007, 0.66666999999999998, 0.0],
         ['C', 1.0, 2.0, 0.0], ['C', 2.3333300000000001, 3.6666700000000003, 0.0],
         ['C', 1.0, 3.0000000000000004, 0.0],['C', 1.0, 4.0, 0.0], 
         ['C', 1.3333300000000001, 0.66666999999999998, 0.0], ['C', 2.0, 1.0, 0.0], 
         ['C', 1.3333300000000001, 1.6666700000000001, 0.0], ['C', 2.0, 2.0, 0.0],
         ['C', 1.3333299999999999, 2.6666699999999999, 0.0], ['C', 2.0, 3.0000000000000004, 0.0],
         ['C', 1.3333300000000001, 3.6666700000000003, 0.0], ['C', 2.0, 4.0, 0.0],
         ['C', 1.3333300000000003, 4.6666700000000008, 0.0], ['C', 2.0, 5.0, 0.0],
         ['C', 2.3333300000000001, 1.6666700000000001, 0.0], ['C', 3.0000000000000004, 2.0, 0.0],
         ['C', 2.3333300000000001, 2.6666699999999999, 0.0], ['C', 3.0000000000000004, 3.0, 0.0],
         ['C', 3.0, 4.0, 0.0], ['C', 2.3333300000000006, 4.6666700000000008, 0.0], 
         ['C', 3.0, 5.0, 0.0], ['C', 0.0, 0.0, 0.629424779], 
         ['C', 3.6666699999999999, 5.3333399999999997, 0.629424779],
         ['C', 1.0, 2.0, 0.629424779], 
         ['C', 0.66666999999999998, 1.33334, 0.629424779],
         ['C', 0.6666700000000001, 2.3333400000000002, 0.629424779],
         ['C', 1.0, 3.0000000000000004, 0.629424779], ['C', 1.0, 4.0, 0.629424779], 
         ['C', 0.66666999999999998, 0.33333999999999997, 0.629424779],
         ['C', 2.0, 1.0, 0.629424779], ['C', 1.6666700000000003, 1.33334, 0.629424779],
         ['C', 2.0, 2.0, 0.629424779],
         ['C', 1.6666700000000003, 2.3333400000000002, 0.629424779],
         ['C', 2.0, 3.0000000000000004, 0.629424779],
         ['C', 1.6666700000000001, 3.3333400000000002, 0.629424779],
         ['C', 1.0, 1.0, 0.629424779], ['C', 2.0, 4.0, 0.629424779],
         ['C', 1.6666699999999999, 4.3333399999999997, 0.629424779],
         ['C', 0.66666999999999987, 3.3333400000000002, 0.629424779],
         ['C', 2.0, 5.0, 0.629424779],
         ['C', 3.0000000000000004, 2.0, 0.629424779],
         ['C', 2.6666699999999999, 2.3333400000000002, 0.629424779],
         ['C', 3.0000000000000004, 3.0000000000000004, 0.629424779],
         ['C', 2.6666699999999999, 3.3333400000000002, 0.629424779],
         ['C', 3.0, 4.0, 0.629424779],
         ['C', 2.6666699999999999, 4.3333399999999997, 0.629424779],
         ['C', 3.0000000000000004, 5.0, 0.629424779],
         ['C', 2.6666699999999999, 5.3333399999999997, 0.629424779],
         ['C', 2.6666699999999999, 1.33334, 0.629424779]]
        # add two potassiums at 1/2, 1/3 and 3 1/2, 4 1/3 and halfway between 
        # the middle and lower layer
        #fracPos=[0.16666666666666667, 0.25, 0.308571429])
        #lat=array(orthorhombicSuperLattice)
#        realPos=dot(fracPos,lat).tolist()
        orthorhombicFracGraphKH2.append(['K', 0.6666666666666667, 0.33333333333333, 0.308571429])
        orthorhombicFracGraphKH2.append(['K', 2.6666666666666667, 3.33333333333333, 0.308571429])
        # put the hydrogens in any old place: 1 2/3, 4 1/3 and 2 2/3, 1 1/3
        # since hydrogen bond is .76 ang, it is ~.31 of a=2.456
#        fracPos=array([0.45, 0.75, 0.308571429])
#        lat=array(orthorhombicSuperLattice)
#        realPos=dot(fracPos,lat).tolist()
        orthorhombicFracGraphKH2.append(['H', 1.516666666666666667, 4.333333333333333333, 0.308571429])
        orthorhombicFracGraphKH2.append(['H', 1.816666666666666667, 4.333333333333333333, 0.308571429])
        orthorhombicFracGraphKH2.append(['H', 2.516666666666666667, 1.333333333333333333, 0.308571429])
        orthorhombicFracGraphKH2.append(['H', 2.816666666666666667, 1.333333333333333333, 0.308571429])
        
        #rotate this supercell so the x axis points along a and y along b and c along z
        #geometry shows sin theta = b_y/a_supercell
        a=2.456
        b_y=2.1269583916945813
        a_supercell=self.norm([2.5*a, math.sqrt(3)/2.*a, 0.0])
        theta=math.asin(b_y/a_supercell)
        
        R_theta=[math.cos(theta), -math.sin(theta)],\
            [math.sin(theta), math.cos(theta)]
        rotatedOrthorhombicFracGraphKH2
        for atom in orthorhombicFracGraphKH2:
            rotatedOrthorhombicFracGraphKH2.append([atom[0],
                R_theta[0][0]*atom[1]+R_theta[0][1]*atom[2],
                R_theta[1][0]*atom[1]+R_theta[1][1]*atom[2],
                atom[3]])
        print rotatedOrthorhombicFracGraphKH2
        
        # we use the unit lattice since the fractional coordinates pertain to it
        orthoSupercell=Supercell(orthorhombicFracGraphKH2, self.graphiteKH2Lattice, 1,1,1)
        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox.xyz'
        orthoSupercell.writeSupCellXYZFile(path)
        
        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox2.xyz'        
        
        normalOrthoSupercell=Supercell(readFilePath=path, n=16, m=8, l=1, coordType='cartesian')
        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox3.xyz'
        normalOrthoSupercell.writeSupCellXYZFile(path)
        self.printIncommensurateLattice()
        return   
    
    def printIncommensurateLattice(self):
        a=2.456
        c=9.04
        print [[2.5*a, math.sqrt(3)/2.*a, 0.0], [-1.5*a, math.sqrt(3)*5/2.*a, 0.0], [0.0, 0.0, 9.0399999999999991]]

if __name__ == '__main__': 
    suite1 = unittest.makeSuite(Supercell_TestCase)
    alltests = unittest.TestSuite((suite1))
    unittest.TextTestRunner(verbosity=2).run(alltests)
