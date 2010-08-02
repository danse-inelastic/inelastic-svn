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



from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Cell import Cell
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no
from vimm.NumWrap import array
from vimm.Constants import bohr2ang

from math import ceil

extensions = ["hist"]
filetype = "Seqquest History"


def load(fullfilename):
    gstep = 0
    filedir, fileprefix, fileext = path_split(fullfilename)
    file=open(fullfilename, 'r')
    
    # Initialize atom data
    material = Material(fileprefix)
    opts = {}
    material.seqquest_options = opts

    dconv = 1. # default to Angstroms, which don't need conversion
    cell = None

    while 1:
        line = file.readline()
        if not line: break
        line = line.strip()
        if line == '@=KEYCHAR':
            continue # ignore other keychars for now
        elif line == '@DISTANCE UNIT':
            line = file.readline().strip()
            if line == 'ANGSTROM':
                continue
            elif line == 'BOHR':
                dconv = bohr2ang
            else:
                print "Warning: unknown distance unit ",line
        elif line == '@DIMENSION':
            line = file.readline().strip()
            opts['ndim'] = int(line)
        elif line == '@NUMBER OF ATOMS':
            line = file.readline().strip()
            opts['nat'] = int(line)
            opts['attypes'] = []
            nread = int(ceil(opts['nat']/20.))
            for i in range(nread):
                line = file.readline().strip()
                opts['attypes'].extend(map(int,line.split()))
            assert len(opts['attypes']) == opts['nat']
        elif line == '@TYPES':
            line = file.readline().strip()
            opts['ntyp'] = int(line)
            opts['types'] = []
            for i in range(opts['ntyp']):
                line = file.readline().strip()
                opts['types'].append(cleansym(line))
        elif line == '@CELL VECTORS':
            line = file.readline()
            axyz = map(float,line.split())
            line = file.readline()
            bxyz = map(float,line.split())
            line = file.readline()
            cxyz = map(float,line.split())
            if abs(dconv-1) > 1e-4: # careful when comparing floats
                axyz = axyz[0]*dconv,axyz[1]*dconv,axyz[2]*dconv
                bxyz = bxyz[0]*dconv,bxyz[1]*dconv,bxyz[2]*dconv
                cxyz = cxyz[0]*dconv,cxyz[1]*dconv,cxyz[2]*dconv
            cell = Cell(axyz,bxyz,cxyz)
        elif line == '@GSTEP':
            line = file.readline().strip()
            gstep = int(line)
        elif line == '@COORDINATES':
            atoms = []
            for i in range(opts['nat']):
                line = file.readline()
                xyz = map(float,line.split())
                if abs(dconv-1) > 1e-4: # careful when comparing floats
                    xyz = xyz[0]*dconv,xyz[1]*dconv,xyz[2]*dconv
                isym = opts['attypes'][i]
                sym = opts['types'][isym-1]
                atoms.append((sym,xyz))
            if gstep > 1: material.new_geo()
            for i in range(opts['nat']):
                sym,xyz = atoms[i]
                atno = sym2no[sym]
                xyz = array(xyz)
                material.add_atom(Atom(atno,xyz))
            if cell: material.set_cell(cell)
        elif line == '@ESCF':
            line = file.readline().strip()
            escf = float(line)
            # Consider saving these for plotting
        elif line == '@FORCES':
            forces = []
            for i in range(opts['nat']):
                line = file.readline()
                forces.append(map(float,line.split()))
        elif line == '@FMAX':
            line = file.readline().strip()
            fmax = float(line)
        elif line == '@FRMS':
            line = file.readline().strip()
            frms = float(line)
        else:
            print "Unknown line ",line
    material.bonds_from_distance()
    return material

            
                
                
            
            
        
