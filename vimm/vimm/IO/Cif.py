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



from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["cif"]
filetype="Cif Format"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    
    try:
        from matter.Structure import Structure
        st = Structure()
        st.read(fullfilename)
        for i,atom in enumerate(st):
            sym = atom.symbol
            xyz = atom.xyz
            material.add_atom(Atom(i, xyz, sym, sym+str(i)))
        #material.bonds_from_distance()
        return material
    except:
        print 'Vimm needs matter package from pypi to open cif files'
        return

def save(filename, material):
    print 'saving cif structures not supported yet'
#    file=open(filename, 'w')
#    for geo in material.get_geos():
#        atoms = geo.get_atoms()
#        file.write('%d\nFile written by vimm.xyz\n' % len(atoms))
#        for atom in atoms:
#            x,y,z = atom.get_xyz()
#            atno = atom.get_atno()
#            file.write('%s %f %f %f\n' % (symbol[atno],x,y,z))
    return

def new():
    material = Material("New Cif Structure")
    return material
