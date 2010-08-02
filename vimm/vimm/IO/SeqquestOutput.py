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


#!/usr/bin/env python

import string, re

from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Bond import Bond
from vimm.Cell import Cell
from vimm.Utilities import path_split, cleansym
from vimm.Element import sym2no
from vimm.Constants import bohr2ang

from vimm.NumWrap import array

p_atomtype = re.compile('^\s*atom type')
p_atomfile = re.compile('^\s*atom file')
p_geometry = re.compile('^\s*atom, t')
p_newgeo = re.compile('NEW')
p_nat = re.compile("^\s*number of atoms")
p_cell = re.compile('^\s*primitive l')
p_coord_type = re.compile('^\s*coordinates\s*$')
p_scale = re.compile('^\s*scale\s*$')
p_scalez = re.compile('^\s*scalez\s*$')
p_to_lattice = re.compile('to_lattice')
extensions = ["out"]
filetype = "Seqquest Output"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'r')

    # Initialize atom data
    material = Material(fileprefix)
    element = []     # Initialize element variable to be appended
    timestamp = 1
    nat = None
    cell = None
    lattice_coords = False
    scale = 1.
    scalez = 1.
    conv_to_ang = True

    while 1:
        line = file.readline()
        if not line: break

        if p_atomtype.search(line):
            # From the headerfile get the number of atom types
            line = file.readline()
            numberoftypes = int(line)

        elif p_coord_type.search(line):
            line = file.readline()
            line = line.strip().lower()
            if line == 'lattice':
                lattice_coords = True
        elif p_to_lattice.search(line):
            raise "Quest to_lattice flags not currently supported"

        elif p_scale.search(line):
            line = file.readline()
            scale = float(line.strip())

        elif p_scalez.search(line):
            line = file.readline()
            scalez = float(line.strip())

        # Using the atom type number, set the atom names
        elif p_atomfile.search(line):
            line = file.readline()
            words = string.split(line)
            atomname = cleansym(words[0]).capitalize()
            #atomname,atomext = path.splitext(words[0])
            #atomname = string.capitalize(atomname) # Captitalize the
            element.append(atomname)               # first letter

        elif p_nat.search(line):
            line = file.readline()
            words = string.split(line)
            nat = int(words[0])

        # Read in the initial geometry data
        elif p_geometry.search(line):
            for i in range(nat):
                line = file.readline()
                words = string.split(line)
                num = int(words[0])
                try:
                    type = element[int(words[1])-1]  #Set the type
                    atno = sym2no[type]
                except:
                    # Fallback for when atoms are specified with symbols
                    atno = sym2no[words[1]]
                x,y,z = [float(i) for i in words[2:5]]
                #print x,y,z
                if lattice_coords:
                    converter = cell.lat2cart_factory()
                    x,y,z = converter(x,y,z)
                    #print x,y,z
                elif conv_to_ang:
                    x,y,z = [bohr2ang*i for i in [x,y,z]]
                    #print x,y,z
                xyz = array((x,y,z))
                material.add_atom(Atom(atno, xyz))
            if cell: material.set_cell(cell)

        elif p_newgeo.search(line):
            comment = file.readline()
            material.new_geo()
            for i in range(nat):
                line = file.readline()
                words = string.split(line)
                num = int(words[0])
                try:
                    type = element[int(words[1])-1]  #Set the type
                    atno = sym2no[type]
                except:
                    # Fallback for when atoms are specified with symbols
                    atno = sym2no[words[1]]
                x,y,z = [float(i) for i in words[2:5]]
                #print x,y,z
                if lattice_coords:
                    converter = cell.lat2cart_factory()
                    x,y,z = converter(x,y,z)
                    #print x,y,z
                elif conv_to_ang:
                    x,y,z = [bohr2ang*i for i in [x,y,z]]
                    #print x,y,z
                xyz = array((x,y,z))
                material.add_atom(Atom(atno, xyz))
            if cell: material.set_cell(cell)
        elif p_cell.search(line):
            line = file.readline()
            words = string.split(line)
            ax,ay,az = [float(i) for i in words[:3]]
            if conv_to_ang:
                ax,ay,az = [bohr2ang*i for i in [ax,ay,az]]
            line = file.readline()
            words = string.split(line)
            bx,by,bz = [float(i) for i in words[:3]]
            if conv_to_ang:
                bx,by,bz = [bohr2ang*i for i in [bx,by,bz]]
            line = file.readline()
            words = string.split(line)
            cx,cy,cz = [float(i) for i in words[:3]]
            if conv_to_ang:
                cx,cy,cz = [bohr2ang*i for i in [cx,cy,cz]]
            cell = Cell((ax,ay,az),(bx,by,bz),(cx,cy,cz),
                        scale=scale,scalez=scalez)
    file.close()
    material.bonds_from_distance()
    return material


if __name__ == "__main__":

# Main program
    from sys import argv

    if (len(argv)>1):
        filename=argv[1]
    load(filename)

