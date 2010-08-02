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



from vimm.Element import symbol

class Atom:
    def __init__(self,atno,xyz,sym=None,label=None):
        self.atno = atno
        self.xyz = xyz
        if not sym:
            self.symbol = symbol[atno]
        else:
            self.symbol = sym
        if not label:
            self.label = self.symbol
        else:
            self.label = label
        self.fftype = None
        return

    def get_position(self): return self.xyz
    def set_label(self,label): self.label = label
    def get_label(self): return self.label
    def get_symbol(self): return self.symbol
    def set_xyz(self, xyz): self.xyz = xyz
    def get_xyz(self): return self.xyz
    def get_atno(self): return self.atno

    def update_symbol(self):
        self.symbol = symbol[self.atno]
        return

    def update_label(self):
        old_label = self.label[1:]
        if not old_label[0].isdigit():
            old_label = old_label[1:]
        self.label = self.symbol + old_label
        return

    def distance(self,other):
        from NumWrap import dot
        from math import sqrt
        d = self.xyz - other.xyz
        return sqrt(dot(d,d))

