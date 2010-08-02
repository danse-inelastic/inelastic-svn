# Vimm: Visual Interface to Materials Manipulation
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


#!/usr/bin/env python
"Bins - a collection of routines to collect atoms"

from math import sqrt
from vimm.NumWrap import dot
from vimm.Element import rcov
from vimm.Bond import Bond
from vimm.Utilities import bbox_atoms

BIG = 1000.
BUFFER = 0.2
ANGS_CELL = 2.0  # Size of cells

# prevent zero-length bonds; turned off because in
#  theory we should never have it, and we'd like to crash when we
#  do have it so that we know about it.
MIN_BOND_LENGTH = 0.1  

class SimpleBins:
    def __init__(self,atoms):
        self.atoms = atoms
        self.get_bbox()
        self.nbinsx = max(1,int(self.dx/ANGS_CELL))
        self.nbinsy = max(1,int(self.dy/ANGS_CELL))
        self.nbinsz = max(1,int(self.dz/ANGS_CELL))
        self.nbins = self.nbinsx*self.nbinsy*self.nbinsz
        self.make_bins()
        self.add_atoms()
        return

    def get_bbox(self):
        bbox = bbox_atoms(self.atoms,BUFFER,BIG)
        self.xmin,self.xmax = bbox[0:2]
        self.ymin,self.ymax = bbox[2:4]
        self.zmin,self.zmax = bbox[4:6]
        self.dx = self.xmax - self.xmin
        self.dy = self.ymax - self.ymin
        self.dz = self.zmax - self.zmin
        return

    def make_bins(self):
        self.bins = []
        self.bin_index = {}
        self.bin_ijk = []
        ijk = 0
        for i in range(self.nbinsx):
            for j in range(self.nbinsy):
                for k in range(self.nbinsz):
                    self.bins.append([])
                    self.bin_index[i,j,k] = ijk
                    self.bin_ijk.append((i,j,k))
                    ijk += 1
        return

    def add_atoms(self):
        ii = 0
        for atom in self.atoms:
            xyz = atom.get_xyz()
            i = int(self.nbinsx*(xyz[0]-self.xmin)/self.dx)
            j = int(self.nbinsy*(xyz[1]-self.ymin)/self.dy)
            k = int(self.nbinsz*(xyz[2]-self.zmin)/self.dz)
            ijk = self.bin_index[i,j,k]
            self.bins[ijk].append(atom)
        return

    def bonds_from_distance(self,scale=1.2):
        bonds = []

        #splitting this in half only so I know which one is the
        # slow part for big systems
        bonds_other = self.bonds_from_distance_other(scale)
        bonds_self = self.bonds_from_distance_self(scale)
        return bonds_other + bonds_self
        

    def bonds_from_distance_other(self,scale=1.2):
        bonds = []
        for icell in range(self.nbins):
            atomsi = self.bins[icell]
            for jcell in self.neighbors_less(icell):
                atomsj = self.bins[jcell]
                for iat in range(len(atomsi)):
                    atomi = atomsi[iat]
                    xyzi = atomi.get_xyz()
                    atnoi = atomi.get_atno()
                    for jat in range(len(atomsj)):
                        atomj = atomsj[jat]
                        xyzj = atomj.get_xyz()
                        atnoj = atomj.get_atno()
                        dxyz = xyzi - xyzj
                        r2 = dot(dxyz,dxyz)
                        cut=scale*(rcov[atnoi]+rcov[atnoj])
                        cut2 = cut*cut
                        if r2 < cut2:
                            bonds.append(Bond(atomi,atomj))
        return bonds

    def bonds_from_distance_self(self,scale=1.2):
        bonds = []
        for icell in range(self.nbins):
            atomsi = self.bins[icell]
            for iat in range(len(atomsi)):
                atomi = atomsi[iat]
                xyzi = atomi.get_xyz()
                atnoi = atomi.get_atno()
                for jat in range(iat):
                    atomj = atomsi[jat]
                    xyzj = atomj.get_xyz()
                    atnoj = atomj.get_atno()
                    dxyz = xyzi - xyzj
                    r2 = dot(dxyz,dxyz)
                    cut=scale*(rcov[atnoi]+rcov[atnoj])
                    cut2 = cut*cut
                    if r2 < cut2:
                        bonds.append(Bond(atomi,atomj))
        return bonds

    def neighbors_less(self,icell):
        "Return all neighboring cells less than icell"
        ii,ij,ik = self.bin_ijk[icell]
        neighbors = []
        nrange = [-1,0,1]
        for dx in nrange:
            ji = ii + dx
            if ji < 0 or ji >= self.nbinsx: continue
            for dy in nrange:
                jj = ij + dy
                if jj < 0 or jj >= self.nbinsy: continue
                for dz in nrange:
                    jk = ik + dz
                    if jk < 0 or jk >= self.nbinsz: continue
                    jcell = self.bin_index[ji,jj,jk]
                    if jcell < icell: neighbors.append(jcell)
        return neighbors
                
            

    
