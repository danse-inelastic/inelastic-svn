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


#pdb.py
# The format spec at:
#  http://www.rcsb.org/pdb/docs/format/pdbguide2.2/guide2.2_frame.html
# was useful.

import re
from vimm.Utilities import path_split
from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Bond import Bond
from vimm.Cell import Cell
from vimm.Element import sym2no
from vimm.NumWrap import array

extensions=["pdb"]
filetype="Protein data base"

# This is incomplete, and there must be a better way of doing this
symconv = {
    'H' : 'H', 'HA' : 'H', 'HB' : 'H', 'HG' : 'H', 'HD' : 'H', 'HE' : 'H',
    'HE' : 'H', 'HH' : 'H', 'HZ' : 'H',
    'C' : 'C', 'CA' : 'C', 'CB' : 'C', 'CG' : 'C', 'CD' : 'C', 'CE' : 'C',
    'CZ' : 'C', 'C1' : 'C', 'C2' : 'C',
    'N' : 'N', 'ND' : 'N', 'NE' : 'N', 'NH' : 'N',
    'O' : 'O', 'OD' : 'O', 'OG' : 'O', 'OE' : 'O', 'OH' : 'O', 'OX' : 'O',
    'SG' : 'S',
    }

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)

    curresnum = None
    curres = None
    locator = None
    residues = []
    for line in open(fullfilename):
        tag = line[:6].strip()
        if tag == 'ATOM' or tag == 'HETATM':
            loctag = line[16:17].strip()
            resnum = int(line[22:26])
            modifyer = line[26].strip()
            restag = line[18:21].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            xyz = array([x,y,z])
            try:
                sym = line[13:15].strip()
                sym = symconv[sym]
                atno = sym2no[sym]
            except:
                sym = line[12:15].strip()
                atno = sym2no[sym]
            if loctag:
                if not locator: locator = loctag
            if loctag and loctag != locator: continue
            if modifyer: continue  # skip residue #25B if we already have #25
            material.add_atom(Atom(atno,xyz))
        elif tag == 'CRYST1':
            words = line.split()
            a,b,c,alpha,beta,gamma = map(float,words[1:7])
            #finish
    material.bonds_from_distance()
    return material



