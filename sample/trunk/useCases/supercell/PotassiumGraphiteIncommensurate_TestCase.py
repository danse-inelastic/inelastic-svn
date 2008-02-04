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
import danseGlob, math

appName = "PotassiumGraphiteIncommensurate"
caseName = "fulltest"

import journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

class PotassiumGraphiteIncommensurate_TestCase(unittest.TestCase):
    
    def setUp(self):
        """
        do potassium graphite supercell as incommensurate approximation
        """
        self.graphiteKUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.4], 
                 ['C', 0.0, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 5.4]]
        self.graphiteKLattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 8.75]]
        
        self.graphiteKH2UnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 5.69], 
                 ['C', 0.0, 1.4179793509910266, 0.0], 
                 ['C', 1.228, 0.70900031028747168, 5.69]]
        self.graphiteKH2Lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 9.04]]  
    
    def testC28KToOrthorhombicSupWithK(self):
        '''convert a C28 hexagonal supercell to orthorhombic and add potassium'''
        # first get 3x2x1 supercell of real coordinates from graphite
        supercell=Supercell(self.graphiteKUnitCell,self.graphiteKLattice,3,2,1,coordType='cartesian')
        fracCoords=supercell.getSupercellFractionalCoordinates()
        lattice=supercell.getSupercellLatticeVectors()
        #print lattice   
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
        
        
    def testC28KToOrthorhombicSupWithKAndH(self):
        '''convert a C28 hexagonal supercell to orthorhombic and add potassium using 
        the experimental spacing of C_28 K with H_2''' 
        # first get 3x2x1 supercell of real coordinates from graphite
        supercell=Supercell(self.graphiteKH2UnitCell,self.graphiteKH2Lattice,3,2,1,coordType='cartesian')
        fracCoords=supercell.getSupercellFractionalCoordinates()
        lattice=supercell.getSupercellLatticeVectors()
        #print lattice   
        #print fracCoords       
        
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

        orthoSupercell=Supercell(orthorhombicFracGraphKH2, self.graphiteKH2Lattice, 1,1,1)
        # get the real coordinates
        realCoords=orthoSupercell.getSupercellRealCoordinates()
        #write it to an xyz file
        realOrthoSupercell=Supercell(realCoords, self.getIncommensurateLattice(),1,1,1, coordType='cartesian')
        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox.xyz'
        realOrthoSupercell.writeSupCellXYZFile(path)
        
        assert(realCoords==realOrthoSupercell.getSupercellRealCoordinates())

#        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox2.xyz'        
#        
#        normalOrthoSupercell=Supercell(readFilePath=path, n=1, m=1, l=1, coordType='cartesian')
#        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'incommensurateApprox3.xyz'
#        normalOrthoSupercell.writeSupCellXYZFile(path)

        #rotate this supercell so the x axis points along a and y along b and c along z
        #geometry shows sin theta = b_y/a_supercell
        a=2.456
        b_y=2.1269583916945813
        a_supercell=self.norm([2.5*a, math.sqrt(3)/2.*a, 0.0])
        theta=math.asin(b_y/a_supercell)
        
        R_theta=[[math.cos(theta), math.sin(theta)],\
            [-math.sin(theta), math.cos(theta)]]
        print R_theta
        rotatedRealCoords=[]
        for atom in realCoords:
            rotatedAtom=[atom[0],
                R_theta[0][0]*atom[1]+R_theta[0][1]*atom[2],
                R_theta[1][0]*atom[1]+R_theta[1][1]*atom[2],
                atom[3]]
            print 'before',atom
            print 'rotated',rotatedAtom
            rotatedRealCoords.append(rotatedAtom)

        rotatedOrthoSupercell=Supercell(rotatedRealCoords, self.getRotatedIncommensurateLattice(), 1,1,1, coordType='cartesian')
        path=danseGlob.installDir+sep+'ccp1gui'+sep+'tests'+sep+'rotatedIncommensurateApprox.xyz'
        rotatedOrthoSupercell.writeSupCellXYZFile(path)
        

 
    def getIncommensurateLattice(self):
        a=2.456
        c=9.04
        return [[2.5*a, math.sqrt(3)/2.*a, 0.0], [-1.5*a, math.sqrt(3)*5/2.*a, 0.0], [0.0, 0.0, c]]
        
    def getRotatedIncommensurateLattice(self):
        a=2.456
        c=9.04
        aPrime=self.norm([2.5*a, math.sqrt(3)/2.*a, 0.0])
        bPrime=self.norm([-1.5*a, math.sqrt(3)*5/2.*a, 0.0])
        return [[aPrime, 0.0, 0.0], [0.0, bPrime, 0.0], [0.0, 0.0, c]]
        
    def norm(self,vec):
        """gives the Euclidean _norm of a list of floats"""
        temp=sum([el**2. for el in vec])
        return math.sqrt(temp)

if __name__ == '__main__': 
    suite1 = unittest.makeSuite(PotassiumGraphiteIncommensurate_TestCase)
    alltests = unittest.TestSuite((suite1))
    unittest.TextTestRunner(verbosity=2).run(alltests)
