# Vimm: Visual Interface for Materials Manipulation
#
# Copyright 2010 Caltech.  Copyright 2005 Sandia Corporation. 
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



# read and view pickled structure object
from matter import Structure, Lattice, Atom
at1 = Atom('C', [0.333333333333333, 0.666666666666667, 0])
at2 = Atom('C', [0.666666666666667, 0.333333333333333, 0])
a = 2.4612
c = 6.7079
graphite = Structure( [ at1, at2], lattice=Lattice(a, a, c, 90, 90, 120) )
print graphite

import pickle
output = open('graphite.pkl', 'wb')
pickle.dump(graphite, output)
output.close()

pkl_file = open('graphite.pkl', 'rb')
g2 = pickle.load(pkl_file)
print g2






#m2 = create_nanotube(10,10,10)
#save_file("nano.xyz", m2)

#atoms = m1.get_atoms()
#d = measure_distance(atoms[0], atoms[1])
#print d

#m3 = build_crystal_from_db("Diamond")
#v2 = Viewer(m3)
