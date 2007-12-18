#!/usr/bin/env python

import sys, os, math
import numpy as np
from pyre.components.Component import Component
from crystal.UnitCellBuilder import AtomLoader

# turn this into a supercell factory and a supercell dataobject

class Supercell(Component):
    #TODO: fix so does realCoords=None, fracCoords=None, ... initialization and put coords and lattice
    # in pyre inventory as well (and make it so these can be set from the constructor (as well as just self variables)
    
    '''
    This class takes a fractional or cartesian coordinate list and lattice vector list and 
    makes an n x m x l super cell.  User can query information about the
    supercell or write an xyz file of the coordinates.
    
    It also makes supercells from files of xyz coordinates and lattice vectors
    
    programmer's note: this class has partly used numpy and partly not
    due to the existence of legacy code
    '''

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
#        n = inv.str( "n", default = "1")
#        n.meta['tip'] = "number of supercells in a direction"
#        m = inv.str( "m", default = "1")
#        m.meta['tip'] = "number of supercells in b direction"
#        l = inv.str( "l", default = "1")
#        l.meta['tip'] = "number of supercells in c direction"
        n = inv.int( "n", default = 1)
        n.meta['tip'] = "number of supercells in a direction"
        m = inv.int( "m", default = 1)
        m.meta['tip'] = "number of supercells in b direction"
        l = inv.int( "l", default = 1)
        l.meta['tip'] = "number of supercells in c direction"
        atomicStructure = inv.facility('atomicStructure', default='unitCellBuilder')
        atomicStructure.validator = inv.choice(['unitCellBuilder','xyzFile'])
        atomicStructure.meta['tip'] = 'input the atomic structure (simulation cell, coordinates, etc.)'

    def __init__(self, atoms=None, latticeVectors=None, coordType='fractional', readFilePath=None):
        Component.__init__(self, 'Supercell', facility=None)
        self.i=self.inventory        
        self.coordinateType=coordType
        if readFilePath!=None:
            self.readXYZFile(readFilePath)
        else:
            self.atoms=atoms
            self.lattice=latticeVectors
            
        #get whatever facility the user has chosen and then 
        # call methods within that component to get the required data object

        # now initialize everything
        self.nlattice=np.array(self.lattice)
        self.supercellLattice=[[self.i.n*component for component in self.lattice[0]],
                 [self.i.m*component for component in self.lattice[1]],
                 [self.i.l*component for component in self.lattice[2]]]
        self.abc=self.getABC()
        self.ABC=self.getSupercellABC()
        #self.fracAtomPosInSupCell=[]
        self.supCellRealAtomPos=[]
        self.supCellFracAtoms=[]
            
    def _ind(self,list):
        """gives the indices of the list to iterate over"""
        return range(len(list))
    
    def _norm(self,vec):
        """gives the Euclidean _norm of a list of floats"""
        temp=sum([el**2. for el in vec])
        return math.sqrt(temp)
    
    def getABC(self):
        """gives the lattice parameters"""
        return [self._norm(vec) for vec in self.lattice]
    
    def getAtoms(self):
        return self.atoms
    
    def getLatticeVectors(self):
        return self.lattice
    
    def getSupercellABC(self):
        """gives the supercell lattice parameters"""
        return [self._norm(vec) for vec in self.supercellLattice]
    
    def getSupercellFractionalCoordinates(self):
        """gives the supercell atoms in terms of fractional coordinates 
            of the supercell"""
        return self.supCellFracAtoms 
    
    def getSupercellRealCoordinates(self):
        return self.supCellRealAtomPos
        
    def getSupercellLatticeVectors(self):
        return self.supercellLattice
    
    def readXYZFile(self,path):
        '''reads an xyz file to create a lattice object
        this method assumes the real space vectors are given on the second line (i.e.):
        [[9.8239999999999998, 0.0, 0.0], [-7.3680000000000003, 12.761750350167489, 0.0], [0.0, 0.0, 6.6959999999999997]]
        '''
        f=file(path,'r')
        lines=f.readlines()
        numAtoms=int(lines[0]) 
        self.lattice=np.array([float(i) for i in lines[1].split()])
        self.lattice=self.lattice.reshape(3,3)
        self.lattice=self.lattice.tolist()
        #self.lattice=eval(lines[1])        
        self.atoms=[]
        for i in range(2, numAtoms+2):
            species,x,y,z=lines[i].split()
            self.atoms.append([species,float(x), float(y), float(z)])
        f.close()
        return
    
    def writeSupCellXYZFile(self,name):
        '''writes an xyz file of the supercell coordinates'''
        f=open(name,'w')
        f.write(str(len(self.supCellRealAtomPos))+os.linesep)
        print >>f, self.supercellLattice
        for atom in self.supCellRealAtomPos:
            newAtom=[str(component) for component in atom]    
            f.write(" ".join(newAtom)+os.linesep)
        f.close()
        return 
    
    def create(self):   
        '''creates the supercell'''   
        for i in range(self.i.n):
          for j in range(self.i.m):
            for k in range(self.i.l):
              for p in self._ind(self.atoms):
                if self.coordinateType=='fractional':
                  extendedFracPos=[self.atoms[p][0],
                   self.atoms[p][1] + i,
                   self.atoms[p][2] + j,
                   self.atoms[p][3] + k]
                  realPos=[extendedFracPos[0], 
                   extendedFracPos[1]*self.lattice[0][0]
                   +extendedFracPos[2]*self.lattice[1][0]
                   +extendedFracPos[3]*self.lattice[2][0],
                   extendedFracPos[1]*self.lattice[0][1]
                   +extendedFracPos[2]*self.lattice[1][1]
                   +extendedFracPos[3]*self.lattice[2][1],
                   extendedFracPos[1]*self.lattice[0][2]
                   +extendedFracPos[2]*self.lattice[1][2]
                   +extendedFracPos[3]*self.lattice[2][2]]
                  self.supCellRealAtomPos.append(realPos) 
                  self.supCellFracAtoms.append([self.atoms[p][0]]
                     + [self.abc[ii]/self.ABC[ii]*extendedFracPos[ii+1] for ii in range(3)])  
                if self.coordinateType=='cartesian':
                  realPos=[self.atoms[p][0],
                   self.atoms[p][1] +i*self.lattice[0][0]
                   +j*self.lattice[1][0]
                   +k*self.lattice[2][0],
                   self.atoms[p][2] + i*self.lattice[0][1]
                   +j*self.lattice[1][1]
                   +k*self.lattice[2][1],
                   self.atoms[p][3] + i*self.lattice[0][2]
                   +j*self.lattice[1][2]
                   +k*self.lattice[2][2]]
                  self.supCellRealAtomPos.append(realPos) 
                  vec=np.array(realPos[1:4])
                  #print vec
                  mat=np.linalg.inv(self.nlattice)
                  #print mat
                  fracPos=np.dot(vec,mat)
                  #print fracPos
                  fracPosList=fracPos.tolist()
                  self.supCellFracAtoms.append([self.atoms[p][0]]+fracPosList)
        return
        

if __name__ == "__main__":
    lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 6.696]]
    fracUnitCell=[['C', 0.0, 0.0, 0.0], ['C', 0.0, 0.0, 0.5], 
                        ['C', 0.33333000000000002, 0.66666999999999998, 0.0], 
                        ['C', 0.66666999999999998, 0.33333999999999997, 0.5]]
    supercellFromFrac=Supercell(fracUnitCell,lattice,2,1,1)
    print supercellFromFrac.getSupercellFractionalCoordinates()
