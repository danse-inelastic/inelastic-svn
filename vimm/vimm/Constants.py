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
"""\
 Constants.py: Useful constants 
"""

# Misc units
Clight=2.99792458e8     # speed of light in m/s
Kboltz=3.166830e-6      # Boltzmann constant
e2 = 14.399             # Coulomb's law coeff if R in \AA and resulting E in eV
planck=6.6260755e-34    # Planck's constant, in Js

# Distance units
bohr2ang = 0.529177249  # Conversion of length from bohr to angstrom
ang2bohr = 1/bohr2ang

# Energy units
hartree2kcal = 627.5095 # Hartree to kcal/mol conversion
kcal2hartree = 1/hartree2kcal

ev2kcal = 23.061        # Conversion of energy in eV to energy in kcal/mol
kcal2ev = 1/ev2kcal

hartree2joule = 4.3597482e-18   # Hatree to Joule conversion factor
joule2hartree = 1/hartree2joule

# Rydbergs to hartree
hartree2rydberg = 2.
rydberg2hartree = 1/hartree2rydberg

# Mass units
amu2me = 1822.882       # Conversion from mass in amu to mass in au (m_e)
me2amu = 1/amu2me       # Conversion from mass in au (m_e) to mass in amu 

# Time units
tau2ps = 41341.447      # Conversion from time in au to time in ps
ps2tau = 1/tau2ps       # inverse

# Derived quantities
Rgas = Kboltz*hartree2kcal*1000.0 # gas constant R = 1.98722 cal/mole/K

# Etemp_conversion
#  = 6.3336e-6 -> kT(Ry) = etemp_Ry_per_K*T(K)
etemp_Ry_per_K = Rgas*kcal2hartree*hartree2rydberg/1000

# Conversion functions:
def Ang2Bohr(x): return ang2bohr*x
def Bohr2Ang(x): return bohr2ang*x

