# vimm: Visual Interface for Materials Manipulation
#
# Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation.  Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government
# retains certain rights in this sofware.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
# USA



from math import sqrt
from vimm.Atom import Atom
from vimm.NumWrap import zeros,dot
from vimm.Element import rcov
from vimm.Bond import Bond
from vimm.Bins import SimpleBins

NAT_BOND_CUTOFF = 5000 # Number of atoms at which to not compute bonds

class Geometry:
    def __init__(self):
        self.atoms = []
        self.images = [] # periodic images of atoms
        self.bonds = []
        self.cell = None
        self.surface = []
        self.nsurface = []
        self.pyq_basis = None
        return

    def get_bonds(self): return self.bonds
    def get_atoms(self): return self.atoms
    def get_atom_list(self): return self.atoms #compat with icarus
    def get_cell(self): return self.cell
    def get_nat(self): return len(self.atoms)
    def get_nati(self): return len(self.atoms) + len(self.images)

    def add_atom(self,atom): self.atoms.append(atom)
    def add_image(self,atom): self.images.append(atom)
    def add_bond(self,bond): self.bonds.append(bond)
    def set_cell(self,cell): self.cell = cell

    def delete_bonds(self): self.bonds = []

    def clear(self):
        self.atoms = []
        self.images = [] # periodic images of atoms
        self.bonds = []
        self.cell = None
        self.surface = []
        self.nsurface = []
        self.pyq_basis = None
        
    def center(self):
        xyzsum = zeros(3,'d')
        for atom in self.atoms:
            xyzsum += atom.xyz
        xyzsum /= len(self.atoms)
        #print "subtracting center of mass = ",xyzsum
        for atom in self.atoms: atom.xyz -= xyzsum
        return

    def bonds_from_distance(self, scale=1.2, force_bonds=0):
        # force_bonds:  Logical variable that determines whether we are
        #               going to force bond finding for really large
        #               molecules
        self.get_periodic_images()
        atoms_images = self.atoms + self.images
        nat = len(atoms_images)

        if nat > NAT_BOND_CUTOFF:
            if force_bonds:
                self.bonds = binned_bond_finder(atoms_images, scale)
        elif nat > 50:
            self.bonds = binned_bond_finder(atoms_images,scale)
        else:
            self.bonds = simple_bond_finder(atoms_images,scale)
        return

    def get_periodic_images(self):
        img_cutoff = 0.1 #Angs- distance cutoff for an image to be
                         # near a uc boundary
        if not self.cell: return
        axyz = self.cell.axyz
        bxyz = self.cell.bxyz
        cxyz = self.cell.cxyz
        #conv = self.cell.cart2lat_factory()
        
        # lattice translations
        I = [(1,0,0)]
        J = [(0,1,0)]
        IJ = [(1,0,0),(0,1,0),(1,1,0)]
        K = [(0,0,1)]
        IK = [(1,0,0),(0,0,1),(1,0,1)]
        JK = [(0,1,0),(0,0,1),(0,1,1)]
        IJK = [(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)]
        atoms = self.atoms
        nimages = len(atoms)+1 # The 1 really is necessary here!
        for atom in atoms:
            atno = atom.get_atno()
            xyz = atom.get_position()
            # The right way to do this is to convert to lattice
            #  coords and test those for being near 0 or 1
            #xl,yl,zl = conv(x,y,z)
            x,y,z = xyz
            if abs(x) < img_cutoff:
                if abs(y) < img_cutoff:
                    if abs(z) < img_cutoff: directions = IJK
                    else: directions = IJ
                else:
                    if abs(z) < img_cutoff: directions = IK
                    else: directions = I
            else:
                if abs(y) < img_cutoff:
                    if abs(z) < img_cutoff: directions = JK
                    else: directions = J
                else:
                    if abs(z) < img_cutoff: directions = K
                    else: directions = []
            for i,j,k in directions:
                xyznew = xyz + i*axyz + j*bxyz + k*cxyz
                self.add_image(Atom(atno,xyznew))
        return

        
def simple_bond_finder(atoms,scale=1.2):
    bonds = []
    for i in range(len(atoms)):
        atomi = atoms[i]
        for j in range(i):
            atomj = atoms[j]
            xyzij = atomi.xyz - atomj.xyz
            rij = sqrt(dot(xyzij,xyzij))
            if rij < scale*(rcov[atomi.atno]+rcov[atomj.atno]):
                bonds.append(Bond(atomi,atomj))
    return bonds

def binned_bond_finder(atoms,scale=1.2):
    bins = SimpleBins(atoms)
    bonds = bins.bonds_from_distance(scale)
    return bonds
    
