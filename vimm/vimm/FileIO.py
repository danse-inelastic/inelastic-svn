# vimm: Visual Interface for Materials Manipulation
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA	02111-1307	
# USA


#!/usr/bin/env python

# Consider autoscanning the IO directory here...
from vimm.IO import XYZ,\
    Cif, \
    PickledStructure, \
	JaguarOutputReader, \
	NWChemOutput, \
   	SeqquestHist, \
  	SeqquestInput, \
   	SeqquestOutput,\
   	Molf, \
   	PDB, \
   	Towhee, \
   	CTab, \
   	BGF, \
   	CML, \
   	CXYZ, \
   	AbinitInput,\
   	AbinitOutput,\
   	Mol,\
	POVOutput,\
	MPQCOutput,\
    ScatteringFunction


modules = [
	XYZ,
    Cif,
	PickledStructure,
	SeqquestOutput,
	JaguarOutputReader,
	NWChemOutput,
	SeqquestHist,
	SeqquestInput,
	Molf,
	PDB,
	Towhee,
	CTab,
	BGF,
	CML,
	CXYZ,
	AbinitInput,
	AbinitOutput,
	Mol,
	POVOutput,
	MPQCOutput,
    ScatteringFunction
	]

def loaders():
	file_loaders = {}

	for module in modules:
		if hasattr(module,'load'):
			func = getattr(module,'load')
			func.type = getattr(module,'filetype')
			for ext in module.extensions:
				if file_loaders.has_key(ext): file_loaders[ext].append(func)
				else: file_loaders[ext] = [func]
	return file_loaders

def savers():
	file_savers = {}
	for module in modules:
		if hasattr(module,'save'):
			func = getattr(module,'save')
			func.type = getattr(module,'filetype')
			for ext in module.extensions:
				if file_savers.has_key(ext): file_savers[ext].append(func)
				else: file_savers[ext] = [func]
	return file_savers

def typestrings(fhandlers): 
    return [f.type for f in fhandlers]
