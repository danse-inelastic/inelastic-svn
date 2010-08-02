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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA	02111-1307	
# USA

from vimm.POVRay import Scene, Sphere, Cylinder
from vimm.Element import color1, rvdw

extensions=["pov"]
filetype="POVRay Output Graphics Format"

def save(filename, material):
	file=open(filename, 'w')
	atoms = material.get_atoms()
	bonds = material.get_bonds()
	scene = Scene()
	for atom in atoms:
		atno = atom.atno
		rgb = color1[atno]
		rad = rvdw[atno]
		scene.add(Sphere(tuple(atom.xyz),0.1,rgb))
	for bond in bonds:
		atom1 = bond.atom1
		atom2 = bond.atom2
		rgb1 = color1[atom1.atno]
		rgb2 = color1[atom2.atno]
		midpoint = (atom1.xyz + atom2.xyz)/2
		scene.add(Cylinder(tuple(atom1.xyz),tuple(midpoint),0.1,rgb1))
		scene.add(Cylinder(tuple(midpoint),tuple(atom2.xyz),0.1,rgb2))
	scene.write_pov(filename)
	scene.render()
	return
