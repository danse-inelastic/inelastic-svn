#!/usr/bin/env python
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
"""\
 ZMatrix.py - support for internal coordinates.

 The ZMatrix format is a way to specify internal coordinates
 for molecules. This normally takes the form of

 C1                  
 H1 C1  1.0      
 H2 C1  1.0  H1 109.5
 H3 C1  1.0  H1 109.5  H2  60

 which can be translated as:
 1. create an atom of type C1
 2. create an atom of type H1, 1.0 Angstroms from C1
 3. create an atom of type H2, 1.0 Angstroms from C1
    and with the H2-C1-H1 bond angle of 109.5 degrees
 4. create an atom of type H3, 1.0 angstroms from C1,
    with the H3-C1-H1 bond angle of 109.5 degrees, and
    with the H3-C1-H1-H2 torsional angle of 60 degrees.
"""

from math import pi,sin,cos,atan,sqrt

from vimm.Atom import Atom
from vimm.NumWrap import array,dot
from vimm.Element import sym2no
from vimm.Utilities import cleansym

deg2rad = pi/180.

def ZMatrix(zatoms):
    natoms = len(zatoms)
    atoms = []
    # keep a running track of the labels for reference
    labels = {}
    for i in range(natoms):
        zatom = zatoms[i]
        if type(zatom) == type(''):
            label = zatom
        else:
            label = zatom[0]
        assert label not in labels
        sym = cleansym(label)
        atno = sym2no[sym]
        if i == 0:
            x,y,z = 0.0,0.0,0.0
        elif i == 1:
            label1 = zatom[1]
            assert label1 in labels
            r = zatom[2]
            x,y,z = r,0,0
        elif i == 2:
            label1  = zatom[1]
            assert label1 in labels
            atom1 = labels[label1]
            x1,y1,z1 = atom1.xyz
            r = zatom[2]
            label2 = zatom[3]
            assert label2 in labels
            atom2 = labels[label2]
            x2,y2,z2 = atom2.xyz

            if abs(x2-x1) < 1e-5:
                thetap = pi
            else:
                thetap = atan((y2-y1)/(x2-x1))
            if x2 < x1: thetap += pi

            theta = zatom[4]*deg2rad
            ang = theta + thetap

            rc = r*cos(ang)
            rs = r*sin(ang)
            x,y,z = x1+rc,y1+rs,z1
        else:
            label1  = zatom[1]
            assert label1 in labels
            atom1 = labels[label1]
            r = zatom[2]
            label2 = zatom[3]
            assert label2 in labels
            atom2 = labels[label2]
            theta = zatom[4]*deg2rad
            label3 = zatom[5]
            assert label3 in labels
            atom3 = labels[label3]
            phi = zatom[6]*deg2rad

            v12 = atom1.xyz - atom2.xyz
            v13 = atom1.xyz - atom3.xyz
            n = cross(v12,v13)
            nn = cross(v12,n)
            n = normalize(n)
            nn = normalize(nn)

            n = -n*sin(phi)
            nn = nn*cos(phi)

            v3 = normalize(n+nn)
            v3 = v3*r*sin(theta)

            v12 = normalize(v12)
            v12 = v12*r*cos(theta)
            v2 = atom1.xyz + v3 - v12
            x,y,z = v2
        atom = Atom(atno,array((x,y,z)),label)
        atoms.append(atom)
        labels[label] = atom
    return atoms

def cross(a,b): return array((a[1]*b[2]-a[2]*b[1],
                              a[2]*b[0]-a[0]*b[2],
                              a[0]*b[1]-a[1]*b[0]))
def normalize(a): return a/sqrt(dot(a,a))

def printatoms(atoms):
    for atom in atoms: print atom.symbol,atom.xyz
    return

def test():
    #atoms = ZMatrix([('C')])
    #atoms = ZMatrix([('C1'),('H1','C1',1.0)])
    #atoms = ZMatrix([('C1'),('H1','C1',1.0),('H2','C1',1.0,'H1',109.5)])
    #printatoms(atoms)
    #atoms = ZMatrix([('C1'),('H1','C1',1.0),('H2','H1',1.0,'C1',109.5)])
    #printatoms(atoms)
    atoms = ZMatrix([('C1'),
                     ('H1','C1',1.0),
                     ('H2','C1',1.0,'H1',109.5),
                     ('H3','C1',1.0,'H1',109.5,'H2',60.),
                     ('H4','C1',1.0,'H1',109.5,'H2',-60.)])
    printatoms(atoms)

def hydros():
    #name = 'methane'
    #atoms = ZMatrix([('C1'),
    #                 ('H1','C1',1.0),
    #                 ('H2','C1',1.0,'H1',109.5),
    #                 ('H3','C1',1.0,'H1',109.5,'H2',120.),
    #                 ('H4','C1',1.0,'H1',109.5,'H2',-120.)])
    #output_bgf(name,atoms)

    #name = 'ethane'
    #atoms = ZMatrix([('C1'),
    #                 ('H1','C1',1.0),
    #                 ('H2','C1',1.0,'H1',109.5),
    #                 ('H3','C1',1.0,'H1',109.5,'H2',120.),
    #                 ('C2','C1',1.5,'H1',109.5,'H2',-120.),
    #                 ('H4','C2',1.0,'C1',109.5,'H1',180.),
    #                 ('H5','C2',1.0,'C1',109.5,'H1',60.),
    #                 ('H6','C2',1.0,'C1',109.5,'H1',-60.)])
    #output_bgf(name,atoms)

    #name = 'ethylene'
    #atoms = ZMatrix([('C1'),
    #                 ('H1','C1',1.0),
    #                 ('H2','C1',1.0,'H1',120),
    #                 ('C2','C1',1.4,'H1',120,'H2',180.),
    #                 ('H4','C2',1.0,'C1',120,'H1',180.),
    #                 ('H6','C2',1.0,'C1',120,'H1',0)])
    #output_bgf(name,atoms)

    #name = 'acetylene'
    #atoms = ZMatrix([('C1'),
    #                 ('H1','C1',1.0),
    #                 ('C2','C1',1.4,'H1',179),
    #                 ('H2','C2',1.0,'C1',179,'H1',180.)])
    #output_bgf(name,atoms)
    
    #name = 'ethane_gauche'
    #atoms = ZMatrix([('C1'),
    #                 ('H1','C1',1.0),
    #                 ('H2','C1',1.0,'H1',109.5),
    #                 ('H3','C1',1.0,'H1',109.5,'H2',120.),
    #                 ('C2','C1',1.5,'H1',109.5,'H2',-120.),
    #                 ('H4','C2',1.0,'C1',109.5,'H1',0.),
    #                 ('H5','C2',1.0,'C1',109.5,'H1',120.),
    #                 ('H6','C2',1.0,'C1',109.5,'H1',-120.)])
    #output_bgf(name,atoms)

    name = 'ethylene_twist'
    atoms = ZMatrix([('C1'),
                     ('H1','C1',1.0),
                     ('H2','C1',1.0,'H1',120),
                     ('C2','C1',1.4,'H1',120,'H2',180),
                     ('H4','C2',1.0,'C1',120,'H1',60),
                     ('H6','C2',1.0,'C1',120,'H1',240)])
    output_bgf(name,atoms)

    return

def output_bgf(name,atoms):
    from Material import Material
    from vimmLib import save_file
    mat = Material(name)
    for atom in atoms: mat.add_atom(atom)
    mat.bonds_from_distance()
    save_file(name+'.bgf',mat)
    return    

if __name__ == '__main__': hydros()
            
            
