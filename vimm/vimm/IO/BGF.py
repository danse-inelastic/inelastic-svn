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

import re
from vimm.FortranIO import read,write
from vimm.Material import Material
from vimm.Cell import Cell, abcabg2abc,uc2abcabg
from vimm.Atom import Atom
from vimm.Bond import Bond
from vimm.Utilities import path_split,cleansym
from vimm.Element import sym2no,symbol
from vimm.NumWrap import array

extensions=["bgf"]
filetype="Biograf file format"

atom_format = "a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5, i3,i2,1x,f8.5"
atom_format_mini = "a6,1x,i5,18x,3f10.5,1x,a5, i3,i2,1x,f8.5"
bond_format = "a6,12i6"

def load(fullfilename):
    filedir, fileprefix, fileext = path_split(fullfilename)
    material=Material(fileprefix)
    file=open(fullfilename, 'r')

    hatpat = re.compile('HETATM')
    atpat = re.compile('^ATOM')
    conpat = re.compile('^CONECT')
    ordpat = re.compile('^ORDER')
    endpat = re.compile('^END')
    ucpat = re.compile('^CRYSTX')

    bonds = {}
    orders = {}
    iat = 0
    for line in open(fullfilename):
        if hatpat.search(line) or atpat.search(line):
            d1,i,d2,d3,d4,d5,x,y,z,attype,d6,d7,q = read(line,atom_format)
            xyz = array([x,y,z])
            sym = cleansym(attype)
            atno = sym2no[sym]
            atom = Atom(atno,xyz,sym,sym+str(iat))
            atom.fftype = attype # save just in case
            material.add_atom(atom)
            iat += 1
        elif conpat.search(line):
            ats = map(int,line[6:].split())
            index = ats[0]-1
            bonds[index] = [atj-1 for atj in ats[1:]]
            orders[index] = [1]*(len(ats)-1)
        elif ordpat.search(line):
            ords = map(int,line[6:].split())
            index = ords[0]-1
            orders[index] = ords[1:]
        elif ucpat.search(line):
            words = line.split()
            a,b,c,alpha,beta,gamma = map(float,words[1:7])
            axyz,bxyz,cxyz = abcabg2abc(a,b,c,alpha,beta,gamma)
            cell = Cell(axyz,bxyz,cxyz)
            material.set_cell(cell)
    atoms = material.get_atoms()
    #print len(atoms)," atoms loaded"
    for iat in bonds.keys():
        bond_partners = bonds[iat]
        bond_orders = orders[iat]
        for jat,ij_order in zip(bond_partners,bond_orders):
            if jat > iat: material.add_bond(Bond(atoms[iat],atoms[jat],
                                                 ij_order))
    return material

def new(): return Material("New BGF Material")

def save(filename,material):
    file=open(filename, 'w')
    atoms = material.get_atoms()
    bonds = material.get_bonds()
    cell = material.get_cell()

    file.write("XTLGRF 200\n")
    file.write("DESCRP Model2\n")      
    file.write("REMARK BGF file created by vimm\n")
    file.write("FORCEFIELD DREIDING\n")  
    file.write("PERIOD 111\n")
    file.write("AXES   ZYX\n")
    file.write("SGNAME P 1                  1    1\n")
    if cell:
        file.write("CRYSTX %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f\n" % cell.abcabg())
    file.write("FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x"\
               ",a1,1x,a5,3f10.5,1x,a5, i3,i2,1x,f8.5)\n")

    write_atoms(file,atoms,atom_format)

    if bonds:
        # Convert the bonds into a list of atoms + bond partners
        bond_partners,bond_orders = make_bond_order_lists(atoms,bonds)
        write_bonds(file,bond_partners,bond_orders,bond_format)
    file.write('END\n')
    return

def make_bond_order_lists(atoms,bonds):
    for i in range(len(atoms)):
        atom = atoms[i]
        atom.index = i
        atom.bond_partners = []
        atom.bond_orders = []
    for bond in bonds:
        ati,atj = bond.get_atoms()
        iorder = bond.get_order()
        ati.bond_partners.append(atj.index)
        atj.bond_partners.append(ati.index)
        ati.bond_orders.append(iorder)
        atj.bond_orders.append(iorder)
    bond_partners = []
    bond_orders = []
    for atom in atoms:
        bond_partners.append(atom.bond_partners)
        bond_orders.append(atom.bond_orders)
    return bond_partners,bond_orders

def write_bonds(file,bond_partners,bond_orders,bond_format):
    file.write("FORMAT CONECT (a6,12i6)\n")
    for i in range(len(bond_partners)):
        array = ['CONECT',i+1] + [j+1 for j in bond_partners[i]]
        conect = write(array,bond_format) + "\n"
        file.write(conect)
        # Only write out bond orders if they're not all 1:
        if max(bond_orders[i]) > 1:
            array = ['ORDER',i+1] + [j for j in bond_orders[i]]
            order = write(array,bond_format) + "\n"
            file.write(order)
    return

def write_atoms(file,atoms,atom_format):
    iat = 1
    for atom in atoms:
        x,y,z = atom.get_xyz()
        atno = atom.get_atno()
        sym = atom.symbol
        if atom.fftype:
            fftype = atom.fftype
        else:
            fftype = atom.symbol
        line = write(['HETATM',iat,sym,'RES','A','444',x,y,z,
                      fftype,0,0,0],atom_format) + '\n'
        file.write(line)
        iat += 1
    return

def test():
    mat = load("Geos/benzene_dimer.bgf")
    for atom in mat.get_atoms():
        print atom.atno,atom.xyz

if __name__ == '__main__': test()

