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

__doc__="""For now we load a structure and convert it to VIMM's internal
data structures (Material and Atom), although eventually these two 
objects will grow together so VIMM will be able to plot Structure objects
directly

Also, eventually this will be generalized to handle any Vibrations and
Motion pickled data objects as well.
"""

import pickle


from vimm.Utilities import path_split,cleansym

extensions=["pkl"]
filetype="Pickled Structure Format"

def load(fullfilename):
    #TODO move this splitting to within Material so the extension can 
    #automatically be the default prefix...then move it into structure
    filedir, fileprefix, fileext = path_split(fullfilename)
    from vimm.Material import Material
    from vimm.Atom import Atom
    from vimm.Cell import Cell
    material=Material(fileprefix)
    material.format = fileext
    
    pkl_file = open(fullfilename, 'rb')
    structure = pickle.load(pkl_file)

    first_run = 1

    if first_run:
        first_run = 0
    else:
        material.new_geo()

    for structureAtom in structure:
        material.add_atom(Atom(structureAtom.Z, structureAtom.xyz_cartn))
    aVec,bVec,cVec = structure.lattice.base
    cell = Cell(aVec,bVec,cVec)
    material.set_cell(cell)
    material.bonds_from_distance()
    return material
    

def save(filename, material):
    for geo in material.get_geos():
        atoms = geo.get_atoms()
        from matter import Structure, Lattice
        import matter.Atom as matterAtom
        for atom in atoms:
            x,y,z = atom.get_xyz()
            atno = atom.get_atno()
            atoms.append(matterAtom(symbol[atno],[x,y,z]))
        cell = geo.get_cell()
        a,b,c,alph,bet,gam = cell.abcabg
        lattice = Lattice(a,b,c,alph,bet,gam)
        stru = Structure( atoms, lattice)
    import pickle
    output = open(filename, 'wb')
    from Utilities import assureCorrectFileEnding
    filename = assureCorrectFileEnding(filename, 'pkl')
    pickle.dump(stru, output)
    output.close()

    return

def new():
    from vimm.Material import Material
    material = Material("New Structure")
    return material
