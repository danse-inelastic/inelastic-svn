#! /bin/env python

from pyre.components.Component import Component
from crystal.UnitCellBuilder import AtomLoader,
import math


class Cluster:
    '''creates a spherical cluster with arbitrary origin and cutoff radius.
    
The cluster origin must be given in fractional coordinates, such as 0.5 0.5 0.5 for the middle of the unit cell.
The cluster radius must be given in Angstroms.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        atoms = inv.facility('Atomic/Species information',default=AtomLoader())
        #atoms = inv.str('Atomic/Species information',default='')
        atoms.meta['tip'] = '''i.e. H core  0.0  0.0  0.0
O shell  1.0  0.0  0.0'''
        unitCell = inv.facility('Unit Cell', default=UnitCell())
        unitCell.meta['tip'] = 'Set the unit cell parameters.'
        
        filename = inv.str( "filename", default = "")
        filename.meta['tip'] = ".xyz file to be read in"
        n = inv.str( "n", default = "1")
        n.meta['tip'] = "number of supercells in a direction"
        m = inv.str( "m", default = "1")
        m.meta['tip'] = "number of supercells in b direction"
        l = inv.str( "l", default = "1")
        l.meta['tip'] = "number of supercells in c direction"
    
    def __init__(self, uc, atomPos, center=(0.0,0.0,0.0), radius=3.0):
        # construct cluster by translating unit cell in cartesian coordinates
        # in all three directions until the new origin is farther away than
        # the origin of the base unit cell
        xLim=int(math.ceil(radius/uc[0][0]))+1
        yLim=int(math.ceil(radius/uc[1][1]))+1
        zLim=int(math.ceil(radius/uc[2][2]))+1
        
        uc_spread=[]
        for ix in range(-(xLim-1),xLim):
         for iy in range(-(yLim-1),yLim):
          for iz in range(-(zLim-1),zLim):
           for s in self.ind(atomPos):
            uc_spread.append([atomPos[s][0], atomPos[s][1] + ix*uc[0][0], atomPos[s][2] + iy*uc[1][1], atomPos[s][3] + iz*uc[2][2]])
        
        # then eliminate all atoms from the list that are outside the
        # cluster origin
        
        self.clusterAtoms=[]
        for atom in uc_spread:
        # [atom[i+1]-center[i] for i in range(3)]
        # print norm([atom[i+1]-center[i] for i in range(3)])
         if self.norm([atom[i+1]-center[i] for i in range(3)])>radius:
          pass
         else:
          self.clusterAtoms.append(atom)
        

    def norm(self, vec):
        """gives the Euclidean norm of a vector"""
        temp=self.Sum([el**2. for el in vec])
        return math.sqrt(temp)
    
    def Sum(self, x):
        total=0
        for part in x:
            total=total+part
        return total
    
    def ind(self, list):
        """gives the indices of the list to iterate over"""
        return range(len(list))
    
    def getAtoms(self):
        return self.clusterAtoms
    
    def create(self):
        

## write cluster atoms to .bas file
#f=file('cluster.bas','w')
#print >>f, len(clusterAtoms)
#for atom in clusterAtoms:
#    print >>f, atom[0],atom[1],atom[2],atom[3]


if __name__=='__main__':
    unitcell=[[4.58666, 0, 0],[0, 4.58666, 0],[0,0,2.95407]]
    atoms=[
 ['Ti', 0.0,         0.0,         0.0],
 ['Ti', 2.29333,     2.29333,     1.477035],
 ['O',  1.397509435, 1.397509435, 0.0],
 ['O',  3.189150565, 3.189150565, 0.0],
 ['O',  3.690839435, .8958205646, 1.477035],
 ['O',  .8958205646, 3.690839435, 1.477035]]
    cluster=Cluster(unitcell,atoms)
    for atom in cluster.getAtoms():
        print atom
