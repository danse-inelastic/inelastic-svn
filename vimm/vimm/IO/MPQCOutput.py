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


import re
from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["log","out"]
filetype="MPQC Output Format"

geostart = re.compile("n\s+atoms\s+geometry\s+")
atpat = re.compile("\s+\d+\s+(\w+)\s+\[\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*\]\s*$")
#atpat = re.compile("\s+\d+\s+(\w+)\s+[\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*]\s*$")
geoend = re.compile("}")

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    file=open(fullfilename, 'r')

    first_run = 1

    while 1:
        line = file.readline()
        if not line: break
        if not geostart.search(line): continue
        if first_run:
            first_run = 0
        else:
            material.new_geo()
        i = 1
        while 1:
            line = file.readline()
            if geoend.search(line): break
            match = atpat.match(line)
            sym = match.group(1)
            x = float(match.group(2))
            y = float(match.group(3))
            z = float(match.group(4))
            sym=cleansym(sym)
            atno = sym2no[sym]
            xyz = array((x,y,z))
            material.add_atom(Atom(atno, xyz, sym, sym+str(i)))
            i += 1
    material.bonds_from_distance()
    return material

def new():
    material = Material("New XYZ Molecule")
    return material
