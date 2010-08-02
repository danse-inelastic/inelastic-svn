#!/usr/bin/env python
"""\
 AbinitInput.py - Reader for inputting abinit input files.
"""

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
from vimm.Cell import Cell,abcabg2abc
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array
from vimm.Constants import bohr2ang

import re

extensions=["in"]
filetype="Abinit input format"

def abinit_tokenizer(fobj,**kwargs):
    "Turn an abinit file into a list of words, skipping comment lines"
    ofile = kwargs.get('ofile',False)
    VERBOSE = kwargs.get('VERBOSE',False)
    startpat = re.compile('^\s*\-outvars:')
    endpat = re.compile('^===')
    started = False
    for line in fobj:
        if ofile and startpat.search(line):
            if VERBOSE: print "abinit-tokenizer started"
            started = True
            continue
        if ofile and endpat.search(line):
            if VERBOSE: print "abinit-tokenizer ended"
            started = False
            continue
        if ofile and not started: continue
        for word in line.split():
            if word[0] == '#': break # skip to end of line
            yield word
    return

def nextn(iterable,n=1):
    data = []
    for i in range(n): data.append(iterable.next())
    return data

def abinit_comment(line): return line[0] == '#'

def get_natom3(iterable,natom):
    data = []
    for i in range(natom):
        data.append([aifloat(i) for i in nextn(iterable,3)])
    return data

def aifloat(str):
    # Like normal float, but also tries to eval
    #  things like "2/3"
    try:
        val = float(str)
    except:
        num,denom = str.split("/")
        val = float(num)/float(denom)
    return val
        

def load(fullfilename,**kwargs):
    # Keyword args
    VERBOSE = kwargs.get('VERBOSE',False)
    
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)

    # Pass 1: check ndtset
    ndtset = 0
    natom = 0
    ntypat = 0
    dt = 1
    iter = abinit_tokenizer(open(fullfilename),**kwargs)
    while 1:
        try:
            word = iter.next()
        except:
            break
        if word == 'ndtset':
            ndtset = int(iter.next())
            if ndtset > 1:
                print "Multiple data sets found. Reading only the first"
                # If you want to select a particular data set, pop
                #  up a dialog box here and ask which one you
                #  want to load.
                # Also need to put code in here so that you don't
                #  get the dialog box twice, such as dt_selected
                #  boolean
        elif word == 'natom':
            natom = int(iter.next())
        elif word == 'ntypat':
            ntypat = int(iter.next())
            
    # Pass 2: get remaining info
    xangst = None
    xred = None
    xcart = None
    znucl = None
    typat = None
    rprim = None
    acell = None
    angdeg = None
    iter = abinit_tokenizer(open(fullfilename),**kwargs)
    while 1:
        try:
            word = iter.next()
        except:
            break
        if word == 'xangst' or word == 'xangst%d' % dt:
            xangst = get_natom3(iter,natom)
        elif word == 'xred' or word == 'xred%d' % dt:
            xred = get_natom3(iter,natom)
        elif word == 'xcart' or word == 'xcart%d' % dt:
            xcart = get_natom3(iter,natom)
        elif word == 'znucl':
            znucl = [int(float(i)) for i in nextn(iter,ntypat)]
        elif word == 'typat':
            typat = [int(i) for i in nextn(iter,natom)]
        elif word == 'acell' or word == 'acell%d' % dt:
            acell = [float(i) for i in nextn(iter,3)]
        elif word == 'rprim' or word == 'rprim%d' % dt:
            rprim = [float(i) for i in nextn(iter,9)]
        elif word == 'angdeg' or word == 'angdeg%d' % dt:
            angdeg = [float(i) for i in nextn(iter,3)]

    # Done parsing
    if VERBOSE:
        print "natom = ",natom
        print "ntypat = ",ntypat
        print "znucl = ",znucl
        print "typat = ",typat
        print "xcart = ",xcart
        print "xred = ",xred
        print "xangst = ",xangst
        print "acel = ",acell
        print "rprim = ",rprim
        print "angdeg = ",angdeg

    # Build the unit cell. Precedence is rprim > angdeg
    if not acell: acell = [1,1,1]
    acell = [bohr2ang*i for i in acell] # Convert acell to Angstrom
    
    if rprim:
        ax,ay,az,bx,by,bz,cx,cy,cz = rprim
        cell = Cell( (acell[0]*ax,acell[0]*ay,acell[0]*az),
                     (acell[1]*bx,acell[1]*by,acell[1]*bz),
                     (acell[2]*cx,acell[2]*cy,acell[2]*cz))
    else:
        if not angdeg:
            angdeg = [90.,90.,90.]
        axyz,bxyz,cxyz = abcabg2abc(acell[0],acell[1],acell[2],
                                    angdeg[0],angdeg[1],angdeg[2])
        cell = Cell(axyz,bxyz,cxyz)
    material.set_cell(cell)
    
    # Build the atom list. Precedence is xred > xangst > xcart
    if xred:
        A,B,C = cell.abc()
        for i in range(natom):
            atno = znucl[typat[i-1]-1]
            xr,yr,zr = xred[i]
            xyz = xr*A + yr*B + zr*C
            material.add_atom(Atom(atno,xyz))
    elif xangst:
        for i in range(natom):
            atno = znucl[typat[i-1]-1]
            material.add_atom(Atom(atno,xangst[i]))
    elif xcart:
        for i in range(natom):
            atno = znucl[typat[i-1]-1]
            xyz = [bohr2ang*a for a in xcart[i]]
            material.add_atom(Atom(atno,xyz))
    else:
        raise "Abinit Input: must specify xred, xangst, or xcart"
    material.bonds_from_distance()
    return material

