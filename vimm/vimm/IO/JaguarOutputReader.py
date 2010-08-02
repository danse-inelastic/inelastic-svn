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


#!/usr/bin/python

from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no
from vimm.NumWrap import array
import string,re

extensions = ["out"]
filetype = "Jaguar"

def get_geo(file):
    geo = []
    lines2skip = 2
    for i in range(lines2skip): file.readline()
    while 1:
        line = file.readline()
        if not line: break
        words = string.split(line)
        if len(words) < 4: break
        sym = cleansym(words[0])
        atno = sym2no[sym]
        if atno == 0: continue
        xyz = array(map(float,words[1:4]))
        geo.append((atno,xyz))
    return geo
    

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    file = open(fullfilename,'r')
    jaguar_options = {}

    inpg_pat = re.compile("Input geometry:")
    symg_pat = re.compile("Symmetrized geometry:")
    newg_pat = re.compile("new geometry:")
    fing_pat = re.compile("final geometry:")
    basis_pat = re.compile("basis set:")
    molchg_pat = re.compile("net molecular charge:")
    multip_pat = re.compile("multiplicity:")

    geos = []
    while 1:
        line = file.readline()
        if not line: break
        if inpg_pat.search(line) or symg_pat.search(line) \
           or newg_pat.search(line) or fing_pat.search(line):
            geo = get_geo(file)
            geos.append(geo)
        elif basis_pat.search(line):
            words = string.split(line)
            jaguar_options['basis'] = words[2]
        elif molchg_pat.search(line):
            words = string.split(line)
            jaguar_options['molchg'] = int(words[3])
        elif multip_pat.search(line):
            words = string.split(line)
            jaguar_options['multip'] = int(words[1])
    # end of main infinite loop
    file.close()

    print "Loading %d geometries" % len(geos)
    for igeo in range(len(geos)):
        if igeo: material.new_geo()
        for (atno,xyz) in geos[igeo]:
            material.add_atom(Atom(atno,xyz))
    if len(material.geo.atoms) < 200: material.bonds_from_distance()
    material.jaguar_options = jaguar_options
    return material


