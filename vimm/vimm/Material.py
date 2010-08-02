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



from vimm.Geometry import Geometry

#rename this to Scene
class Material:
    def __init__(self,name='material'):
        self.name = name
        self.geo = Geometry()
        self.geos = [self.geo]
        self.length = 1
        self.format = 'xyz'
        return

    def new_geo(self):
        self.geo = Geometry()
        self.geos.append(self.geo)
        self.length+=1
        return

    def get_name(self): return self.name
    def get_cell(self): return self.geo.get_cell()
    def get_atom_list(self): return self.geo.get_atom_list()
    def get_atoms(self): return self.geo.get_atoms()
    def get_bonds(self): return self.geo.get_bonds()
    def get_nat(self): return self.geo.get_nat()
    def get_nati(self): return self.geo.get_nati()
    def get_atom(self,iat): return self.geo.atoms[iat]
    
    def add_atom(self,atom): self.geo.add_atom(atom)
    def add_bond(self,bond): self.geo.add_bond(bond)
    def set_cell(self,cell): self.geo.set_cell(cell)
    def get_geos(self): return self.geos

    def delete_current_bonds(self): self.geo.delete_bonds()
    def delete_all_bonds(self):
        for geo in self.geos: geo.delete_bonds()
        return

    def set_name(self, name):
        self.name = name
        return

    def set_every_cell(self,cell):
        for geo in self.geos: geo.set_cell(cell)

    def center(self):
        for geo in self.geos: geo.center()
        
    def bonds_from_distance(self,scale=1.2,force_bonds=0):
        ''' calculate bonds based on distance
        
        Todo: this should be put in the structure class (not part of viewer)
        '''
        for geo in self.geos: geo.bonds_from_distance(scale,force_bonds)
        return

    def current_bonds_from_distance(self,scale=1.2,force_bonds=0):
        self.geo.bonds_from_distance(scale,force_bonds)
        return

    def current_frame(self):
        return self.geos.index(self.geo)

    def advance_frame(self):
        i = self.geos.index(self.geo)
        if i < self.length-1:
            self.geo = self.geos[i+1]
        else:
            self.geo = self.geos[0]
        return

    def backup_frame(self):
        i = self.geos.index(self.geo)
        if i > 0:
            self.geo = self.geos[i-1]
        else:
            self.geo = self.geos[self.length-1]
        return

    def set_frame(self, frame):
        if(frame >= 0 and frame < self.length):
            self.geo = self.geos[frame]
        else:
            self.geo = self.geos[0]
        return

    

