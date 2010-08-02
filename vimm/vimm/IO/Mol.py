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

from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Bond import Bond
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["mol","MOL"]
filetype="MOL file format"

# See Dalby et al., J. Chem. Inf. Comput. Sci, 32, 244, 1992
# for more information on the MOL format

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    file=open(fullfilename, 'r')

    line = file.readline()
    title = line.strip()
    line = file.readline()
    title2 = line.strip()
    line = file.readline()
    title3 = line.strip()

    line = file.readline()
    natoms = int(line[:3])
    nbonds = int(line[3:6])

    # Note: I'm skipping the H information here, which is
    #  typically given in fields 5-
    for i in range(natoms):
        line = file.readline()
        words = line.split()
        xyz = array(map(float,words[:3]))
        sym = cleansym(words[3])
        atno = sym2no[sym]
        material.add_atom(Atom(atno,xyz,sym,sym+str(i)))
    atoms = material.get_atoms()
    for i in range(nbonds):
        line = file.readline()
        words = line.split()
        # bond order is the third field, which I'm ignoring
        iat,jat,iorder = map(int,words[:3])
        material.add_bond(Bond(atoms[iat-1],atoms[jat-1],iorder))
    return material

def new():
    material = Material("New MOL Molecule")
    return material

def save(filename,material):
    file=open(filename, 'w')
    atoms = material.get_atoms()
    bonds = material.get_bonds()
    file.write('MOL file written by vimm.xyz\n\n\n')
    file.write('%3d%3d  0  0  0  0  0  0  0  0999 V2000\n'
               % (len(atoms),len(bonds)))
    for atom in atoms:
        x,y,z = atom.get_xyz()
        atno = atom.get_atno()
        file.write('%10.4f%10.4f%10.4f %3s 0  0  0  0  0\n'
                   % (x,y,z,symbol[atno]))
    for bond in bonds:
        ati,atj = bond.get_atoms()
        iat = atoms.index(ati)
        jat = atoms.index(atj)
        #iat,jat = atoms.index[ati],atoms.index[atj]
        iorder = bond.get_order()
        file.write('%3d%3d%3d  0  0  0\n' % (iat+1,jat+1,iorder))
    return
