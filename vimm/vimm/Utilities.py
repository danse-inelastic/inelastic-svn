# Vimm: Visual Interface for Materials Manipulation
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


#utility_functiions.py

import re, os

def assureCorrectFileEnding(filename, extension):
    """Appends correct file ending in case user doesn't"""
    import os
    path,ext = os.path.splitext(filename)
    if ext !='.'+extension: filename = filename + '.'+extension
    return filename 

def cleansym(s):
    """This function strips off the garbage (everything after and including
    the first non-letter) in an element name."""
    return re.split('[^a-zA-Z]',s)[0]

def path_split(fullfilename):
    "Split a filename into directory, name, and extension"
    dir,fname=os.path.split(fullfilename)
    name,ext=os.path.splitext(fname)
    ext = ext.replace('.','')
    return dir, name, ext

def entry_float(entry,default=0):
    try: val = float(entry.GetValue())
    except: val = default
    return val

def entry_int(entry,default=0):
    try: val = int(entry.GetValue())
    except: val = default
    return val

def entry_string(entry,default=''):
    val = entry.GetValue()
    if not val: val = default
    return val

def bbox_atoms(atoms, buffer=2.,big=1000):
    xmin = big
    ymin = big
    zmin = big
    xmax = -big
    ymax = -big
    zmax = -big
    
    for atom in atoms:
        xyz = atom.get_position()
        xmin = min(xmin,xyz[0])
        ymin = min(ymin,xyz[1])
        zmin = min(zmin,xyz[2])
        xmax = max(xmax,xyz[0])
        ymax = max(ymax,xyz[1])
        zmax = max(zmax,xyz[2])
        
    if buffer:
        xmin -= buffer
        ymin -= buffer
        zmin -= buffer
        xmax += buffer
        ymax += buffer
        zmax += buffer
    return xmin,xmax,ymin,ymax,zmin,zmax
    
def isapprox(a,b,delta=1e-5): return abs(a-b) < delta
