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

import re

from vimm.Material import Material
from vimm.Atom import Atom
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["molf"]
filetype="Molden interchange format"

atpat = re.compile('\[Atoms\]')
bfpat = re.compile('\[GTO\]')
orbpat = re.compile('\[MO\]')

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    file=open(fullfilename, 'r')

    atoms = []
    bfs = []
    orbs = []

    mode = None

    for line in file.readlines():
        if atpat.search(line): mode = 'atoms'
        elif bfpat.search(line): mode = 'bfs'
        elif orbpat.search(line): mode = 'orbs'
        elif mode == 'atoms': atoms.append(line)
        elif mode == 'bfs': bfs.append(line)
        elif mode == 'orbs': orbs.append(line)
        else: print '? ',line,

    for line in atoms:
        words = line.split()
        if len(words) < 6: continue
        
        atno = int(words[2])
        xyz = map(float,words[3:6])
        material.add_atom(Atom(atno,array(xyz)))
    material.bonds_from_distance()
    material.geo.basis = parse_basis(bfs)
    material.geo.orbs = parse_orbs(orbs)
    return material

def save(filename,material):
    file = open(filename,'w')
    i = 1
    for atom in material.get_atoms():
        atno = atom.get_atno()
        xyz = atom.get_position()
        file.write('%s %5.0f %5.0f %10.4f %10.4f %10.4f\n' %
                   (symbol[atno],i,atno,xyz[0],xyz[1],xyz[2]))
        i+= 1
    return

def parse_basis(lines):

    bfs = []

    while 1:
        line = lines.pop(0)
        if not line: break
        words = line.split()
        if not words: break
        iat,ibs = map(int,words)
        atbasis = []
        while 1:
            line = lines.pop(0)
            words = line.split()
            if not words: break
            type = words[0]
            nprim = int(words[1])
            coef = float(words[2])
            prims = []
            for i in range(nprim):
                line = lines.pop(0)
                exp,coef = map(float,line.split())
                prims.append((exp,coef))
            atbasis.append((type,prims))
        bfs.append((iat,atbasis))
    #print_bfs(bfs)
    return bfs

def parse_orbs(lines):
    sympat = re.compile('^Sym\s*=\s*(\S+)$')
    enepat = re.compile('^Ene\s*=\s*(\S+)$')
    spinpat = re.compile('^Spin\s*=\s*(\S+)$')
    occpat = re.compile('^Occup\s*=\s*(\S+)$')
    coefpat = re.compile('\s*(\d+)\s*(\S+)$')

    orbs = []
    sym,ene,spin,occ,coefs = None,None,None,None,[]

    for line in lines:
        if sympat.match(line):
            if sym: orbs.append((sym,ene,spin,occ,coefs))
            sym,ene,spin,occ,coefs = None,None,None,None,[]
            sym = sympat.match(line).groups()[0]
        elif enepat.match(line):
            ene = float(enepat.match(line).groups()[0])
        elif spinpat.match(line):
            spin = spinpat.match(line).groups()[0]
        elif occpat.match(line):
            occ = float(occpat.match(line).groups()[0])
        elif coefpat.match(line):
            a,b = coefpat.match(line).groups()
            iorb,coef = int(a),float(b)
            coefs.append((iorb,coef))
    #print_orbs(orbs)
    return orbs

def print_orbs(orbs):
    i = 1
    for orb in orbs:
        sym,ene,spin,occ,coefs = orb
        print "%4d %10.4f %10.4f" % (i,ene,occ)
        i += 1
    return

def print_bfs(bfs):
    for bf in bfs:
        iat,atbasis = bf
        print iat
        for atb in atbasis:
            type,prims = atb
            print "    ",type
            for exp,coef in prims:
                print "        ",exp,coef
    return
